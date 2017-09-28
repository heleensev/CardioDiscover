#check datatypes in all columns
import re, logging
import numpy as np
import pandas as pd
from App import glob

logger = logging.getLogger(__name__)

row_errors = dict()

col_types = {'SNP': '((rs[ _-]?)?\d+)|'
             '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)',
             'CHR': '(\d){1,2}|[XY]',
             'BP': '\d{10}',
             'A1': '[ATCGDI]{1}',
             'A2': '[ATCGDI]{1}',
             'FRQ': '(0)*\.\d*',
             'FRQ1': '(0)*\.\d*',
             'FRQ2': '(0)*\.\d*',
             'Effect': '\d*\.\d\?*(E)?-?\d*',
             'SE': '\d*\.\d\?*(E)?-?\d*',
             'P': '\d*\.\d\?*(E)?-?\d*',
             'case': '[0-10000]',
             'control': '[0-10000]'}

def init_check_correct(InputFile):
    type_checker(InputFile)


def type_checker(InputFile):
    # get filename from old (UncheckedFile) file object
    filename = InputFile.filename
    # set headers in classify_columns
    headers = InputFile.headers
    #columns to skip
    disposed = InputFile.skip
    # create new file object, contains attributes for the processed output file
    CheckedFile = glob.CheckedFile(filename, disposed)
    # disposed columns
    disposed = CheckedFile.dispose
    # csv_names
    csv_names = list()
    # all columns without disposed columns
    headers = [x for i, x in enumerate(headers) if i not in disposed]
    # for header in headers of InputFile except for the disposed columns
    for n, head in enumerate(headers):
        print(n)
        df = InputFile.file_to_dfcol(cols=[n])
        df, head = check_vals(df, n, head)
        CheckedFile.writedf_to_file(df=df, header=head)
        csv_names.append('{}.csv'.format(head))

def check_vals(df, n, head):

    global row_errors
    df_BED = None

    def rs_check():
        # check if rs prefix is present, if not, return concatenated value
        cur_val = val
        if match.group(2) and not match.group(3):
            new_val = 'rs{}'.format(cur_val)
            return new_val
        # if SNP pattern matches with BED format, insert into BED column
        elif match.group(4):
            df_BED.iloc[i] = match.group(4)
            return False

    def chr_check():
        # check if autosomal chromosome number is no higher than 22
        cur_val = val
        if isinstance(cur_val, int) and cur_val > 22:
            return False
        else:
            return True

    # check if human base pair number is no higher than 3,3 billion
    def bp_check():
        cur_val = val
        bp_human_genome = 3300000000
        if cur_val > bp_human_genome:
            return False
        else:
            return True

    def allele_check():
        return True

    def freq_check():
        return True

    def effect_check():
        #check for beta val or odds ratio, minus
        return True

    def pval_check():
        return True

    def se_check():
        return True

    def sample_control_check():
        return True

    disposed_vals = {"marker_original": [],
                     "CHR": [],
                     "BP": [],
                     "effect_allele": []}

    check_funcs = {'SNP': rs_check, 'CHR': chr_check, 'BP': bp_check, 'A1': allele_check,
                   'A2': allele_check(), 'FRQ1': freq_check, 'FRQ2': freq_check,
                   'Effect': effect_check, 'P': pval_check, 'SE': se_check,
                   'control': sample_control_check(), 'case': sample_control_check}

    column = head
    if column == 'SNP':
        # create extra column for values in BED format in SNP column
        #df.insert(n, 'BED', None)
        nan_values = [np.NaN for i in df.itertuples()]
        df_BED = pd.DataFrame({'BED': nan_values})

    pattern = col_types.get(head)[0]

    for i, (row, val) in enumerate(df.itertuples()):
        val = str(val)
        # value may start or end with white space, case insensitive
        valPattern = re.compile(r'(\s|^){}(\s|$)'.format(pattern), re.I)
        match = valPattern.match(val)
        if match:
            if ' ' in val:
                val = val.strip()
                #df.replace(val, val.strip)
            if col_types.get(head)[1]:
                passed = check_funcs.get((col_types.get(head)[1]))()
                if not passed:
                    passed = str(np.NaN)
            else:
                continue
            df.replace(str(val), passed)
        else:
            df.replace(str(val), str(np.NaN))
            # count number of errors for one row in a dictionary
            row_errors[str(i)] = row_errors.get(str(i), 0) + 1

    if column == 'SNP':
        df = df.append(df_BED)
        head = [head, 'BED']

    return df, head




    # if BED_format:
    #     process_BED()

# def process_BED():
#
# def check_rs(val, match):
#     if match.group(1):
#         str(val).lstrip('rs')
#
#
# def check_loc():
#
# def check_allele():
#
# def check P_value():

#def check

"""note to self: fixed regex bugs with - values, work with dispose and headers from InputFile in this script
    fix chromosome col regex, [1-22] not correct"""