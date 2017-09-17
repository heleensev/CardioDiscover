#external imports
import logging
from logging.config import dictConfig
#package imports
from App import config
#from App import reader
import App.read_GWAS as reader
from App import classifier
from App import checker

def main():

    dictConfig(config.logging_config)

    file, filename = reader.init_reader()
    #do something with headers, write to df or something
    headers = classifier.init_classifier(file)
    df = checker.init_check_correct(file)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()