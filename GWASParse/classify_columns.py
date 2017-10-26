#Module for automatic check on datatypes in the individual columns
import re, logging
import GWASParse.usr_classify_columns as usr_check

logger = logging.getLogger(__name__)
InputFile = object()
header_num = int()
identical = 0

col_types = [['SNP', '(snp)|(marker[ -_]?(name)?)|(rs[ _-]?(id))', '((rs[ _-]?)?\d+)|'
              '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)'],
             ['CHR', '(ch(r)?(omosome)?)', '[1-22]|[XY]'],
             ['BP', '(pos)|(loc(ation)?)|(bp)|(hg(\d){2})|(grch(\d){2})', '\d+'],
             ['Allele', '(allele(s)?)?(A([12_-]|$))?[12]?', '[ACTGDI]{1}($|(\s))'],
             ['FRQ', '([12][ _-]?)?fr(e)?q(uency)?([ _-]?[\w])?', '(\d)*(\.)(\d)*(E)?(-)?(\d)*'],
             ['Effect', '(beta)|(effect)|(OR)|odds[ _-]?ratio', '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['SE', '(se)|(std(\w)*)|((standard( -_)?)?error)', '(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['Control', 'control', '[0-1000000]'],
             ['Case', '(N)|(studies)|(case)', '[0-1000000]'],
             ['P', 'p([ _-])?\.?(val)?(ue)?', '(\d)*(\.)(\d)*(E(-)?)?(\d)*']]


def init_classifier(file):
    # InputFile is file object in config
    global InputFile
    InputFile = file
    headers, dispose = header_IDer()
    headers = check_essential(headers)
    # set new attribute headers, and columns to skip
    InputFile.headers = headers
    InputFile.skip = dispose


def header_IDer():

    global InputFile

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

    # transform first line of the csv to a DataFrame, to determine the headers
    df = InputFile.file_to_df(chsize=1)
    headers = df.columns.values.tolist()
    global header_num
    header_num = len(headers)
    dispose = list()

    # loop over all columns to determine the information type
    for i, header in enumerate(headers):
        print(i)
        # get a chunk of the column to perform the check (for memory efficiency)
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
                    # replace old header in list with new header
                    headers[i] = new_header
                    # break loop when column is identified
                    break
        else:
            dispose.append(i)
    print(headers)
    return headers, dispose


def identical_increment():
    # count occurrences of identical patterns for header and values
    # implies headers are missing from the input file
    global InputFile
    global identical
    identical += 1
    # if the total occurrences are more than 5, set headers to None, set names to a list filled with zeroes
    # these attributes of the UncheckedFile object, used to read the dataframe correctly in 'check_correct'
    if identical > 5:
        InputFile.headers = None
        InputFile.names = [0 for _ in range(header_num)]


def col_check(df, header, rehead, recol, head=False, col=False, result=False):

    hdPattern = re.compile(r'(\s|^)(\w*[ -_])?({})+([ -_]\w*)?(\s|$)'.format(rehead), re.I)
    colPattern = re.compile(r'(\s|^)(\w*[ -_])?({})+([ _-]\w*[ -_])?(\s|$)'.format(recol), re.I)

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


def check_essential(headers):
    global InputFile
    #required headers for the input GWAS file
    required = ['SNP', 'CHR', 'BP', 'A1',
                'A2', 'FRQ', 'Effect', 'P', 'SE']
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
                raise ValueError
    except ValueError:
        # if essential header is not identified, user input is required
        usr_headers = usr_check.init_usr_check(InputFile)
        # after user input, check again for essential headers
        check_essential(usr_headers, InputFile)

    return headers


