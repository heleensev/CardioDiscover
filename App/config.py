#global objects and classes use throughout the program
import logging
import pandas as pd


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
        self.headers = 0
        self.names = None
        self.skip = None

    # function to read a file to a (pandas)dataframe, chunksize or the columns used may be specified
    def file_to_df(self, chsize=None, cols=None):
        # sep = df_buffer.get('separator')
        filename = self.filename
        sep = self.sep
        headers = self.headers
        names = self.names
        print("sep: {}".format(sep))
        for df in pd.read_csv(filename, header=headers, names=names, sep=sep, chunksize=chsize, usecols=cols):
            return df

class CheckedFile:
    def __init__(self, filename, dispose):
        self.dispose = dispose
        self.file = '{}.csv'.format(filename)

    def writedf_to_file(self, col, header):
        filename = self.file
        header = header
        col = pd.DataFrame(col)

        self.file = col[header].to_csv(filename, index=False, mode='a')

        pass
