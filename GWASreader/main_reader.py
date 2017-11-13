# main modules of CardioDiscover
from DataFrameHandler import chunker
from GWASParse import check_n_correct
from SNPconformer import liftover
from SNPconformer import reference_check

# imports for meta data handling
from MetaReader.reader import meta_studies


def main():

    # returns 'study' object with metadata as attributes
    studies, prefs = meta_studies(path="../config.json")

    for study in studies:
        # read the file to a pandas dataframe, get params from study object
        chunker.init(study)
    if prefs.hpc:
        gen_bash()
    else:
        # what to do
        pass



    # # check and correct the GWAS file
    # study = check_n_correct.init_check_correct(study)
    # # make iterator in liftover and 1000ref
    # study = liftover.iterator()
    # stuy = reference_check.iterator()
    # study = ''
    # #call the stuff

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()