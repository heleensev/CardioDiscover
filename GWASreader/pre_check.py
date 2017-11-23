from GWASParse import read_GWAS
from GWASParse import classify_columns

from MetaReader.reader import read_meta
from MetaReader.writer import write_meta


def main():

    """ reads config.json containing the meta data, calls MetaReader to turn
        this information into 'Study' objects,
        loops over the Study objects to:
        - read the GWAS data with read_GWAS,
        - classify the columns in the GWAS data set
        finally write additional info to config.json
    """
    meta_doc = read_meta(path="/home/sevvy/PycharmProjects/CardioDiscover/test_config.json")

    for study_doc in meta_doc:
        # doc updated separator for the columns
        study_doc = read_GWAS.init_reader(study_doc)
        # updated doc with headers and indices
        study_doc = classify_columns.init_classifier(study_doc)
        # update original meta_doc with the new meta data
        meta_doc.update(study_doc)
    # write doc with additional info to json config file
    write_meta(meta_doc)

if __name__ == '__main__':
    main()
