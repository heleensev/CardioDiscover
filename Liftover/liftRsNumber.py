#!/usr/bin/python
import sys, os, time
#import pydev, pickle
#import cPickle as pickle for python 2

starttime = time.time()
print(starttime)
#pydevd.settrace('hpcsubmit.op.umcutrecht.nl', port=22, stdoutToServer=True, stderrToServer=True)

def usage():
    print("%s file: lift over rs number. " % sys.argv[0])
    print("file should look like:")
    print("11111")
    print("11112")
    print("...")

def get_path(dir, fpath):
    fpath = dir+fpath
    return os.path.join(os.path.dirname(__file__), fpath)

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
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    #record obsolete rs number
    for ln in myopen('SNPHistory.bcp.gz'):
        fd = ln.strip().split('\t')
        if ln.find('re-activ') < 0:
            RS_HISTORY.add(fd[0])
    #pickle.dump(RS_HISTORY, open("RS_HISTORY.pl", "wb"), pickle.HIGHEST_PROTOCOL)

    #record rs number merge history
    for ln in myopen('RsMergeArch.bcp.gz'):
        fd = ln.strip().split('\t')
        h, l = fd[0], fd[1]
        c = fd[6]
        # print 'c=', c
        RS_MERGE[h] = (l, c)
    #pickle.dump(RS_MERGE, open("RS_MERGE.pl", "wb"), pickle.HIGHEST_PROTOCOL)

    # # find some retracted SNPs for fun
    # for h, v in RS_MERGE.iteritems():
    # 	l, c = v
    # 	if c in RS_HISTORY:
    # 	    print h, '->', l
    # RSM_pickle_path = get_path("../Datasets/LiftOver/", "RS_MERGE.pl")
    # RSH_pickle_path = get_path("../Datasets/liftOver/", "RS_HISTORY.pl")
    # RS_MERGE = pickle.load(open(RSM_pickle_path, "rb"))
    # RS_HISTORY = pickle.load(open(RSM_pickle_path, "rb"))

    import re

    output_file = open("ouput_file.rs", "a")

    rsPattern = re.compile(r'[0-9]*')
    for ln in myopen(sys.argv[1]):
        rs = ln.strip()
        if not rsPattern.match(rs):
            #print('ERROR: rs number should be like "1000"')
            output_file.write("Err: wrong format for:  %s\n" % rs)
            sys.exit(2)
        # rs number not appear in RS_MERGE -> there is no merge on this rs
        if rs not in RS_MERGE:
            #print("unchanged\t", rs)
            output_file.write("%s not in rsMerge: unchanged\n" % rs)

            continue
        # lift rs number
        while True:
            if rs in RS_MERGE:
                rsLow, rsCurrent = RS_MERGE[rs]
                if rsCurrent not in RS_HISTORY:
                    #print("lifted\t", rsCurrent)
                    output_file.write("%s lifted to: %s\n" % (rs, rsCurrent))
                    break
                else:
                    rs = rsLow
                    output_file.write("%s lifted to lower rs: %s\n" % (rs, rsLow))
            else:
                # program never reaches this block??
                print("unlifted\t", rs)
                output_file.write("%s unlifted, not in rsMerge\n" % rs)
                break

endtime = time.time()
output_file.write("total runtime in seconds: %d"%endtime-starttime)
output_file.close()
print("total runtime in seconds: %d"%(endtime-starttime))


#pydevd.stoptrace()