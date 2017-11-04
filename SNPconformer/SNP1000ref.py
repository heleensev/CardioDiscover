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


def reference_check(SNP, BP, A1, A2, FRQ, GWAS_set, effect, chnk_num):
    # check the SNPs in the GWAS set with the reference (1000 genome call set)
    # desired format: A1: ref allele, A2: alt allele, FRQ: alt allele frequency
    global collection, no_match_sum
    ref_all, alt_all = str()
    # assign different name for original variables, to distinguish from
    # (possibly) mutated variables
    org_A1, org_A2 = A1, A2
    # in orientation check the allele corresponding to the reference allele is found
    org_key, org_val = 'A1', org_A1  # key and value to lookup unique SNP entry
    # bool for (not) removing row at the end of this function block
    remove = False

    try:
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
                        assert(A1 and A2 in ['A', 'T', 'C', 'G'])
                        if orientation_check():
                            match = True
                            break
                    if match:
                        break
                    raise NoRefMatchException('No matching allele pair')
            else:
                raise NoRefMatchException('No hit in for SNP ID')
            return entry

        def orientation_check(comp=False):
            # allele 1 and 2, may be changed throughout this function block,
            # if orientation differs from reference
            global A1, A2, ref, org
            # complementary alleles to look up during orientation check
            complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

            def replace_alleles(ref, org):
                global org_key, org_val
                GWAS_set.ix[(GWAS_set.SNP == SNP) & GWAS_set[ref] == org, 'A1'] = A1
                GWAS_set.ix[(GWAS_set.SNP == SNP) & GWAS_set[ref] == org, 'A2'] = A2
                # set variables for finding the entry with alt allele
                org_key, org_val = ref, org

            # allele_check if the ref and alt allele corresponds with assumed position
            if ref_all == A2 and alt_all == A1:
                if comp:
                    replace_alleles('A1', org_A1)
                return True
            # allele_check if ref and alt allele are switched from position
            elif ref_all == A1 and alt_all == A2:
                # swap the two variables around
                A1, A2 = A2, A1
                # replace the column positions for the swapped alleles in GWAS_set
                replace_alleles('A2', org_A2)
                return True
            else:
                # if first check failed, get complementary alleles to perform check again
                A1 = ''.join([complements.get(x) for x in A1])
                A2 = ''.join([complements.get(x) for x in A2])
                if orientation_check(True):
                    logger.info('complementary alleles for {}'.format(SNP))
                    return True

        def frequency_check():
            global frq_switch_sum
            frq_range = 0.15
            eur_frq = float(entry.get('EUR_AF'))

            def check_range(inverse=False):
                global FRQ
                FRQ = float('%f' % FRQ)
                if inverse:
                    FRQ = 1 - FRQ
                under_range = FRQ - frq_range
                upper_range = FRQ + frq_range
                # if eur_freq is smaller than under_range and higher than upper_range
                if under_range < eur_frq < upper_range:
                    return True

            def inverse_replace_frq_odds():
                # inverse the frequency and odds ratio (or beta) to match the alternative SNP
                # inversed effect (FRQ is already inversed in check_range when not matching to alt allele
                EFF = float(float(effect) * -1)
                GWAS_set.ix[(GWAS_set.SNP == SNP) & GWAS_set[org_key] == org_val, 'FRQ'] = FRQ
                GWAS_set.ix[(GWAS_set.SNP == SNP) & GWAS_set[org_key] == org_val, 'effect'] = EFF

            # check most frequently occurring condition first
            if check_range(FRQ):
                pass
            elif check_range(inverse=True):
                # if the frequency was for the ref allele, it is inversed and replaced in GWAS_set
                inverse_replace_frq_odds()
                frq_switch_sum += 1
            else:
                raise NoRefMatchException('no matching frequency')

        def indel_check():
            ref_variant = entry.get('VT')
            if ref_variant == 'INDEL'


        # call SNP_lookup to initiate lookup, allele check
        entry = SNP_lookup()
        # call frequency check to determine if the SNP is correctly called
        frequency_check()
        # position in reference dataset (GRCh38) may differ from GWAS dataset
        ref_loc = entry.get('POS')
        # replace base pair position if different from reference
        if BP != ref_loc:
            GWAS_set.ix[(GWAS_set.SNP == SNP) & GWAS_set[org_key] == org_val, 'BP'] = ref_loc

    except NoRefMatchException as message:
        logger.info('{} for SNP: {} ({},{})'.format(message, SNP, A2, A1))
        no_match_sum += 1
        remove = True
    except:
        logger.error(sys.exc_info())
        logger.error('during liftover at chunk {}, at row {}'.format(chnk_num, SNP))
        remove = True
    finally:
        # if an exception occurred, remove row from GWAS_set
        if remove:
            bad_row = GWAS_set[(GWAS_set.snp == SNP) & (GWAS_set[org_key] == org_val)]
            GWAS_set.drop(bad_row)

"""
note: org_key, org_val obsolete, unique entry found with A1 = ref.alt
inplace replacement done on iteratabe GWAS_set, change in file reader
check order unpacking of values from iterable after reading file
"""
