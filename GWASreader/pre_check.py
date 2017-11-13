from GWASParse import read_GWAS
from GWASParse import classify_columns

from MetaReader.reader import read_meta
from MetaReader.writer import write_meta


def main():
    # original doc containing the metadata
    meta_doc = read_meta(path="/home/sevvy/PycharmProjects/CardioDiscover/config.json")

    for study_doc in meta_doc:
        # read the GWAS file, study doc update with separator for the columns
        study_doc = read_GWAS.init_reader(study_doc)
        # identify the columns in the GWAS file, study doc updated with headers and indices
        study_doc = classify_columns.init_classifier(study_doc)
        # update original meta_doc with the new meta data
        meta_doc.update(study_doc)
    # when done write doc with additional info to json config file
    write_meta(meta_doc)

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()
