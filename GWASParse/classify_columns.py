# Module for automatic check on datatypes in the individual columns
import re
import logging
import traceback
import GWASParse.usr_classify_columns as usr_check
from DataFrameHandler import chunker

logger = logging.getLogger(__name__)
studyID = str
path = str
sep = str
identical = 0

col_types = [['SNP', '(snp)|(marker[ -_]?(name)?)|(rs[ _-]?(id))', '((rs[ _-]?)?\d+)|'
              '((chr)?\d{1,2}\:(\d)+)'],
             ['CHR', '(ch(r)?(omosome)?)', '[1-26]|[XY]'],
             ['BP', '((pos)|(loc(ation)?)|(bp)|(hg(\d){2})|(grch(\d){2}))', '\d+'],
             ['Allele', '(allele)|(A)[-_ ]?[12]?', '[ACTG]+|[RDI]?|[1234]?'],
             ['FRQ', '([12][ _-]?)?fr(e)?q(uency)?([ _-]?[\w])?', '(\d)*(\.)(\d)*(E)?(-)?(\d)*'],
             ['Effect', '(beta)|(effect)|(OR)|odds[ _-]?ratio', '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['SE', '(se)|(std(\w)*)|((standard( -_)?)?error)', '(\d)*(\.)(\d)*(E(-)?)?(\d)*'],
             ['Control', 'control', '^[0-1000000]+$'],
             ['Case', '(^N([ _-]\w*)?)|(studies)|(case)', '[0-1000000]+'],
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

    def allele_check():
        new_header = dup_vals_check('Allele', ['A1', 'A2'])
        if new_header:
            return new_header

    # check and correction for values that are allowed to be duplicate in the headers (i.e: allele)
    def dup_vals_check(val, dup_vals):
        # if the current column name from col_types in the loop matches Allele
        if col[0] == val:
            if dup_vals[0] not in new_headers:
                new_head = dup_vals[0]
            elif dup_vals[1] not in new_headers:
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
            if new_header in ['FRQ', 'P', 'SE']:
                raise Exception('throw_out_duplicate')
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
        try:
            df_chunk = df[header]
            for c, col in enumerate(col_types):
                if col_check(df_chunk, header, col[1], col[2]):
                    new_header = col[0]
                    # call duplicate check for duplicate headers
                    if new_header == 'Allele':
                        new_header = allele_check()
                        new_headers.append(new_header)
                        header_idx.append(i)
                        break
                    elif duplicate_check():
                        # replace old header in list with new header
                        new_headers.append(new_header)
                        header_idx.append(i)
                        # break loop when column is identified
                        break
            else:
                # if no valid header match found for the column, dispose column
                dispose.append(header)

        except Exception as e:
            if e == 'throw_out_duplicate':
                continue
            print(traceback.format_exc())
            logger.error(traceback.format_exc())
            check_essential([])

    logger.info('for study {}, disposed columns: {}'.format(studyID, ''.join(dispose)))
    return new_headers, header_idx


def col_check(df, header, re_head, re_row, head=False, row=False, result=False):

    hd_pattern = re.compile(r'(\s|^)(\w*[ -_])?{}\Z([ -_]\w*)?(\s|$)'.format(re_head), re.I)
    row_pattern = re.compile(r'(\s+|^)({})\Z(\s+|$)'.format(re_row), re.I)

    # if 20 of 25 values match the column pattern, the type is confirmed
    cnt = 0
    for row, val in df.iteritems():
        val = str(val)
        if row_pattern.match(val):
            cnt += 1
    if cnt > 20:
        row = True
    # if the column header matches the header pattern, the header is confirmed
    if hd_pattern.match(header):
        head = True
    # if the type is confirmed, but not the header, header may actually  be a row value
    # implies header is missing from the input file, call identical_increment to count occurrences
    elif row and row_pattern.match(header):
        raise Exception('Header missing for column, continuing to user_classify_columns')
    # if header or column matches with the pattern, header is confirmed
    if head and row:
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
        print(headers)
        print(studyID)
        # if essential header is not identified, user input is required
        usr_headers = usr_check.init_usr_check(path)
        # after user input, check again for essential headers
        check_essential(usr_headers)
    except Exception as e:
        logger.error(e)

    return headers
