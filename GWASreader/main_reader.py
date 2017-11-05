# main modules of CardioDiscover
from GWASParse import check_n_correct
from SNPconformer import liftover
from SNPconformer import SNP1000ref
import StatTester

# imports for meta data handling
from MetaReader.reader import read_meta
from MetaReader.reader import meta_studies
from MetaReader.writer import update_meta
from MetaReader.writer import write_meta

def main():
    # original doc containing the metadata
    meta_doc = read_meta(path="")
    # returns 'study' object with metadata as attributes
    studies = meta_studies(path="")

    for study in studies:
        # check and correct the GWAS file
        study = check_n_correct.init_check_correct(study)
        # make iterator in liftover and 1000ref
        study = liftover.iterator()
        study = ''
        #call the stuff

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()