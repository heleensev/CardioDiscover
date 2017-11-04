import pandas as pd
import simplejson as json
import logging, sys
from humantime import get_time
from simplejson.scanner import JSONDecodeError
from MetaReader.config import study
from StatTester import stat_test

info_score, n_studies = False
# the instance of 'study' object currently in the loop
cur_study = object()
logger = logging.getLogger(__name__)

def init_file_reader():
    global cur_study
    logging.basicConfig(filename='../SNP.log', filemode='a', level=logging.DEBUG)

    logger.info('initiating SNP conformer at {}'.format(get_time()))
    # list containing all the 'study' object with meta data as attributes
    files = read_meta()
    for n, study in enumerate(files):
        path = study.get('path')
        read_GWAS(path, 5000)

def read_GWAS(file, chsize):
    logger.info('initiating read_file at {}'.format(get_time()))
    for chnk_num, chunk in enumerate(pd.read_csv(file, chunksize=chsize, header=None, sep='\t')):
        print("entering file {}: chunk: {}".format(file, chnk_num))
        if chnk_num < 1:
            check_headers(chunk)
        iterate_file(chnk_num, GWAS_set=chunk.itertuples(index=True))

def iterate_file(chnk_num, GWAS_set, SNP='SNP', i=0):
    logger.info('initiating iterate_file at {}'.format(get_time()))
    try:
        for i, _, _, _, _, _, _, FRQ, effect, SE, P, *V in GWAS_set:
            stat_test.init_compute(cur_study, FRQ, effect, SE, P, V, chnk_num)
    except:
        logger.error(sys.exc_info())
        logger.error('during parseRsmerge at chunk {}, at SNP {}, at row {}'.format(chnk_num, SNP, i))

def check_headers(first_chunk):
    headers = first_chunk.columns.headers.tolist
    if 'Info' in headers:
        info_score = True
    if 'Case' in headers:
        n_studies = True


