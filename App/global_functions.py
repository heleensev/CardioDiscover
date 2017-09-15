#global functions use throughout the program

#function to read a file to a (pandas)dataframe, chunksize or the columns used may be specified
def filetodf(chsize=None, cols=None):
    global filename

    sep = df_buffer.get('separator')
    print("sep: {}".format(sep))
    for i, df in enumerate(pd.read_csv(filename, sep= sep, header=0, chunksize=chsize, usecols= cols)):
        #column_unifier(df)
        if i == 0:
            column_unifier()

    #getsomeBEDs(chunk)

#function to write or adapt dataframe
def writedf():
    pass
