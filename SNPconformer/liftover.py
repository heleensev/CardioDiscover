from UnqWrap import DbQuerier
from humantime import get_time
import logging ,sys

collection = DbQuerier.Collection
GWAS = ""
liftover_sum = 0
nohit_sum = 0
logger = logging.getLogger(__name__)

def init_collection():
    global collection
    collection = DbQuerier('../DB/GWAS').db_collection('SNPliftover')

def liftover_check(SNP, gwas_set, chk_num):

    global collection
    global liftover_sum, nohit_sum
    logger.info('initiating SNP conformer at {}'.format(get_time()))
    try:
        match = collection.fetch('rs_low', SNP)
        if match:
            entry = match[0]
            rs_cur = entry.get('rs_cur')
            if rs_cur != SNP:
                gwas_set.replace(SNP, rs_cur, inplace=True)
                liftover_sum += 1
            else:
                # log or not?
                pass
        else:
            nohit_sum += 1
    except:
        logger.error(sys.exc_info())
        logger.error('during liftover at chunk {}, at row {}'.format(chk_num, SNP))





