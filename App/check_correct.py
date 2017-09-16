#check datatypes in all columns
import App.global_class as glob
import pandas as pd
import re

def init_check_correct(file):
    
    type_checker(file)
    
def type_checker(file):
    #provide filename
    filename = file.filename
    checked_file = glob.CheckedFile(filename)

    df = file.filetodf(file, chsize=5)
    headers = df.columns.headers
    for head in headers:
        df = file.filetodf(file, cols=head)
        df = check_vals(df, head)
        checked_file.writedf_to_file(col=df, header=head)



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
