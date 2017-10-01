#Module for automatic check on datatypes in the individual columns
import re, logging
import pandas as pd
from App import config
import App.usr_classify_columns as usr_check

logger = logging.getLogger(__name__)
MutableFile = object()
header_num = int()
identical = 0

col_types = [['SNP', '(snp)|(marker[ -_]?(name)?)|(rs[ _-]?(id))', '((rs[ _-]?)?\d+)|'
              '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)'],
             ['CHR', '(ch(r)?(omosome)?)', '[1-22]|[XY]'],
             ['BP', '(.*[ _-]?((pos)|(loc(ation)?))|(bp)+($|[ _-]))|(hg(\d){2})|(grch(\d){2})', '\d+'],
             ['Allele', '(allele(s)?)?(A([12_-]|$))?[12]?', '[ACTGDI]{1}($|(\s))'],
             ['FRQ', '(([12][ _-]?)?fr(e)?q(uency)?([ _-]?[\w])?)', '\d*\.\d\?*(E)?-?\d*'],
             ['Effect', '(beta)|(effect)|(OR)|odds[ _-]?ratio', '(-)?\d*\.\d\?*(E)?-?\d*'],
             ['SE', '(se)|(std)', '\d*\.\d\?*(E)?-?\d*'],
             ['control', 'control', '[0-10000]'],
             ['case', '((n[ _-]?))?(studies)|(case)|$', '[0-10000]'],
             ['P', 'p([ _-])?\.?(val)?(ue)?', '\d*\.\d\?*(E)?-?\d*']]


def init_classifier(InputFile):
    global MutableFile
    MutableFile = InputFile
    headers, dispose = header_IDer(InputFile)
    headers = check_essential(headers, InputFile)
    #set new attribute headers, and columns to skip
    MutableFile.headers = headers
    MutableFile.skip = dispose


def header_IDer(InputFile):

    def allele_check():
        new_header = dup_vals_check('Allele', ['A1', 'A2'])
        if new_header:
            return new_header

    def freq_check():
        new_header = dup_vals_check('FRQ', ['FRQ1', 'FRQ2'])
        if new_header:
            return new_header

    # check and correction for values that are allowed to be duplicate in the headers (i.e: allele and freq)
    def dup_vals_check(val, dup_vals):
        # if the current column name from col_types in the loop matches FRQ or Allele
        if col[0] == val:
            if header in dup_vals:
                return header
            if dup_vals[0] in headers:
                new_header = dup_vals[1]
            else:
                new_header = dup_vals[0]
            return new_header

    def duplicate_check():
        try:
            # if header is already in the headers list (for header in headers list except current header)
            # headers minus current evaluated value
            headers_min_cur = [x for n, x in enumerate(headers) if n != i]
            if col[0] in headers_min_cur:
                print(header)
                raise ValueError
            else:
                return True
        except ValueError:
            # if duplicate header is not allele, let user check the columns
            usr_headers = usr_check.init_usr_check(InputFile)
            check_essential(usr_headers, InputFile)

    #hope python knows this is an class object
    df = InputFile.file_to_df(chsize=1)
    # if df == pd.DataFrame:
    #     print("true")
    # elif df.size
    headers = df.columns.values.tolist()
    global header_num
    header_num = len(headers)
    dispose = list()

    #retourneer originele headers, check of er headers in het input bestand staan, en dan?
    for i, header in enumerate(headers):
        print(i)
        df = InputFile.file_to_df(cols=[i], chsize=25)
        for c, col in enumerate(col_types):
            if col_check(df, header, col[1], col[2]):
                new_header = col[0]
                # call duplicate check for duplicate headers
                if duplicate_check():
                    if allele_check():
                        new_header = allele_check()
                    elif freq_check():
                        new_header = freq_check()
                    headers[i] = new_header
                    break
        else:
            dispose.append(i)
    print(headers)
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


def col_check(df, header, rehead, recol, head=False, col=False, result=False):

    hdPattern = re.compile(r'(\s|^)({})(\s|$)'.format(rehead), re.I)
    colPattern = re.compile(r'(\s|^)({})(\s|$)'.format(recol), re.I)

    # if 20 of 25 values match the column pattern, the type is confirmed
    cnt = 0
    for row, val in df.itertuples():
        val = str(val)
        if colPattern.match(val):
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
    if head and col:
        result = True

    return result


def check_essential(headers, file):
    #required headers for the input GWAS file
    required = ['SNP', 'CHR', 'BP', 'A1',
                'A2', 'FRQ[12]?', 'Effect', 'P', 'SE']
    for head in headers:
        print(head)
    try:
        for req in required:
            match = False
            for head in headers:
                hdPattern = re.compile(r'{}'.format(req))
                if hdPattern.match(head):
                    match = True
            if not match:
                #if essential header is not identified, user input is required
                raise ValueError
    except ValueError:
        usr_headers = usr_check.init_usr_check(file)
        check_essential(usr_headers, file)
        print("blabla")

    return headers

"""notes to self: headers not being replaced anymore

    Todo: make a todolist, think of something for sliding columns, and other thing"""

