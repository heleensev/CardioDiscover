#global objects and classes use throughout the program
import logging, os
import pandas as pd

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
        names = self.names
        print("sep: {}".format(sep))
        for df in pd.read_csv(filename, header=0, names=names, sep=sep, chunksize=chsize, usecols=cols):
            return df

    def file_to_dfcol(self, cols=None):
        filename = self.filename
        sep = self.sep
        names = self.names
        df = pd.read_csv(filename, header=0, names=names, sep=sep, usecols=cols)
        return df


class CheckedFile:
    def __init__(self, filename):
        self.filename = filename
        self.columns = list()

    def column_names(self, name):
        columns = self.columns
        self.columns = columns.append(name)

    def write_to_file(self, df, name):
        name = '{}.csv'.format(name)
        df.to_csv(name, index=False, header=0)

    def concat_write(self, head=True):
        filename = self.filename
        columns = self.columns

        # pd.read replace by methods, make it cleaner
        cols = [col for col in columns]
        col = cols[0]
        for chunk in pd.read_csv(col, header=head, chunksize=5000):
            col_prev = chunk
            for col in cols[1:]:
                col_cur = pd.read_csv(col, header=head, chunksize=5000).get_chunk()
                concat_chunk = pd.concat([col_prev, col_cur])
                col_prev = col_cur
            concat_chunk.to_csv(filename, sep='\t', header=head, mode='a', index=False)
            head = False

# class CheckedFile:
#     def __init__(self, filename, dispose):
#         self.dispose = dispose
#         self.filename = '{}.csv'.format(filename)
#         self.file = open('{}'.format(filename))
#
#
#     def writedf_to_file(self, df=None, header=None):
#         filename = '{}.csv'.format(header)
#
#         # if os.path.isfile(filename):
#         #     csv_input = pd.read_csv(filename, chunksize=2)
#         #     csv_input[header] = df[header]
#         # csv_input.to_csv('output.csv', index=False)
#
#         df.to_csv(filename, index=False, header=header)
#
#     def concat_dfs(self, csv_names):
#
#         pass


# class ExceptionTemplate(Exception):
#     def __init__(self, message, errors):
#         # Call the base class constructor with the parameters it needs
#         super(ExceptionTemplate, self).__init__(message)
#
#         # Now for your custom code...
#         self.errors = errors
#     #def call_usr_check(self, file, ):




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

"""fix writing to csv in chunks in CheckedFile, use csv reader"""