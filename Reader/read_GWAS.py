import pandas as pd
from io import StringIO
from pyliftover import liftover
import re, os, logging

all_files = ["cad.add.160614.website.txt","HTN_all_ethnic.csv", "tag.cpd.table.txt"]
log_file = open("log.txt", 'a')
log_file.flush()
df_buffer = dict()
filename = str()
file_nm = 0
#RAF(risk allele freq == MAF??), wat te doen met CAF (coded allele freq) == minor allele freq?
#RAF EAF MAF CAF
replacement_headers = {'additional info': 'info', 'strand orientation': 'strand', 'control samplesize': 'controls',
                       'samplesize cases': 'case', 'P-value' : 'P', 'effect size or Beta': 'Beta',
                       'effect allele frequency': 'EAf', 'major allele frequency': 'RAF',
                       'non-effect allele frequency' : 'CAF', 'minor allele frequency': 'MAF', 'effect/risk allele':
                       'effect_allele', 'major allele': 'major_allele', 'non-effect allele': "non_effect_allele",
                       'minor allele': 'minor_allele', 'position or location of SNP': 'BP', 'chromosome number': 'CHR',
                       'rsID of marker or SNP': 'MarkerOriginal'}
header_info = [['rsID of marker or SNP', 1], ['chromosome number', 2], ['location of SNP', 3],
               ['strand orientation', 4], ['effect allele', 5], ['major allele', 6], ['non-effect allele', 7],
               ['minor allele', 8], ['effect allele frequency', 9], ['major allele frequency', 10],
               ['non-effect allele frequency', 11], ['minor allele frequency', 12], ['effect size or Beta', 13],
               ['standard error', 14], ['P-value', 15], ['case samplesize', 16], ['control samplesize', 17],
               ['additional info', 18]]
header_dict = {''}

def get_path(dir, fpath):
    fpath = dir+fpath
    return os.path.join(os.path.dirname(__file__), fpath)

def main():

    input_prompt()
    log_file.close()

def input_prompt():

    for i, file in enumerate(all_files):
        print(file)

    user_input = str(input("choose one or multiple files, by typing the numbers (sep=space)\n"))
    user_input = user_input.split()

    parse_input(user_input)

def parse_input(user_input):

    selected_files = list()

    for num in user_input:
        selected_files.append(all_files[int(num)-1])

    for file, num in zip(selected_files, user_input):
        chunker1(file)
        global file_nm
        file_nm = int(num)

def chunker1(file):
    file = get_path("../Datasets/GWAS/", file)
    print(file)
    global filename
    filename = file
    chunked = False

    lines = str()
    NUM_OF_LINES = 250000
    filename = file
    with open(filename) as fin:
        # temp = open("tmp_chunk", 'w')
        for i, line in enumerate(fin):
            if line != '':
                lines += line
            if (i + 1) % NUM_OF_LINES == 0:
                check_sep(lines)
                # check_sep(chucked)
                chunked = True
                break
        if not chunked:
            log_file.write("not chunked, to check sep\n")
            check_sep(lines)


def chunker(file):
    file = get_path(file)
    print(file)
    chunked = False

    lines = str()
    NUM_OF_LINES = 250000
    filename = file
    with open(filename) as fin:
        #temp = open("tmp_chunk", 'w')
        for i, line in enumerate(fin):
            if line != '':
                lines += line
            if (i + 1) % NUM_OF_LINES == 0:
                if chunked:
                    file_to_df(lines, chunked)
                else:
                    check_sep(lines)
                #check_sep(chucked)
                chunked = True
        if not chunked:
            log_file.write("not chunked, to check sep\n")
            check_sep(lines)

def check_sep(lines):
    log_file.write("entering check sep\n")
    b = {}

    split_lines = lines.split("\n")

    if len(split_lines) == 1:
        print("Your file doesnt contain newlines, too bad, but that's not gonna work")
        return
    header_line = split_lines[0]

    separators = re.findall(r"\W", header_line)

    for sep in separators:
        b[sep] = b.get(sep, 0) + 1

    cnts = list()
    seps = list()
    for sep in b.keys():
        seps.append(sep)
        cnt = b.get(sep)
        cnts.append(int(cnt))
    max_cnt = max(cnts)
    if max_cnt > 5:
        sep = seps[cnts.index(max_cnt)]
        log_file.write("valid seperator found: " + sep + "\n")
        #add seperator to df_buffer (dictionary) in case of chuncked file
        df_buffer['separator'] = sep
        #file_to_df(lines)
        filetodf()
    else:
        print("no valid separator found")

