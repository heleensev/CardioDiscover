import pandas as pd


def file_to_dataframe(path, sp='\t', nms=None, ch=None, cols=None):
    for chunk in pd.read_csv(path, header=0, names=nms, sep=sp, chunksize=ch, usecols=cols):
        return chunk


# Class for the unchecked file (GWAS)
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
        names = self.names
        print("sep: {}".format(sep))
        for df in pd.read_csv(filename, header=0, names=names, sep=sep, chunksize=chsize, usecols=cols):
            return df