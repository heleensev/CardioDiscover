from timebuddy import get_time
import redis
import logging ,sys

snp_db = redis.StrictRedis(db=1)
GWAS = ""
liftover_sum = 0
nohit_sum = 0
logger = logging.getLogger(__name__)

def liftover_check(SNP, gwas_set, chk_num):
    global liftover_sum, nohit_sum
    logger.info('initiating SNP conformer at {}'.format(get_time()))

    try:
        match = snp_db.execute_command('JSON.GET', SNP)
        if match:
            entry = match.decode()
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
