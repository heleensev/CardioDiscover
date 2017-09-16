#global functions use throughout the program
import pandas as pd

log_file = open("log.txt", 'a')

#function to read a file to a (pandas)dataframe, chunksize or the columns used may be specified
def filetodf(filename, chsize=None, cols=None, sep=None):

    #sep = df_buffer.get('separator')
    print("sep: {}".format(sep))
    for i, df in enumerate(pd.read_csv(filename, sep= sep, header=0, chunksize=chsize, usecols= cols)):
        #column_unifier(df)
        # if i == 0:
        #     column_unifier()
        return df

    #getsomeBEDs(chunk)

#function to write or adapt dataframe
def writedf():
    pass
