from GWASParse import check_n_correct
from MetaReader import reader
# from SNPconformer import liftover
# from SNPconformer import reference_check

def run():
    config_path = "/home/sevvy/PycharmProjects/CardioDiscover/test_config.json"
    studies = reader.meta_studies(config_path)

    for study in studies:

    study = check_n_correct.init()
# # check and correct the GWAS file
# study = check_n_correct.init_check_correct(study)
# # make iterator in liftover and 1000ref
# study = liftover.iterator()
# stuy = reference_check.iterator()
# study = ''
# #call the stuff