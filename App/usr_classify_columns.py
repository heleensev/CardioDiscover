import logging

#RAF(risk allele freq == MAF??), wat te doen met CAF (coded allele freq) == minor allele freq?
#RAF EAF MAF CAF
logger = logging.getLogger(__name__)
replacement_headers = {'additional info': 'info', 'strand orientation': 'strand', 'control samplesize': 'controls',
                   'samplesize cases': 'case', 'P-value' : 'P', 'effect size or Beta': 'Beta',
                   'effect allele frequency': 'EAf', 'major allele frequency': 'JAF',
                   'non-effect allele frequency' : 'NAF', 'minor allele frequency': 'MAF', 'effect/risk allele':
                   'effect_allele', 'major allele': 'major_allele', 'non-effect allele': "non_effect_allele",
                   'minor allele': 'minor_allele', 'position or location of SNP': 'BP', 'chromosome number': 'CHR',
                   'rsID of marker or SNP': 'marker_original'}
header_info = [['rsID of marker or SNP', 1], ['chromosome number', 2], ['location of SNP', 3],
               ['strand orientation', 4], ['effect allele', 5], ['major allele', 6], ['non-effect allele', 7],
               ['minor allele', 8], ['effect allele frequency', 9], ['major allele frequency', 10],
               ['non-effect allele frequency', 11], ['minor allele frequency', 12], ['effect size or Beta', 13],
               ['standard error', 14], ['P-value', 15], ['case samplesize', 16], ['control samplesize', 17],
               ['additional info', 18]]
header_dict = {''}

def init_usr_check(file):
    headers = column_unifier(file)
    return headers

def column_unifier(file):
    logger.info("entering column_unifier\n")

    print("Automatic column parsing not succesful. Help me, human?")
    skip = input("Skip column check? Y/N\n")
    while True:
        if skip.upper() == "N":
            
            df = file.file_to_df(chsize=5)
            headers = df.columns.values
            usr_headers = []
            # global file_nm
            # print("file name: {}\nThe headers of this file are: ".format(str(all_files[file_nm])))
            # for i, header in enumerate(headers):
            #     print("{}\t{}\n".format(str(i),header))

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

            # with pd.option_context('max_rows',10):
            #     print(df)
        elif skip.upper() == "Y":
            return
        else:
            print("Y or N please\n")


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

def get_some_rss(df):

    rscol = df.columns.values.tolist()[0]
    #rs_output = open("cad_rs.txt", 'a')
    df[rscol].to_csv("cad_rs.csv", index=False, mode='a')


