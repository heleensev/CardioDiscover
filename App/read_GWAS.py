import os, re, logging
from App import glob


df_buffer = dict()
filename = str()
file_nm = 0
logger = logging.getLogger(__name__)
all_files = ["cad.add.160614.complete.website.txt","HTN_all_ethnic.csv", "tag.cpd.table.txt"]

def init_reader():
    logger.info("Entering read_GWAS")

    selected_file = input_prompt()
    sep = check_sep(selected_file)

    InputFile = glob.UncheckedFile(selected_file, sep)

    return InputFile


def get_path(fdir, fpath):

    fpath = fdir+fpath
    return os.path.join(os.path.dirname(__file__), fpath)


def input_prompt():
    for i, file in enumerate(all_files):
        print(file)

    user_input = str(input("choose one or multiple files, by typing the numbers (sep=space)\n"))
    user_input = user_input.split()

    file = parse_input(user_input)
    
    return file


def parse_input(user_input):
    selected_files = list()

    for num in user_input:
        selected_files.append(all_files[int(num)-1])

    for file, num in zip(selected_files, user_input):
        global file_nm
        file_nm = int(num)
        return file

def open_file(file):
    file = get_path("../Datasets/GWAS/", file)
    print(file)
    global filename
    filename = file
    with open(filename) as fin:
        header = fin.readline(500)
        if header:
            return header
        else:
            print("file does not contain newlines, that's not going to work")
            exit(1)


def check_sep(file):
    header_line = open_file(file)
    logger.info("entering check sep\n")
    b = {}

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
        logger.info("valid seperator found: " + sep + "\n")
        #add seperator to df_buffer (dictionary) in case of chuncked file
        df_buffer['separator'] = sep
        #file_to_df(lines)
        return sep
    else:
        print("no valid separator found")
        exit(1)



    # loc_names = ['bp_hg19', 'Physical_Location', 'BP']
    #
    # dflist = df["Physical_Location"].tolist()
    #
    # lo = liftover('hg17', 'hg18')
    # for location in dflist:
    #     print(lo.convert_coordinate('chr1', location))

