#global objects and classes use throughout the program
import pandas as pd
import logging

logging_config = dict(
            version=1,
            formatters={
                'f': {'format':
                          '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
            },
            handlers={
                'h': {'class': 'logging.StreamHandler',
                      'formatter': 'f',
                      'level': logging.DEBUG}
            },
            root={
                'handlers': ['h'],
                'level': logging.DEBUG,
            },
                )



#Global classes available throughout the program
class UncheckedFile:
    def __init__(self, filename, sep):
        self.filename = filename
        self.sep = sep

    # function to read a file to a (pandas)dataframe, chunksize or the columns used may be specified
    def file_to_df(self, chsize=None, cols=None, sep=None):
        # sep = df_buffer.get('separator')
        filename = self.filename
        print("sep: {}".format(sep))
        df = pd.read_csv(filename, sep=sep, header=0, chunksize=chsize, usecols=cols)
        return df

class CheckedFile:
    def __init__(self, filename):
        self.file = '{}.csv'.format(filename)

    def writedf_to_file(self, col, header):
        filename = self.file
        header = self.header
        col = pd.DataFrame(self.col)

        self.file = col[header].to_csv(filename, index=False, mode='a')

        pass
