#check datatypes in all columns
import re, logging
from App import glob

logger = logging.getLogger(__name__)

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
    for head in [x for i,x in enumerate(headers) if i not in disposed]:
        df = InputFile.file_to_df(cols=head)
        df = check_vals(df, head)
        CheckedFile.writedf_to_file(df, header=head)


def check_vals(df, head):

    col_types = {'marker_original': ['check_rs_vals', '((rs)[ _-]?)?\d+'],
                 'CHR': ['check_vals', '[1-22]|[XY]'],
                 'BP': ['check_vals', '\d+'],
                 'effect_allele': ['check_vals', '[ATCGDI]{1}'],
                 'non_effect_allele': ['check_vals', '[ATCGDI]{1}'],
                 'major_allele': ['check_vals', '[ATCGDI]{1}'],
                 'minor_allele': ['check_vals', '[ATCGDI]{1}'],
                 'allele': ['check_vals', '[ATCGDI]{1}'],
                 'freq': '(0)*\.\d*',
                 'A1_freq': '(0)*\.\d*',
                 'A2_freq': '(0)*\.\d*',
                 'Beta': '\d*\.\d\?*(E)?-?\d*',
                 'SE': '\d*\.\d\?*(E)?-?\d*',
                 'sample': '[0-10000]',
                 'P': '\d*\.\d\?*(E)?-?\d*',
                 'control': '[0-10000]',
                 'info': '\w'}

    disposed_vals = {"marker_original": [],
                     "CHR": [],
                     "BP": [],
                     "effect_allele": []}
    column = df[head]
    pattern = col_types.get(head)[0]

    for val in column:
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
