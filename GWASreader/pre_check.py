from GWASParse import read_GWAS
from GWASParse import classify_columns

from MetaReader.reader import read_meta
from MetaReader.reader import meta_studies
from MetaReader.writer import update_meta
from MetaReader.writer import write_meta

def main():
    # original doc containing the metadata
    meta_doc = read_meta(path="")

    for study in meta_doc:
        # read the GWAS file, study doc update with separator for the columns
        study = read_GWAS.init_reader(study)
        # identify the columns in the GWAS file, study doc updated with headers
        study = classify_columns.init_classifier(study)
        # call the stuff
        meta_doc.update(study)
    write_meta(meta_doc)

# if __name__ == '__main__':
#     # execute only if run as the entry point into the program
main()
