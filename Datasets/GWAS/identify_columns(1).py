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
                 ['allele', '(allele)?(A([12_-]|$))?[12]?','[ACTGDI]'],
                 ['Beta','(beta)?(effect)?(OR)?', '\d*\.\d\?*(E)?-?\d*'], 
                 ['SE', '(se)?(std)?', '\d*\.\d\?*(E)?-?\d*'], 
                 ['sample', '((n[ _-]?)$)?(studies)?(case)?', '[0-10000]'],
                 ['control', 'control', '[0-10000]'],
                 ['info', 'info', '\w']]
    
    for i, header in enumerate(headers):
        df = glob.filetodf(cols=i)
        while True:
            for c, check in enumerate(col_types:
                if col_check(df):
                    head = col_types[c][0]
                    break
            break


def col_check(df, rehead, recol, head= False, col= False):
    allele = None
                 
    if df.headers:
        header = df.headers
        hdPattern = re.compile(r'{}'.format(rehead), re.I)
        if hdPattern.match(header):
            if 'allele' in rehead:
                 allele_type(df)
            head = True
    cnt -= 0
    colPattern = re.compile(r'{}'.format(recol), re.I)
    for row in df.tolist():
        if colPattern.match(row):
            cnt += 1
    if cnt > 14:
        col = True

    if head or col:
        checker(df, allel
        return True, allele
    
    else:
         return False, allele
                 
def allele_type():
    
    header = df.columns
    head_type = None
                 
    #allele_types = [['effect_allele', '(effect)?(ef)?(risk)?','[ACTGDI]'],
    #                ['non_effect_allele ','non[-_ ]effect', '[ACTGDI]'] 
    #                ['major_allele', 'major', '[ATCDGI]'], 
    #                ['minor_allele', 'minor', '[ATCDGI]'],
    #                ['A1_freq', '((((effect)|(major))[ _-]?)fr(e)?q)?(EAF)?', '(0)*\.\d*'],
    #                ['A2_freq', '((((non[ -_]?effect)|(minor))[ _-]?)fr(e)?q)?(MAF)?', '(0)*\.\d*'],
    #                ['freq', '(([12][ _-]?)?fr(e)?q(uency)?([ _-]?[12])?)', '(0)*\.\d*']] 
    
    allele_types = [['effect_allele', '((effect)|(ef)|(risk))|(non[-_ ]effect)|(major)|(minor))','[ACTGDI]'],
                    ['A1_freq', '((((effect)|(major))[ _-]?)fr(e)?q)?(EAF)?', '(0)*\.\d*'],
                    ['A2_freq', '((((non[ -_]?effect)|(minor))[ _-]?)fr(e)?q)?(MAF)?', '(0)*\.\d*'],
                    ['freq', '(([12][ _-]?)?fr(e)?q(uency)?([ _-]?[12])?)', '(0)*\.\d*']] 
    if allele_cnt < 2:
        headPattern = re.compile(r'{}'.format(al_type[0][0]), re.I)
        match = headPattern.match(header)
            if match:
                if match.group(1):
                    head_type = 'effect'
                elif match.group(2)
                    head_type = 'non_effect'
                elif match.group(3):
                    head_type = 'minor'
                else:
                    head_type = 'major'
            else:
                if allele_cnt < 1:
                    head_type = 'A1'
                else:
                    head_type = 'A2'
    elif allele_cnt < 4:
        for al_type in allele_types[1:]:
            freqPattern = re.compile(r'{}'.format(al_type[1])
            if freqPattern.match(header):
                head_type = al_type[0]
    else:
        log_file.write("No more options for match with allele\n')
    allele_cnt += 1
                       
    return head_type
   
        
                 
                 
        
        
        