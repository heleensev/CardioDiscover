#Module for automatic check on datatypes in the individual columns
import re, logging
from App import checker
from App import usr_check
logger = logging.getLogger(__name__)
MutableFile = object()
header_num = int()
identical = 0


def init_classifier(InputFile):
    global MutableFile
    MutableFile = InputFile
    headers, dispose = header_IDer(InputFile)
    headers = check_essential(headers, InputFile)
    #set new attribute headers, and columns to skip
    MutableFile.headers = headers
    MutableFile.skip = dispose


def header_IDer(InputFile):
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
    df = InputFile.file_to_df(chsize=1)
    headers = df.columns.values
    global header_num
    header_num = len(headers)
    dispose = list()

    #retourneer originele headers, check of er headers in het input bestand staan, en dan?
    for i, header in enumerate(headers):
        df = InputFile.filetodf(cols=i, chsize=25)
        while True:
            for c, col in enumerate(col_types):
                if col_check(df, col[1], col[2]):
                    #if header is already in the headers list (for header in headers list except current header)
                    if col[0] in [x for i, x in enumerate(headers) if i != c]:
                        #if that duplicate header is "allele"
                        if col[0] == 'allele' and 'A2' not in headers:
                            if 'A1' in headers:
                                headers[i] = 'A2'
                            else:
                                headers[i] = 'A1'
                        # if duplicate header is not allele, let user check the columns
                        else:
                            headers = usr_check.init_usr_check(InputFile)
                            headers = check_essential(headers, InputFile)
                            return headers
                    headers[i] = col[0]
                else:
                    dispose.append(i)
            break

    return headers, dispose


def identical_increment():
    # count occurrences of identical patterns for header and values
    # implies headers are missing from the input file
    global MutableFile
    global identical
    identical += 1
    # if the total occurrences are more than 5, set headers to None, set names to a list filled with zeroes
    # these attributes of the UncheckedFile object, used to read the dataframe correctly in 'check_correct'
    if identical > 5:
        MutableFile.headers = None
        MutableFile.names = [0 for i in range(header_num)]


def col_check(df, rehead, recol, head= False, col= False):

    header = df.columns.values.tolist()
    hdPattern = re.compile(r'{}'.format(rehead), re.I)
    colPattern = re.compile(r'(\s)*{}(\s)*'.format(recol), re.I)

    # if 20 of 25 values match the column pattern, the type is confirmed
    cnt = 0
    for row in df.tolist():
        if colPattern.match(row):
            cnt += 1
    if cnt > 20:
        col = True
    # if the column header matches the header pattern, the header is confirmed
    if hdPattern.match(header):
        head = True
    # if the type is confirmed, but not the header, header may actually  be a row value
    # implies headers are missing from the input file, call identical_increment to count occurrences
    elif col and colPattern.match(header):
        identical_increment()
    # if header or column matches with the pattern, header is confirmed
    if head or col:
        checker(df, head)
        return True
    else:
        return False

def check_essential(headers, file):
    #required headers for the input GWAS file
    required = ['marker_original', 'CHR', 'BP', '(effect)|(major)|(A1)',
                '(non_effect)|(minor)|(A2)', 'freq', 'Beta', 'P']

    for req in required:
        match = False
        for head in headers:
            hdPattern = re.compile(r'{}'.format(req))
            if hdPattern.match(head):
                match = True
        if not match:
            #if essential header is not identified, user input is required
            headers = usr_check.init_usr_check(file)
            check_essential(headers, file)
            break

    return headers

