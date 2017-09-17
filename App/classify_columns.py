#Module for automatic check on datatypes in the individual columns
import re
import App.check_correct as checker
import App.config as glob
import App.usr_classify_columns as usr_check
allele_cnt = 0


def init_classifier(file):
    headers, df = header_IDer(file)
    headers = check_essential(headers, file)

    return headers


def header_IDer(file):
    # noinspection PyTypeChecker
    col_types = [['marker_original', '(snp)|(marker[ -_]?(name)?)|(rs[ _-]?(id))', '((rs)[ _-]?)?\d+'],
                 ['CHR', '(ch(r)?(omosome)?)', '[1-22]|[XY]'],
                 ['BP', '(((pos)|(loc)|(bp))($)|([ _-]))?(hg(\d){2})?(grch(\d){2})*', '\d+'],
                 ['effect_allele', '((effect)|(ef)|(risk)|(aff)', '[ATCGDI]{1}'],
                 ['non_effect_allele', 'non[-_ ]effect|(un[ _-]?aff)', '[ATCGDI]{1}'],
                 ['major_allele', 'major', '[ATCGDI]{1}'],
                 ['minor_allele', 'minor', '[ATCGDI]{1}']
                 ['allele', '(allele(s)?)?(A([12_-]|$))?[12]?','[ACTGDI]{1}'],
                 ['freq', '(([12][ _-]?)?fr(e)?q(uency)?([ _-]?[12])?)', '(0)*\.\d*'], 
                 ['A1_freq', '((((effect)|(major))[ _-]?)fr(e)?q)?(EAF)?', '(0)*\.\d*'],
                 ['A2_freq', '((((non[ -_]?effect)|(minor))[ _-]?)fr(e)?q)?(MAF)?', '(0)*\.\d*'],  
                 ['Beta', '(beta)?(effect)?(OR)?', '\d*\.\d\?*(E)?-?\d*'],
                 ['SE', '(se)?(std)?', '\d*\.\d\?*(E)?-?\d*'], 
                 ['sample', '((n[ _-]?)$)?(studies)?(case)?', '[0-10000]'],
                 ['P', 'p([ _-])?(val)?(ue)?', '\d*\.\d\?*(E)?-?\d*'],
                 ['control', 'control', '[0-10000]'],
                 ['info', '(info)|(annot)', '\w']]
    #hope python knows this is an class object
    df = file.file_to_df(chsize=6)

    headers = df.headers.values.tolist()
    for i, header in enumerate(headers):
        df = file.filetodf(cols=i)
        while True:
            for c, col in enumerate(col_types):
                if col_check(df):
                    if col[0] in [x for i, x in enumerate(headers) if i != c]:
                        continue
                    if col[0] == 'allele':
                        if 'A1' in headers:
                            headers[i] = 'A2'
                        elif 'A2'in headers:
                            continue
                        else:
                            headers[i] = 'A1'
                    headers[i] = col[0]
                    break
            break

    return headers, df


def col_check(df, rehead, recol, head= False, col= False):
    if df.headers:
        header = df.headers
        hdPattern = re.compile(r'{}'.format(rehead), re.I)
        if hdPattern.match(header):
            head = True
    cnt = 0
    colPattern = re.compile(r'(\s)*{}(\s)*'.format(recol), re.I)
    for row in df.tolist():
        if colPattern.match(row):
            cnt += 1
    if cnt > 20:
        col = True
    if head or col:
        checker(df, head)
        return True
    else:
        return False

def check_essential(headers, file):
    #required headers for the input GWAS file
    required = ['marker_original', 'CHR', 'BP', '(effect)|(major)|(A1)',
                '(non_effect)|(minor)|(A2)', 'freq', 'Beta', 'P']

    match = False
    for req in required:
        for head in headers:
            hdPattern = re.compile(r'{}'.format(req))
            if hdPattern.match(head):
                match = True
        if not match:
            #if essential header is not identified, user input is required
            headers = usr_check.init_usr_check(file)
            break
        else:
            match = False

    return headers

