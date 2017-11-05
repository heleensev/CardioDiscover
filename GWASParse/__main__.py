#external imports
# import logging
# from logging.config import dictConfig
#package imports
from MetaReader.reader import read_meta
from MetaReader.reader import meta_studies
from MetaReader.writer import update_meta
from MetaReader.writer import write_meta
from GWASParse import reader
from GWASParse import classifier
from GWASParse import checker


def main():
    # original doc containing the metadata
    meta_doc = read_meta(path="")
    # returns 'study' object with metadata as attributes
    files = meta_studies(path="")

    for this_study in files:
        # read the study file, find separator, create
        GWASin = reader.init_reader(this_study)
        # do something with headers, write to df or something
        classifier.init_classifier(GWASin)
        # additional meta data about study to perform update
        add_meta = checker.init_check_correct(GWASin, this_study)

        meta_doc = update_meta(meta_doc, add_meta)

    write_meta(meta_doc)

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()
