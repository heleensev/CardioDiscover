#check datatypes in all columns, correct if necessary
import re, logging
import numpy as np
import pandas as pd
from Parser import glob

logger = logging.getLogger(__name__)
InputFile = object()
row_errors = dict()
beta_values = int()
col_types = {'SNP': '((rs[ _-]?)?\d+)|'
                    '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)',
             'CHR': '(\d){1,2}|[XY]',
             'BP': '\d{10}',
             'A1': '[ATCGDI]{1}',
             'A2': '[ATCGDI]{1}',
             'FRQ': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'FRQ1': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'FRQ2': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'Effect': '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'SE': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'P': '(\d)*(\.)(\d)*(E)?(-)?(\d)',
             'Case': '[0-1000000]',
             'Control': '[0-1000000]'}


def init_check_correct(file):
    global InputFile
    InputFile = file
    type_checker()


def type_checker():
    global InputFile
    # get filename from old (UncheckedFile) file object
    filename = InputFile.filename
    # set headers in classify_columns
    org_headers = InputFile.headers
    #columns to skip
    disposed = InputFile.skip
    print('disposed: {}'.format(disposed))
    # create new file object, contains attributes for the processed output file
    CheckedFile = glob.CheckedFile(filename, disposed)
    # all column headers without disposed columns
    headers = [x for i, x in enumerate(org_headers) if i not in disposed]
    # for header in headers of InputFile except for the disposed columns
    for head in headers:
        n = org_headers.index(head)
        df = InputFile.file_to_dfcol(head=head, cols=[n])
        df, head = check_vals(df, head)
        CheckedFile.write_to_file(df, head)
    CheckedFile.concat_write()


def check_vals(df, head):
    global InputFile
    global row_errors

    # specific check functions for column type in GWAS
    def rs_check(result=True):
        # check if rs prefix is present, if not, return concatenated value
        cur_val = val
        df_BED = BED
        if not match.group(4):
            new_val = 'rs{}'.format(cur_val.strip())
            return new_val
        # if SNP pattern matches with BED format, insert into BED column
        elif match.group(5):
            df_BED.iloc[i] = match.group(5)
            result = False
        return result

    def chr_check(result=True):
        # check if autosomal chromosome number is no higher than 22
        cur_val = val
        if isinstance(cur_val, int) and cur_val > 23:
            result = False
        elif int(cur_val) == 23:
            #replace with X/Y????
            pass
        return result

    # check if human base pair number is no higher than 3,3 billion
    def bp_check(result=True):
        cur_val = val
        bp_human_genome = 3300000000
        if cur_val > bp_human_genome:
            result = False
        return result

    def allele_check():
        return True

    def freq_check():
        return True

    def effect_check():
        #check for beta val: regression coefficient or odds ratio: exp(beta)
        global beta_values
        if match.group(1):
            beta_values += 1
        return True

    def pval_check():
        return True

    def se_check():
        return True

    def sample_control_check():
        return True

    def effect_type():
        if column == 'effect':
            size = (df.shape[0]) / 2
            if beta_values > size / 100:
                return 'Beta'
            elif beta_values > 0:
                df.replace('(-)(\d)*(\.)', str(np.NaN), regex=True, inplace=True)
                return 'OR'
            else:
                return 'OR'

    def row_errors_append():
        # count number of errors for one row in a dictionary
        row_errors[str(i)] = row_errors.get(str(i), 0) + 1

    # corresponding check functions for the individual headers
    check_funcs = {'SNP': rs_check, 'CHR': chr_check, 'BP': bp_check, 'A1': allele_check,
                   'A2': allele_check, 'FRQ1': freq_check, 'FRQ2': freq_check,
                   'Effect': effect_check, 'P': pval_check, 'SE': se_check,
                   'control': sample_control_check, 'case': sample_control_check}

    column = head
    if column == 'SNP':
        # create extra column for values in BED format in SNP column
        #df.insert(n, 'BED', None)
        nan_values = [np.NaN for i in df.itertuples()]
        BED = pd.DataFrame({'BED': nan_values})

    pattern = col_types.get(head)
    for i, (row, val) in enumerate(df.itertuples()):
        val = str(val)
        # value may start or end with white space, case insensitive
        valPattern = re.compile(r'(\s|^)({})(\s|$)'.format(pattern), re.I)
        match = valPattern.match(val)
        if match:
            # get corresponding check for column type from dict 'check_funcs'
            passed = check_funcs.get(head)()
            # if not passed more stringent check, set value to NaN
            if not passed:
                passed = str(np.NaN)
                row_errors_append()
            else:
                if ' ' in val:
                    passed = val.strip()
                # if no new value is returned, but passed is True, continue to the next item in loop
                elif not isinstance(passed, str):
                    continue
            df.replace(val, passed, inplace=True)
        else:
            # if not matched with general pattern, set value to NaN
            df.replace(val, str(np.NaN), inplace=True)
            row_errors_append()

    if head == 'effect':
        head = effect_type()

    elif column == 'SNP':
        df = df.append(BED)
        head = [head, 'BED']

    return df, head

"""note to self: fixed regex bugs with - values, work with dispose and headers from InputFile in this script
    fix chromosome col regex, [1-22] not correct"""