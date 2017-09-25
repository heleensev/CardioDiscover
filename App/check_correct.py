#check datatypes in all columns
import re, logging
from App import glob

logger = logging.getLogger(__name__)

row_errors = dict()

def init_check_correct(InputFile):
    type_checker(InputFile)


def type_checker(InputFile):
    # get filename from old (UncheckedFile) file object
    filename = InputFile.filename
    # set headers in classify_columns
    headers = InputFile.headers
    # create new file object, contains attributes for the processed output file
    CheckedFile = glob.CheckedFile(filename)

    disposed = InputFile.disposed
    # for header in headers of InputFile except for the disposed columns
    for head in [x for i, x in enumerate(headers) if i not in disposed]:
        df = InputFile.file_to_df(cols=head)
        df = check_vals(df, head)
        CheckedFile.writedf_to_file(df, header=head)


def check_vals(df, head):

    global row_errors

    #check if rs prefex is present
    def rs_check():
        cur_val = val
        if not match.group(1):
            new_val = 'rs{}'.format(cur_val)
            return new_val

    def chr_check():
        cur_val = val
        pass

    def pb_check():
        pass

    def allele_check():
        pass

    def freq_check():
        pass

    def beta_check():
        pass

    def se_check():
        pass

    def slide_check(row):
        pass

    col_types = {'marker_original': ['rs_check', '(^((rs)[ _-]?)|^)\d+'],
                 'CHR': ['chr_check', '[1-22]|[XY]'],
                 'BP': ['bp_check', '\d+'],
                 'effect_allele': ['allele', '[ATCGDI]{1}'],
                 'non_effect_allele': ['allele', '[ATCGDI]{1}'],
                 'major_allele': ['allele', '[ATCGDI]{1}'],
                 'minor_allele': ['allele', '[ATCGDI]{1}'],
                 'allele': ['allele', '[ATCGDI]{1}'],
                 'freq': ['freq_check','(0)*\.\d*'],
                 'A1_freq': ['freq_check','(0)*\.\d*'],
                 'A2_freq': ['freq_check','(0)*\.\d*'],
                 'Beta': ['beta_check','\d*\.\d\?*(E)?-?\d*'],
                 'SE': ['se_check','\d*\.\d\?*(E)?-?\d*'],
                 'sample': ['sample_check','[0-10000]'],
                 'P': ['pval_check','\d*\.\d\?*(E)?-?\d*'],
                 'control': ['control_check','[0-10000]']}
                 #'info': '\w'}

    disposed_vals = {"marker_original": [],
                     "CHR": [],
                     "BP": [],
                     "effect_allele": []}
    column = df[head]
    pattern = col_types.get(head)[0]

    for i, val in enumerate(column):
        valPattern = re.compile(r'(\s)*{}(\s)*'.format(pattern), re.I)
        match = valPattern.match(val)
        if match:
            if ' ' in val:
                df.replace(val, val.strip)
            if col_types.get(head)[1]:
                #col_types.get(head)[1](val, match)
                pass

            continue
        else:
            df.replace(val, None)
            # count number of errors for one row in a dictionary
            row_errors[str(i)] = row_errors.get(str(i), 0) + 1
            #delete entire row
    return df




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