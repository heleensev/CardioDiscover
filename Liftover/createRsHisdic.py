import cPickle as pickle

def myopen(fn):
    import gzip
    try:
        h = gzip.open(fn)
        ln = h.read(2)  # read arbitrary bytes so check if @param fn is a gzipped file
    except:
        # cannot read in gzip format
        return open(fn)
    h.close()
    return gzip.open(fn)

RS_HISTORY = set()  # store rs
RS_MERGE = dict()  # high_rs -> (lower_rs, current_rs)
if __name__ == '__main__':

    # record obsolete rs number
    for ln in myopen('SNPHistory.bcp.gz'):
        fd = ln.strip().split('\t')
        if ln.find('re-activ') < 0:
            RS_HISTORY.add(fd[0])
    pickle.dump(RS_HISTORY, open("RS_HISTORY.pl", "wb"), pickle.HIGHEST_PROTOCOL)
