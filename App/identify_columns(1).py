#Module for automatic check on datatypes in the individual columns
import re
import App.check_correct as checker
import App.global_functions as glob

allele_cnt = 0

def init_header_ider():
    header_ider()

def header_ider():

#([(?p<bp>)(?p<pos>)(?p<loc>)]($|[ _-]))?(hg(\d){2})?(grch(\d){2})*
#EAF: effect allele freq, NAF: non-effect allele freq, JAF: major allele freq, MAF: minor allele freq    
    col_types = [['marker_original', '(snp)*(marker(name)*)*(rs(id))*', '[0-9]*'], 
                 ['CHR', '(ch(r)?(omosome)?)', '[1-22]?[XY]?'],
                 ['BP', '(((pos)|(loc)|(bp))($)|([ _-]))?(hg(\d){2})?(grch(\d){2})*', '\d*$'], 
                 ['effect_allele', '((effect)|(ef)|(risk))','[ACTGDI]'],
                 ['non_effect_allele', 'non[-_ ]effect'],
                 ['major_allle', 'major'],
                 ['minor_allele', 'minor']
                 ['allele', '(allele)?(A([12_-]|$))?[12]?','[ACTGDI]'],
                 ['freq', '(([12][ _-]?)?fr(e)?q(uency)?([ _-]?[12])?)', '(0)*\.\d*'], 
                 ['A1_freq', '((((effect)|(major))[ _-]?)fr(e)?q)?(EAF)?', '(0)*\.\d*'],
                 ['A2_freq', '((((non[ -_]?effect)|(minor))[ _-]?)fr(e)?q)?(MAF)?', '(0)*\.\d*'],  
                 ['Beta','(beta)?(effect)?(OR)?', '\d*\.\d\?*(E)?-?\d*'], 
                 ['SE', '(se)?(std)?', '\d*\.\d\?*(E)?-?\d*'], 
                 ['sample', '((n[ _-]?)$)?(studies)?(case)?', '[0-10000]'],
                 ['control', 'control', '[0-10000]'],
                 ['info', 'info', '\w']]
    
    header_bf = list()
    for i, header in enumerate(headers):
        df = glob.filetodf(cols=i)
        while True:
            for c, col in enumerate(col_types):
                if col_check(df):
                    if col[0] == 'allele':
                        if 'A1' in header_bf
                            head = 'A2'
                        elif 'A2'in header_bf:
                            continue
                        else:
                            head = 'A1'
                    head = col_types[c][0]
                    df = checker(df, head)
                    break
            break


def col_check(df, rehead, recol, head= False, col= False):
    allele = None
                 
    if df.headers:
        header = df.headers
        hdPattern = re.compile(r'{}'.format(rehead), re.I)
        if hdPattern.match(header):
            head = True
    cnt -= 0
    colPattern = re.compile(r'{}'.format(recol), re.I)
    for row in df.tolist():
        if colPattern.match(row):
            cnt += 1
    if cnt > 14:
        col = True
    if head or col:
        checker(df, head)
        return True
    else:
         return False
                 
        
        
        