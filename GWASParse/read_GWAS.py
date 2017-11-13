import re, logging

filename = str()
logger = logging.getLogger(__name__)


def init_reader(study):
    logger.info("Entering read_GWAS")
    path = study.get_path()
    sep = check_sep(path)
    # update studyID doc with separator
    study.update({'sep': sep})

    return study


def open_file(file):
    global filename
    try:
        # read first line of file, if line is longer than 300, probably not a header line or line \
        # was not proper split because of lacking new lines
        with open(file) as GWAS_file:
            header = GWAS_file.readline(500)
            if header:
                return header
            else:
                mssg = "file does not contain newlines, or has extremely long lines, that's not going to work"
                print(mssg)
                raise Exception(mssg)
    except Exception as e:
        if e:
            logger.error(e)
        else:
            logger.error("Error occured during separator check: {}".format(e))
        exit(1)


def check_sep(path):
    try:
        # call open_file to check for a valid separator, and a valid header line
        header_line = open_file(path)
        logger.info("entering check sep\n")
        b = {}
        # find all non-newlines in the header line
        separators = re.findall(r"\W", header_line)
        # for all found non-newlines, write to a dictionary, count entries by \
        # summing previous identical entries
        for sep in separators:
            b[sep] = b.get(sep, 0) + 1
        # list for
        cnts = list()
        seps = list()
        for sep in b.keys():
            seps.append(sep)
            cnt = b.get(sep)
            cnts.append(int(cnt))
        max_cnt = max(cnts)
        if max_cnt > 5:
            sep = seps[cnts.index(max_cnt)]
            logger.info("valid separator found: " + sep + "\n")
            return sep
        else:
            mssg = "no valid separator found"
            print(mssg)
            raise Exception(mssg)
    except Exception as e:
        if e:
            logger.error(e)
        else:
            logger.error("Error occured during separator check: {}".format(e))
        exit(1)
