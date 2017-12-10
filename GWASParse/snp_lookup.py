# module for checking if SNPid is present in dbSNP/dbVar
import requests
from bs4 import BeautifulSoup as BS
from pyliftover import LiftOver

chains = {18: '', 19: '', 38: '38'}


def liftover_loc(study, loc):

    def liftover():
        lo = LiftOver(chain)
        con_pos = lo.convert_coordinate(*floc)[0]
        if con_pos:
            return con_pos[0][0], con_pos[0][1]

    rs_id = str
    floc = [loc.split(':')[0], loc.split(':')[1]]
    if study.build:
        chain = chains.get(study.build)
        if study.build != '38':
            floc[0] = 'chr{}'.format(loc.split(':')[0])
            floc = liftover()
        rs_id = query_loc(*floc)
        return rs_id, floc
    else:
        return False


def query_loc(chr, bp):

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' \
          'esearch.fcgi?db=snp&term={}[Base%20position]{}' \
          '[Chromosome]&term%22Homo+sapiens%22[Organism]'

    result = None
    go = True
    tries = 0
    while go and tries < 20:
        try:
            resp = requests.get(url.format(bp, chr))
            go = False
        except requests.RequestException:
            tries += 1
            continue
    if resp:
        xml = resp.text
        if xml:
            soup = BS(xml, 'lxml')
            idlist = soup.find_all('idlist')
            if idlist:
                hit = idlist[0].id
                if hit:
                    result = hit
    return result
