import logging
import sys

logger = logging.getLogger(__name__)
replacement_headers = {'additional info': 'info', 'strand orientation': 'strand', 'control samplesize': 'controls',
                       'samplesize cases': 'case', 'P-value' : 'P', 'effect size or Beta': 'Beta',
                       '(minor)allele frequency': 'FRQ', 'effect/minor allele': 'A1', 'major/non_effect allele': 'A2',
                       'position or location of SNP': 'BP', 'chromosome number': 'CHR', 'rsID of marker or SNP': 'SNP'}
header_info = [['rsID of marker or SNP', 1], ['chromosome number', 2], ['location of SNP', 3],
               ['strand orientation', 4], ['effect/minor allele', 5], ['non_effect/major allele', 6],
               ['minor allele', 7], ['effect allele frequency', 8], ['major allele frequency', 9],
               ['allele frequency', 10], ['effect size or Beta', 11], ['standard error', 12],
               ['P-value', 13], ['case sample size', 14], ['control sample size', 15], ['additional info', 16]]
header_dict = {''}


def init_usr_check(file):
    print("Automatic column parsing not succesful. Help me, human?")
    skip = input("Do column check? Y/N\n")
    while True:
        # if user chooses to skip the check, condition is false
        if skip.upper() == "N":
            sys.exit(1)
        elif skip.upper() == "Y":
            headers = column_unifier(file)
            return headers
        else:
            print("Y or N please\n")


def column_unifier(file):
    logger.info("entering column_unifier\n")

    df = file.file_to_df(chsize=5)
    headers = df.columns.values
    new_headers = df.columns.values
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
                new_headers[i] = replacement_headers.get(header_info[int(cor_nm)-1][0])
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

    print(df.columns.values)

    return new_headers


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