def filetodf():
    global filename

    sep = df_buffer.get('separator')
    print("sep: {}".format(sep))
    for df in pd.read_csv(filename, sep= sep, header=0, chunksize=6000):
        column_unifier(df)
    #getsomeBEDs(chunk)

    print("done reading df")


def file_to_df(lines, chunked= False):
    log_file.write("entering file_to_df\n")
    df = None
    contents = lines
    sep = df_buffer.get('separator')
    #csv_contents = contents.replace(sep, ",")
    head_present = 0
    if chunked:
        log_file.write("chunked: df_buffer.get(headers)")
        head_present = df_buffer.get('headers')
    else:
        head_present = 'infer'

    try:
        temp = open("temp_chunk.csv", 'w')
        temp.write(lines)
        #df = pd.read_csv(contents, sep=sep, header=head_present)
        df = pd.read_csv(contents)
        temp.close()
    except Exception as e:

        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    print("done reading df")

    if df:
        if chunked:
            log_file.write('chunked in file_to_df\n')
            check_correct()
        else:
            log_file.write('not chunked in file_to_df\n')
            headers = df.columns.values
            df_buffer['headers'] = headers
            column_unifier(df)
    else:
        log_file.write("failed to read dataframe\n")


def column_unifier(df):
    log_file.write("entering column_unifier\n")
    width = 20

    headers = df.columns.values
    # global file_nm
    # print("file name: {}\nThe headers of this file are: ".format(str(all_files[file_nm])))
    # for i, header in enumerate(headers):
    #     print("{}\t{}\n".format(str(i),header))

    # replacement_headers = {'info': 'additional information about the data', 'strand': 'strand of DNA',
    #                         'controls': 'control group data', 'case': 'case group data',
    #                         'N': 'samplesize', 'HWE':'HWE value', 'P': 'P-value','Beta': 'effect size or'
    #                         'beta', 'RAF': 'RAF', 'EAF': 'eaf', 'MAF': 'maf', 'CAF': 'caf', 'otherAllel':
    #                         'other allele or minor allele', 'MajorAllele': 'Major allele or effect allele'
    #                         , 'BP': 'position or location of SNP', 'CHR': 'chromosome nr', 'MarkerOriginal'
    #                   df      : 'rsID of marker or SNP'}


    new_columns = df.columns.values
    global replacement_headers
    global header_info

    print("len headers: ", len(header_info))

    for i, header in enumerate(headers):
        print_table()
        print(df[[header]][0:5])
        print("Please type the number of the corresponding description of the information in this column. "
              "If the description is not available, then it's not relevant, type: N")
        try_again = True
        while try_again:
            cor_nm = str(input())
            if cor_nm.isdigit():
                headers[i] = replacement_headers.get(header_info[int(cor_nm)-1][0])
                try_again = False
            elif cor_nm.upper() == "N":
                try_again = False
            else:
                "Seems like you failed to type a number, please try again"
            print('If you made a mistake press any key for the following input, else: press ENTER')
            not_done = input()
            if not_done:
                try_again = True
                print("Please type the number of the corresponding description of the information in this column. "
                      "If the description is not available, then it's not relevant, type: N")


    df_buffer['new_columns'] = new_columns
    print(df.columns.values)

    with pd.option_context('max_rows',10):
        print(df)

    getsomeBEDs(df)

def print_table():

    global header_info

    iter_headers = iter(header_info)
    for i, item in enumerate(iter_headers):
        try:
            if True:
                next_item = next(iter_headers)
                print('{}\t{}|{}\t{}'.format(item[1], item[0].ljust(40), str(next_item[1]), next_item[0].ljust(40)))
            else:
                print('{}\t{}|').format(str(item[1]), item[0].ljust(40))
        except AttributeError:
            print("attribute error")

        except StopIteration:
            print("stop iteration")
    print("\n")

def getsomeBEDs(df):

    # rs_col = df["markername"].tolist()
    # print(rs_col)
    pass


def check_correct():
    log_file.write("entering check correct\n")


    pass

def liftover():

    pass
    # loc_names = ['bp_hg19', 'Physical_Location', 'BP']
    #
    # dflist = df["Physical_Location"].tolist()
    #
    # lo = liftover('hg17', 'hg18')
    # for location in dflist:
    #     print(lo.convert_coordinate('chr1', location))


main()