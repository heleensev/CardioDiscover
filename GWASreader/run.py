# local package for file chunking
from DataFrameHandler import chunker
# imports for meta data handling
from MetaReader.reader import meta_studies
# local module for generating bash scripts for qsub
from GWASreader import gen_bash, local_run


def main():

    # returns 'study' object with metadata as attributes
    studies, prefs = meta_studies(path="../config.json")

    for study in studies:
        # read the file to a pandas dataframe, get params from study object
        chunker.init(study, pickle=True)
    if prefs.hpc:
        gen_bash.run(studies)
    else:
        #local_run.run()
        pass

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()
