from SNPconformer import liftover, reference_check
from timebuddy import get_time
import pandas as pd
import logging, sys

GWAS = ""
logger = logging.getLogger(__name__)


def init_file_reader():
    logging.basicConfig(filename='../SNP.log', filemode='a', level=logging.DEBUG)

    logger.info('initiating SNP conformer at {}'.format(get_time()))

    # initiate collection object for querying the database
    liftover.init_collection()
    reference_check.init_collection()

    # call read file, to initiate read, SNP liftover and reference check procedure
    read_file(GWAS, 5000)
    # get stats at end of procedure for future reference
    get_stats()


def read_file(file, chsize):
    logger.info('initiating read_file at {}'.format(get_time()))
    for chnk_num, GWAS_set in enumerate(pd.read_csv(file, chunksize=chsize, header=None, sep='\t')):
        print("entering file {}: chunk: {}".format(file, chnk_num))
        iterate_file(chnk_num, GWAS_set.itertuples(index=True), GWAS_set)


def iterate_file(chnk_num, GWAS_chnk, GWAS_set, SNP='SNP', i=0):
    logger.info('initiating iterate_file at {}'.format(get_time()))
    try:
        for i, _, _, SNP, BP, _, _, A1, A2, FRQ, effect, SE, P in GWAS_chnk:
            liftover.liftover_check(SNP, GWAS_set, chnk_num)
            reference_check.reference_check(SNP, BP, A1, A2, FRQ, effect, GWAS_set, chnk_num)
    except:
        logger.error(sys.exc_info())
        logger.error('during parseRsmerge at chunk {}, at SNP {}, at row {}'.format(chnk_num, SNP, i))


def get_stats():
    # write stats about procedures to log file
    logger.info('number of liftovers: {}'.format(liftover.liftover_sum))
    logger.info('number of no hits in SNPArch: {}'.format(liftover.nohit_sum))
    logger.info('number of no hits with 1000genome reference {}'.format(reference_check.no_match_sum))
    logger.info('number of switched alleles {}'.format(reference_check.frq_switch_sum))