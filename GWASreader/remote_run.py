from GWASParse import check_n_correct
from SNPconformer import liftover
from SNPconformer import reference_check
from sys import argv
import pickle


def run():
    df = pickle.load(pk_df)
    study = pickle.load(pk_study)

    df, add_meta = check_n_correct.init(df, study)
    df = liftover.init(df, study)
    reference_check.init(df, study)

# # check and correct the GWAS file
# study = check_n_correct.init_check_correct(study)
# # make iterator in liftover and 1000ref
# study = liftover.iterator()
# stuy = reference_check.iterator()
# study = ''
# #call the stuff

if __name__ == "__main__":
    pk_df = argv[1]
    pk_study = argv[2]
    run()
