import os, re, logging
from GWASParse import glob


df_buffer = dict()
filename = str()
logger = logging.getLogger(__name__)
all_files = ["cad.add.160614.complete.website.txt","HTN_all_ethnic.csv", "tag.cpd.table.txt"]

def init_reader():
    logger.info("Entering read_GWAS")
    # call input_prompt for user input
    selected_file = input_prompt()
    sep = check_sep(selected_file)

    InputFile = glob.UncheckedFile(selected_file, sep)

    return InputFile


def get_path(fdir, fpath):

    fpath = fdir+fpath
    return os.path.join(os.path.dirname(__file__), fpath)


def input_prompt():
    # for all file in list of files, only for testing, to be deleted
    for i, file in enumerate(all_files):
        print('{}: {}'.format(i+1, file))
    # get user input for choosing the files from the list by the numbers
    user_input = str(input("choose one or multiple files, by typing the numbers (sep=space)\n"))
    # make a list of user input
    user_input = user_input.split()

    file = parse_input(user_input)
    # return file to init_reader
    return file


def parse_input(user_input):
    selected_files = list()
    # for every number typed by user, append corresponding file to a list
    for num in user_input:
        selected_files.append(all_files[int(num)-1])
    # for every file in selected_files list,
    for file, num in zip(selected_files, user_input):
        file_nm = int(num)
        logger.info("Processing file number {}".format(file_nm + 1))
        # call get_path to get absolute path of input file
        file = get_path("../Datasets/Parser/GWAS/", file)
        # return file to input_prompt
        return file

def open_file(file):

    global filename
    filename = file
    # read first line of file, if line is longer than 300, probably not a header line or line \
    # was not proper split because of lacking new lines
    with open(filename) as fin:
        header = fin.readline(500)
        if header:
            return header
        else:
            print("file does not contain newlines, or has extremely long lines, that's not going to work")
            exit(1)


def check_sep(file):
    # call open_file to check for a valid separator, and a valid header line
    header_line = open_file(file)
    logger.info("entering check sep\n")
    b = {}
    # find all non-newlines in the header line
    separators = re.findall(r"\W", header_line)
    # for all found non-newlines, write to a dictionary, count entries by \
    # summing previous identical entries
    for sep in separators:
        b[sep] = b.get(sep, 0) + 1
    # list for
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


