#check datatypes in all columns, correct if necessary
import re, simplejson, logging
import numpy as np
import pandas as pd
from MetaReader.writer import write_meta
from GWASParse import glob

""" GLOBALS """
logger = logging.getLogger(__name__)
# study size to get a sum of the study effect
study_size = int()
# sum of effective size
eff_sum = float()
# object containing attrubutes of the input file
GWASin = object()
# counter for rows with issues, these are dropped from the set
row_errors = dict()
# counter for negative effect values, used to determine if effect
# score is OR or Beta
neg_values = int()
# global variable for info value from first row, used to determine if
# info score is fixed or not
first_info = float()
# boolean to determine if the info score is fixed
info_fixed = True

# patterns for the individual columns that may be present in dataset
col_types = {'SNP': '((rs[ _-]?)?\d+)|'
                    '((chr)?\d{1,2}\:(\d)+(:[ATCGDI])?)',
             'CHR': '(\d){1,2}|[XY]',
             'BP': '\d{10}',
             'A1': '[ATCGRDI]+',
             'A2': '[ATCGRDI]+',
             'FRQ': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'FRQ1': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'Effect': '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'SE': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'P': '(\d)*(\.)(\d)*(E)?(-)?(\d)',
             'Case': '[0-1000000]',
             'Control': '[0-1000000]',
             'Info': '(\d)*(\.)(\d)*(E)?(-)?(\d)*'}


def init_check_correct(file, study):
    global GWASin
    global study_size
    study_size = study.study_size
    GWASin = file
    type_checker()
    # get additional meta data about study
    add_meta = get_meta_items()
    return add_meta


def type_checker():
    global GWASin
    # get filename from old (UncheckedFile) file object
    filename = GWASin.filename
    # set headers in classify_columns
    org_headers = GWASin.headers
    # columns to skip in check and csv writing
    disposed = GWASin.skip
    print('disposed: {}'.format(disposed))
    # create new file object, contains attributes for the processed output file
    GWASout = glob.CheckedFile(filename, disposed)
    # all column headers without disposed columns
    headers = [x for i, x in enumerate(org_headers) if i not in disposed]
    # for header in headers of GWASin except for the disposed columns
    for head in headers:
        n = org_headers.index(head)
        df = GWASin.file_to_dfcol(head=head, cols=[n])
        df, head = check_vals(df, head)
        # write checked column to a temporary file
        GWASout.write_to_file(df, head)

    # write temporary files (columns) to one csv file
    GWASout.concat_write()


def get_meta_items():
    # should be adding attribute to the object
    # add to meta data file if info score is present and fixed or not
    if info_fixed:
        if first_info:
            info = first_info
        else:
            info = 'NONE'
    else:
        info = 'VARIABLE'

    return {'info_score': info, 'sum_effective_size': eff_sum}


