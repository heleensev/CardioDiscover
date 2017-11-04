#external imports
# import logging
# from logging.config import dictConfig
#package imports
from MetaReader.reader import read_meta
from MetaReader.writer import update_meta
from MetaReader.writer import write_meta
from GWASParse import reader
from GWASParse import classifier
from GWASParse import checker

meta_doc = dict

def main():
    global meta_doc

    files = read_meta('')
    for this_study in files:
        InputFile = reader.init_reader(this_study)
        #do something with headers, write to df or something
        classifier.init_classifier(InputFile)
        this_study = checker.init_check_correct(InputFile, this_study)
        meta_doc = update_meta(meta_doc, this_study)

    write_meta(meta_doc)
# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()

""" work on the meta writer"""