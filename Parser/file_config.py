#global objects and classes use throughout the program
import logging, os
import pandas as pd

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

    def file_to_dfcol(self, head, cols=None):
        filename = self.filename
        sep = self.sep
        df = pd.read_csv(filename, header=0, names=[head], sep=sep, usecols=cols)
        return df

# Class for the checked file, after classify_columns
class CheckedFile:
    def __init__(self, filename, disposed):
        self.filename = filename
        self.disposed = disposed
        self.columns = list()
        self.orientation = dict()

    def update_column_names(self, name):
        columns = self.columns
        columns.append(name)

    def update_orientation(self, orient):
        self.orientation = orient

    def write_to_file(self, df, name):
        name = '{}.csv'.format(name)
        df.to_csv(self.get_path(name), index=False, header=name)
        self.update_column_names(name)

    def get_filename(self):
        file_wo_path = self.filename.split('/')[-1]
        path = '/'.join(self.filename.split('/')[:-2])
        self.filename = '{}/Output/processed_{}'.format(path, file_wo_path)
        # if file already exists, empty the contents
        if os.path.exists(self.filename):
            open(self.filename, 'w').close()

    def get_path(self, filename):
        outputdir = '/home/sevvy/PycharmProjects/CardioDiscover/Datasets/Tempfiles/'
        fpath = outputdir + filename
        return os.path.join(os.path.dirname(__file__), fpath)

    def get_chunksize(self):
        columns = self.columns
        chunksize = int((pd.read_csv(self.get_path(columns[0]), header=0).shape[0])/2)
        chunks = int(chunksize/5000)
        if chunksize % 5000 != 0:
            chunks += 1
        return chunks

    def message(self):
        print('Process succesful! find your checked & corrected file here: {}'.format(self.filename))

    def concat_write(self, head=True):
        self.get_filename()
        filename = self.filename
        columns = self.columns

        # pd.read replace by methods, make it cleaner
        chunks = self.get_chunksize()
        concat_chunk = pd.DataFrame

        for _ in range(chunks):
            col_prev = pd.read_csv(self.get_path(columns[0]), header=0, chunksize=5000).get_chunk()
            for col in columns[1:]:
                col_cur = pd.read_csv(self.get_path(col), header=0, chunksize=5000).get_chunk()
                concat_chunk = pd.concat([col_prev, col_cur], axis=1)
                col_prev = concat_chunk
            concat_chunk.to_csv(filename, sep='\t', header=head, mode='a', index=False)
            head = None
        self.message()


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
