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

    # record rs number merge history
    for ln in myopen('RsMergeArch.bcp.gz'):
        fd = ln.strip().split('\t')
        h, l = fd[0], fd[1]
        c = fd[6]
        # print 'c=', c
        RS_MERGE[h] = (l, c)
    pickle.dump(RS_MERGE, open("RS_MERGE.pl", "wb"), pickle.HIGHEST_PROTOCOL)