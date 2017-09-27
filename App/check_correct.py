#check datatypes in all columns
import re, logging, numpy
from App import glob

logger = logging.getLogger(__name__)

row_errors = dict()

col_types = {'SNP': ['((rs[ _-]?)?\d+)|'
                     '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)', 'rs_check'],
             'CHR': ['(\d){1,2}|[XY]', 'chr_check'],
             'BP': ['\d{10}', 'bp_check'],
             'effect_allele': ['[ATCGDI]{1}', 'allele_check'],
             'non_effect_allele': ['[ATCGDI]{1}', 'allele_check'],
             'major_allele': ['allele', '[ATCGDI]{1}'],
             'minor_allele': ['allele', '[ATCGDI]{1}'],
             'Allele': ['allele', '[ATCGDI]{1}'],
             'FRQ': ['freq_check', '(0)*\.\d*'],
             'A1_freq': ['freq_check', '(0)*\.\d*'],
             'A2_freq': ['freq_check', '(0)*\.\d*'],
             'Beta': ['beta_check', '\d*\.\d\?*(E)?-?\d*'],
             'SE': ['se_check', '\d*\.\d\?*(E)?-?\d*'],
             'sample': ['sample_check', '[0-10000]'],
             'P': ['pval_check', '\d*\.\d\?*(E)?-?\d*'],
             'control': ['control_check', '[0-10000]']}

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

    disposed = CheckedFile.dispose
    # for header in headers of InputFile except for the disposed columns
    for n, head in enumerate([x for i, x in enumerate(headers) if i not in disposed]):
        df = InputFile.file_to_dfcol(cols=[n])
        df = check_vals(df, n, head)
        CheckedFile.writedf_to_file(df, header=head)

def slide_check():

    for row_index in row_errors:
        if row_errors.get(row_index) > 1:
            pass


def check_vals(df, n, head):

    global row_errors

    def rs_check():
        # check if rs prefix is present, if not, return concatenated value
        cur_val = val
        if match.group(2) and not match.group(3):
            new_val = 'rs{}'.format(cur_val)
            return new_val
        # if SNP pattern matches with BED format, insert into BED column
        elif match.group(4):
            df.iloc[i, n+1] = match.group(4)
            return False

    def chr_check():
        # check if autosomal chromosome number is no higher than 22
        cur_val = val
        if isinstance(cur_val, int) and cur_val > 22:
            return False

    # check if human base pair number is no higher than 3,3 billion
    def bp_check():
        cur_val = val
        bp_human_genome = 3300000000
        if cur_val > bp_human_genome:
            return False
    #
    def allele_check():
        pass

    def freq_check():
        pass

    def beta_check():
        pass

    def se_check():
        pass

    disposed_vals = {"marker_original": [],
                     "CHR": [],
                     "BP": [],
                     "effect_allele": []}
    check_funcs = {'rs_check': rs_check, 'chr_check': chr_check,
                   'bp_check': bp_check, 'allele_check': allele_check,
                   'freq_check': freq_check, 'beta_check': beta_check,
                   'se_check': se_check}

    column = head
    if column == 'SNP':
        # create extra column for values in BED format in SNP column
        #df.insert(n, 'BED', None)
        df['BED'] = None

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
                    passed = str(numpy.NaN)
            else:
                continue
            df.replace(str(val), passed)
        else:
            df.replace(str(val), str(numpy.NaN))
            # count number of errors for one row in a dictionary
            row_errors[str(i)] = row_errors.get(str(i), 0) + 1

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