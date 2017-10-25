from SNPconformer import liftover, SNP1000ref
from humantime import get_time
import pandas as pd
import logging, sys

GWAS = ""
logger = logging.getLogger(__name__)


def init_file_reader():
    logging.basicConfig(filename='../SNP.log', filemode='a', level=logging.DEBUG)

    logger.info('initiating SNP conformer at {}'.format(get_time()))

    # initiate collection object for querying the database
    liftover.init_collection()
    SNP1000ref.init_collection()
    chunk_file(GWAS, 5000)


def chunk_file(file, chsize):
    logger.info('initiating chunk_file at {}'.format(get_time()))
    for chnk_num, chunk in enumerate(pd.read_csv(file, chunksize=chsize, header=None, sep='\t')):
        print("entering file {}: chunk: {}".format(file, i))
        iterate_file(chnk_num, iterable=chunk.itertuples(index=False))


def iterate_file(chnk_num, iterable):
    logger.info('initiating iterate_file at {}'.format(get_time()))
    try:
        for _, _, SNP, BP, _, _, A1, A2, FRQ, effect, SE, P in iterable:
            liftover.liftover_check(SNP, iterable, chnk_num)
            SNP1000ref.orientation_check(SNP, BP, A1, A2, FRQ, chnk_num)
    except:
        logger.error(sys.exc_info())
        logger.error('during parseRsmerge at chunk {}, at row {}'.format(chnk_num, SNP))

