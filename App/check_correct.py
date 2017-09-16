#check datatypes in all columns
import App.global_functions as glob
import pandas as pd
import re

def init_check_correct(file):
    
    type_checker(file)
    
def type_checker(file):
    
    df = glob.filetodf(file, chsize=5)
    headers = df.columns.headers
    for head in headers:
        df = glob.filetodf(file, cols=head)
        check_vals(df)


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

    column = df[head]
    pattern = col_types.get(head)[0]

    for val in column:
        valPattern = re.compile(r'(\s)*{}(\s)*'.format(pattern), re.I)
        match = valPattern.match(val)
        if match:
            if match.group(1) or match.group(2):
                val = val.strip(r'\s')
                #replace value in row with stripped \s
                pass
            if col_types.get(head)[1]:
                col_types.get(head)[1](val, match)
            continue
        else:
            #delete entire row
            pass
    #
    # if BED_format:
    #     process_BED()

def process_BED():

def check_rs(val, match):
    if match.group(1):
        str(val).lstrip('rs')


def check_loc():

def check_allele():

def check P_value():

#def check
