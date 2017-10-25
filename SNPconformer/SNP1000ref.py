from UnqWrap import DbModifier
from UnqWrap import DbQuerier
from SNPconformer.config import NoRefMatchException
from humantime import get_time
import logging, sys

db = DbModifier
collection = DbQuerier.Collection
frq_switch_sum = 0
logger = logging.getLogger(__name__)


def init_collection():
    global collection
    collection = DbQuerier('../DB/GWAS').db_collection('SNP1000')


def reference_check(SNP, BP, A1, A2, FRQ, gwas_set, chnk_num):
    global collection
    global frq_switch_sum
    remove = False
    try:
        def orientation_check():
            global A1, A2
            complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

            def check():
                global A1, A2
                # check if the ref and alt allele corresponds with assumed position
                if ref_all == A2 and alt_all == A1:
                    return True
                # check if ref and alt allele are switched from position
                elif ref_all == A1 and alt_all == A2:
                    # swap the two variables around
                    A1, A2 = A2, A1
                    # log the alternative column position
                    # gwas_set.loc[gwas_set['SNP']]
                    print('A1: {}, A2: {}'.format(A1, A2))
                    return True
            if not check():
                A1 = ''.join([complements.get(x) for x in A1])
                A2 = ''.join([complements.get(x) for x in A2])
                print(A1, A2)
                if check():
                    #log complement
                    return True

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

        frq_range = 0.15
        under_range = float(FRQ)-frq_range
        upper_range = float(FRQ)+frq_range
        eur_frq = float(entry.get('EUR_AF'))
        # position in reference dataset (GRCh38) may differ from GWAS dataset
        location = entry.get('POS')
        MAF = 1-eur_frq

        # if eur_freq is smaller than under_range and higher than upper_range
        if under_range < eur_frq < upper_range:
            pass
        elif under_range < MAF < upper_range:
            # replace frq in gwas_set with MAF in document matching the SNP ID and FRQ
            gwas_set.ix[(gwas_set['SNP'] == SNP) & gwas_set['FRQ'] == FRQ] = MAF
            frq_switch_sum += 1
        else:
            raise NoRefMatchException('no matching frequency')
    except NoRefMatchException as e:
        logger.info('{} for SNP: {} ({},{})'.format(e, SNP, A2, A1))
        remove = True
    except:
        logger.error(sys.exc_info())
        logger.error('during liftover at chunk {}, at row {}'.format(chnk_num, SNP))
        remove = True
    finally:
        # if an exception occurred, remove row from dataframe
        if remove:
            bad_row = gwas_set[(gwas_set.snp == SNP) & (gwas_set.frq == FRQ)]
            gwas_set.drop(bad_row)
