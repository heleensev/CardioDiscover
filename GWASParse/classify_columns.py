# Module for automatic check on datatypes in the individual columns
import re, logging
import GWASParse.usr_classify_columns as usr_check
from DataFrameHandler import chunker

logger = logging.getLogger(__name__)
studyID = str
path = str
sep = str
identical = 0

col_types = [['SNP', '(snp)|(marker[ -_]?(name)?)|(rs[ _-]?(id))', '((rs[ _-]?)?\d+)|'
              '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)'],
             ['CHR', '(ch(r)?(omosome)?)', '[1-26]|[XY]'],
             ['BP', '(pos)|(loc(ation)?)|(bp)|(hg(\d){2})|(grch(\d){2})', '\d+'],
             ['Allele', '(allele(s)?)?(A([12_-]|$))?[12]?', '[ACTGRDI1234]+($|(\s))'],
             ['FRQ', '([12][ _-]?)?fr(e)?q(uency)?([ _-]?[\w])?', '(\d)*(\.)(\d)*(E)?(-)?(\d)*'],
             ['Effect', '(beta)|(effect)|(OR)|odds[ _-]?ratio', '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['SE', '(se)|(std(\w)*)|((standard( -_)?)?error)', '(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['Control', 'control', '[0-1000000]'],
             ['Case', '(N)|(studies)|(case)', '[0-1000000]'],
             ['P', 'p([ _-])?\.?(val)?(ue)?', '(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['Info', '(info)|(imputation)|(variance)', '(\d)*(\.)(\d)*(E)?(-)?(\d)*']]


def init_classifier(this_study):
    global path, sep, studyID
    # set the global to given study (this_study) file object
    study = this_study
    path = study.get('path')
    sep = study.get('sep')
    studyID = study.get('studyID')

    headers, header_idx = header_IDer()
    check_essential(headers)
    # set new attribute headers, and indices of columns to keep
    study.update({'headers': headers, 'header_idx': header_idx})

    return study


def header_IDer():
    try:
        def allele_check():
            new_header = dup_vals_check('Allele', ['A1', 'A2'])
            if new_header:
                return new_header

        # check and correction for values that are allowed to be duplicate in the headers (i.e: allele)
        def dup_vals_check(val, dup_vals):
            # if the current column name from col_types in the loop matches Allele
            if col[0] == val:
                if dup_vals[0] not in headers:
                    new_head = dup_vals[0]
                elif dup_vals[1] not in headers:
                    new_head = dup_vals[1]
                else:
                    raise Exception('duplicate header found: {}'.format(header))
                return new_head

        def duplicate_check():
            # if header is already in the headers list (for header in headers list except current header)
            # headers minus current evaluated value
            headers_min_cur = [x for n, x in enumerate(headers) if n != i]
            if col[0] in headers_min_cur:
                # more than one frequency may be present in data set, only use first one
                if new_header == 'FRQ':
                    return False
                else:
                    # if the duplicate header is not an allele or a frequency raise error
                    raise Exception('Duplicate header detected, proceeding to user column check')
            else:
                return True

        # transform the csv to a DataFrame, to determine the headers
        # get a chunk of the file to perform the check (for memory efficiency)
        df = chunker.small_chunk(path=path, sep=sep)
        headers = df.columns.values.tolist()

        dispose = list()
        new_headers = list()
        header_idx = list()

        # loop over all columns to determine the information type
        for i, header in enumerate(headers):
            for c, col in enumerate(col_types):
                if col_check(df, header, col[1], col[2]):
                    new_header = col[0]
                    # call duplicate check for duplicate headers
                    if new_header == 'Allele':
                        new_header = allele_check()
                        new_headers.append(new_header)
                        break
                    elif duplicate_check():
                        # replace old header in list with new header
                        new_headers.append(new_header)
                        # break loop when column is identified
                        break
                    header_idx.append(i)
            else:
                # if no valid header match found for the column, dispose column
                dispose.append(header)
        logger.info('for study {}, disposed columns: {}'.format(studyID, ''.join(dispose)))
        return new_headers, header_idx

    except Exception as e:
        logger.error(e)
        check_essential([])


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
    # implies header is missing from the input file, call identical_increment to count occurrences
    elif col and colPattern.match(header):
        raise Exception('Header missing for column, continuing to user_classify_columns')
    # if header or column matches with the pattern, header is confirmed
    if head and col:
        result = True

    return result


def check_essential(headers):
    # required headers for the input GWAS file
    required = ['SNP', 'CHR', 'BP', 'A1',
                'A2', 'FRQ', 'Effect', 'P', 'SE']
    try:
        for req in required:
            match = False
            for head in headers:
                hd_pattern = re.compile(r'{}'.format(req))
                if hd_pattern.match(head):
                    match = True
            if not match:
                raise ValueError
    except ValueError:
        # if essential header is not identified, user input is required
        usr_headers = usr_check.init_usr_check(path)
        # after user input, check again for essential headers
        check_essential(usr_headers)
    except Exception as e:
        logger.error(e)

    return headers
