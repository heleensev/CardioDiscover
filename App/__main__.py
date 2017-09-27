#external imports
# import logging
# from logging.config import dictConfig
#package imports

from App import reader
from App import classifier
from App import checker

def main():

    #dictConfig(config.logging_config)
    InputFile = reader.init_reader()
    #do something with headers, write to df or something
    classifier.init_classifier(InputFile)
    checker.init_check_correct(InputFile)

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()
