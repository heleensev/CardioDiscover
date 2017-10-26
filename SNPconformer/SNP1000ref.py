from UnqWrap import DbModifier
from UnqWrap import DbQuerier
from SNPconformer.config import NoRefMatchException
from humantime import get_time
import logging, sys

db = DbModifier
collection = DbQuerier.Collection
frq_switch_sum = 0
no_match_sum = 0
logger = logging.getLogger(__name__)


def init_collection():
    global collection
    logger.info('initiating SNP1000 collection at {}'.format(get_time()))
    collection = DbQuerier('../DB/GWAS').db_collection('SNP1000')


def reference_check(SNP, BP, A1, A2, FRQ, GWAS_set, chnk_num):
    global collection, no_match_sum
    ref_all, alt_all = str()
    remove = False

    try:
        def orientation_check():
            # allele 1 and 2, may be changed throughout this function block,
            # if orientation differs from reference
            global A1, A2
            complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

            def allele_check():
                global A1, A2
                # allele_check if the ref and alt allele corresponds with assumed position
                if ref_all == A2 and alt_all == A1:
                    return True
                # allele_check if ref and alt allele are switched from position
                elif ref_all == A1 and alt_all == A2:
                    # swap the two variables around
                    A1, A2 = A2, A1
                    # log the alternative column position
                    # GWAS_set.loc[GWAS_set['SNP']]
                    return True
            if not allele_check():
                # if first check failed, get complementary alleles to perform check again
                A1 = ''.join([complements.get(x) for x in A1])
                A2 = ''.join([complements.get(x) for x in A2])
                if allele_check():
                    logger.info('complementary alleles for {}'.format(SNP))
                    return True

        def SNP_lookup():
            global ref_all, alt_all
            # search database for matching SNP identifier
            search = collection.fetch('SNP', SNP)
            match = False
            # for multi_allelic SNPs, multiple entries for one rs ID, so: len list > 1
            if len(search) > 0:
                while True:
                    for i, entry in enumerate(search):
                        ref_all = entry.get('REF')
                        alt_all = entry.get('ALT')
                        if orientation_check():
                            match = True
                            break
                    if match:
                        break
                    raise NoRefMatchException('No matching allele pair')
            else:
                raise NoRefMatchException('No hit in for SNP ID')
            return entry

        def frequency_check():
            global frq_switch_sum
            frq_range = 0.15
            under_range = float(FRQ) - frq_range
            upper_range = float(FRQ) + frq_range
            eur_frq = float(entry.get('EUR_AF'))
            MAF = 1 - eur_frq

            # if eur_freq is smaller than under_range and higher than upper_range
            if under_range < eur_frq < upper_range:
                # check most frequently occurring condition first
                pass
            elif under_range < MAF < upper_range:
                # replace frq in GWAS_set with MAF in document matching the SNP ID and FRQ
                GWAS_set.ix[(GWAS_set['SNP'] == SNP) & GWAS_set['FRQ'] == FRQ] = MAF
                frq_switch_sum += 1
            else:
                raise NoRefMatchException('no matching frequency')

        # call SNP_lookup to initiate lookup, allele check
        entry = SNP_lookup()
        # call frequency check to determine if the SNP is correctly called
        frequency_check()

        # position in reference dataset (GRCh38) may differ from GWAS dataset
        ref_loc = entry.get('POS')
        # replace base pair position if different from reference
        if BP != ref_loc:
            GWAS_set.ix[(GWAS_set['SNP'] == SNP) & GWAS_set['POS'] == FRQ] = ref_loc

    except NoRefMatchException as message:
        logger.info('{} for SNP: {} ({},{})'.format(message, SNP, A2, A1))
        no_match_sum += 1
        remove = True
    except:
        logger.error(sys.exc_info())
        logger.error('during liftover at chunk {}, at row {}'.format(chnk_num, SNP))
        remove = True
    finally:
        # if an exception occurred, remove row from dataframe: GWAS_set
        if remove:
            bad_row = GWAS_set[(GWAS_set.snp == SNP) & (GWAS_set.frq == FRQ)]
            GWAS_set.drop(bad_row)
