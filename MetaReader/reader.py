import simplejson as json
import logging
from json.decoder import JSONDecodeError
from MetaReader.config import study

logger = logging.getLogger(__name__)

def read_meta(path):
    try:
        with open(path) as json_file:
            meta_file = json.load(json_file)
        # for all the studies in the meta data file
        return meta_file
    except FileNotFoundError:
        logger.info('meta_study file not found')
    except JSONDecodeError:
        logger.info('problem loading meta data json file')


def meta_studies(path):
    files = list()
    try:
        meta_file = read_meta(path)
        for studyID in meta_file:
            study_path = studyID.get('path')
            study_size = studyID.get('study_size')
            this_study = study(studyID, study_path, study_size)
            study_lambda = studyID.get('lambda')
            if study_lambda:
                this_study.set_lambda(study_lambda)
            corr_factor = studyID.get('corr_factor')
            if corr_factor:
                this_study.set_correction(corr_factor)
            eff_size = studyID.get('eff_size')
            if eff_size:
                this_study.set_sum_eff(eff_size)
            # append study objects to a list
            files.append(this_study)
        # return the list with study objects
        return files
    except Exception as e:
        logger.info('')