def check_vals(df, head):
    global GWASin, row_errors
    BED = pd.DataFrame

    def head_operation():
        # check if SNP column: add BED column
        global BED, first_info
        if head == 'SNP':
            # create extra column for values in BED format in SNP column
            nan_values = [np.NaN for _ in df.itertuples()]
            BED = pd.DataFrame({'BED': nan_values})
        # get the info score of the first row
        if head == 'Info':
            first_info= float(df.iloc[0])

    def tail_operation():
        global head, df
        # check if current header is 'effect', determine the type of unit
        if head == 'effect':
            effect_type()
        elif head == 'SNP':
            df = df.append(BED)
            head = [head, 'BED']

    # specific check functions for column type in GWAS
    def rs_check(result=True):
        # check if rs prefix is present, if not, return concatenated value
        cur_val = val
        df_BED = BED
        # if SNP pattern matches with BED format, insert into BED column
        if match.group(5):
            df_BED.iloc[i] = match.group(5)
            result = False
        elif not match.group(4):
            result = 'rs{}'.format(cur_val.strip())
        return result

    def chr_check(result=True):

        """
            if ( $fields[1] eq "X" ) { $chr[$study] = 23; }
            elsif ( $fields[1] eq "Y" ) { $chr[$study] = 24; }
            elsif ( $fields[1] eq "XY" ) { $chr[$study] = 25; }
            elsif ( $fields[1] eq "MT" ) { $chr[$study] = 26; }
            else { $chr[$study] = $fields[1]; }
        """

        # check if autosomal chromosome number is no higher than 22
        global val
        if isinstance(val, int) and val < 23:
            result = True
        elif int(val) == 23:
            #replace with X/Y????
            pass
        else:
            result = False
        return result

    # check if human base pair number is no higher than 3,3 billion
    def bp_check(result=True):
        global val
        bp_human_genome = 3300000000
        if val > bp_human_genome:
            result = False
        return result

    def allele_check():
        # multiple allele check?
        """
        ### Function to convert alleles encoding of 1/2/3/4 to A/C/G/T -- which is PLINK old-style
        sub allele_1234_to_ACGT($)
        {
        	my $allele = shift;
        	if ( $allele eq "1" ) { return "A"; }
        	if ( $allele eq "2" ) { return "C"; }
        	if ( $allele eq "3" ) { return "G"; }
        	if ( $allele eq "4" ) { return "T"; }
        	return $allele;
        }
        """

        pass

    def freq_check():
        # convert scientific notation to float?
        return True

    def effect_check():
        # check for beta val: regression coefficient or odds ratio: ln(OR)
        global neg_values
        # if the value of the 'effect' column is negative, probably a Beta, as opposed to OR
        if match.group(1):
            neg_values += 1
        return True

    def pval_check():
        # convert scientific notation to float?
        return True

    def se_check():
        # convert scientific notation to float?
        return True

    def sample_control_check():
        return True

    def info_check():
        global val, eff_sum, info_fixed
        # info score must be between 1 and 0, because it is a percentage
        if 0 >= val <= 1:
            ratio = float(val)
        else:
            ratio = 1
        sample_size_eff = float(study_size * ratio)
        eff_sum += sample_size_eff

        # if the info value is not the same as the one from the first row, change bool
        if (val != first_info) and info_fixed:
            info_fixed = False
        # if val not 0 < val < 1 then make first_info False, so meta info = NONE
        return True

    def effect_type():
        # removed the head == 'effect' check
        size = (df.shape[0]) / 2
        # if zero negative values are found, it is certain the effect sizes are odd ratio's
        # but a small number of effect sizes may be negative due to a programmatic error
        if (neg_values/size) < 0.0005:
            if neg_values > 0:
                logger.info('you may want to check your data and run the parser again \n'
                            'a small number of negative effect values were found: < 0.5%\n'
                            'these were converted to positive numbers and converted to Beta')
            # iterate effect sizes and convert to beta by taking the natural logarithm
            for i, (row, val) in enumerate(df.itertuples()):
                if val < 0:
                    val *= -1
                df.replace(val, np.log(float(val)), regex=True, inplace=True)
        elif 0.0005 < (neg_values/size) < 0.3:
            logger.info('check your effect size, very few negative numbers for Beta values\n'
                        'were found: < 30%')
        # no operation for 'else': more than 30 % negative values, so all is well
        return 'Beta'

    def row_errors_append():
        # count number of errors for one row in a dictionary
        row_errors[str(i)] = row_errors.get(str(i), 0) + 1

    # corresponding check functions for the individual headers
    check_funcs = {'SNP': rs_check, 'CHR': chr_check, 'BP': bp_check, 'A1': allele_check,
                   'A2': allele_check, 'FRQ1': freq_check, 'FRQ2': freq_check,
                   'Effect': effect_check, 'P': pval_check, 'SE': se_check, 'Info':
                   info_check, 'Control': sample_control_check, 'Case': sample_control_check}

    head_operation()
    # get the specific pattern for the column type for dic 'col_types'
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
    # some operations to be done at end of the loop, depending on column type
    tail_operation()

    return df, head

"""note to self: correct chromosome check concerning chr 23(X|Y)
   remove allele2 frequency
   remove bed file column, make NaN value, catch exception later on
   check order of headers
   complete meta data json file operations
"""
