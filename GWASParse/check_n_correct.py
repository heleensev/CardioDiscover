# check datatypes in all columns, correct if necessary
import re, simplejson, logging
import numpy as np
import pandas as pd
from MetaReader.writer import write_meta

""" GLOBALS
    df: chunked pandas dataframe from GWAS csv file
    study: Study (see MetaReader.config) object containing meta data,
    study_size: to compute a sum of the study,
    eff_sum: sum of the effective size of study,
    row_errors: dictionary of bad rows to be dropped,
    neg_values: counter for the 'effect' column to determine if Beta/OR,
    first_info: first row of 'effect' column to determine if effect is fixed,
    info_fixed: bool for fixed effect
    col_types: patterns for columns that may be present in data set
"""

logger = logging.getLogger(__name__)

df = object()
study = object()
study_size = int()
eff_sum = float()
row_errors = dict()
neg_values = int()
first_info = float()
info_fixed = True

col_types = {'SNP': '((rs[ _-]?)?\d+)|(.*)',
             'CHR': '(\d){1,2}|[XYMT]{1,2}',
             'BP': '\d{10}',
             'A1': '[ATCGRDI]+',
             'A2': '[ATCGRDI]+',
             'FRQ': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'Effect': '(-)?(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'SE': '(\d)*(\.)(\d)*(E(-)?)?(\d)*',
             'P': '(\d)*(\.)(\d)*(E)?(-)?(\d)',
             'Case': '[0-1000000]',
             'Control': '[0-1000000]',
             'Info': '(\d)*(\.)(\d)*(E)?(-)?(\d)*'}


def init(this_df, this_study):

    """
    :param this_df: chunked pandas dataframe from GWAS csv
    :param this_study: Study object with meta data as attributes
    :return: checked and corrected dataframe

    """
    global df, study, study_size
    df = this_df
    study = this_study
    study_size = study.study_size
    type_checker()
    # get additional meta data about study
    add_meta = get_meta_items()

    return df, add_meta


def type_checker():
    global study, df

    headers = study.headers
    for i, header in enumerate(headers):
        check_vals(df.groupby[i], header)


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
    global study, row_errors

    def head_operation():
        global first_info
        # get the info score of the first row
        if head == 'Info':
            first_info = float(df.iloc[0])

    def tail_operation():
        global head, df
        # check if current header is 'effect', determine the type of unit
        if head == 'effect':
            effect_type()

    # specific check functions for column type in GWAS
    def rs_check():
        # check if rs prefix is present, if not, return concatenated value
        cur_val = val
        if match.group(1) and match.group(2):
            result = True
        elif match.group(1):
            result = 'rs{}'.format(cur_val.strip())
        else:
            result = np.NaN
        return result

    def chr_check(result=True):
        # NCBI notation for X, Y, XY and MT
        chr_map = {'X': '23', 'Y': '24', 'XY': '25', 'MT': '26'}
        cur_val = val
        if cur_val in chr_map:
            cur_val = chr_map.get(cur_val)
            return cur_val
        # check if autosomal chromosome number is no higher than 22
        global val
        if not isinstance(val, int) and val < 23:
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
        # old PLINK notation for alleles
        plink_map = {'1': 'A', '2': 'C', '3': 'G', '4': 'T'}
        # multiple allele check?

        cur_val = val
        if cur_val in plink_map:
            cur_val = plink_map.get(cur_val)


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
        size = df.size
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
    check_funcs = {'SNP': rs_check, 'CHR': chr_check, 'BP': bp_check, 'A1': allele_check, 'A2': allele_check,
                   'FRQ1': freq_check, 'Effect': effect_check, 'P': pval_check, 'SE': se_check,
                   'Info': info_check, 'Control': sample_control_check, 'Case': sample_control_check}

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


"""note to self:
    correct chromosome check concerning chr 23(X|Y)
   remove bed file column, make NaN value, catch exception later on
   check order of headers

   look at the fixed effect stuff with Sander
"""
