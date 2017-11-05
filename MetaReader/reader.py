import simplejson as json
import sys, copy, logging
from json.decoder import JSONDecodeError
from MetaReader.config import study

logger = logging.getLogger(__name__)

# required attributes, if not
meta_req_attributes = {'path', 'size', 'phenotype'}

meta_attributes = {'path': study.set_path, 'size': study.set_study_size, 'phenotype': study.set_phenotype,
                   'sep': study.set_sep, 'headers': study.set_headers, 'num_variants': study.set_num_variants,
                   'lambda': study.set_lambda, 'corr_factor': study.set_correction, 'sum_eff': study.set_sum_eff
                   }


def read_meta(path):
    try:
        with open(path) as json_file:
            meta_file = json.load(json_file)
        # for all the studies in the meta data file
        check_meta(meta_file)
        return meta_file
    except FileNotFoundError:
        print('study meta data file not found')
    except JSONDecodeError:
        print('problem loading meta data json file')
    except Exception as e:
        print(e)
    finally:
        sys.exit(1)


def check_meta(meta_file):
    try:
        meta_keys = set(meta_file)
        # set with all the attributes that may be present in the meta file
        all_attr = copy.deepcopy(meta_req_attributes)
        set(all_attr).update(meta_keys)

        # check if the required attributes are present in the file
        if meta_req_attributes.difference(meta_keys):
            raise Exception('Required attributes: path, size, phenotype not present')
        elif meta_keys.difference(all_attr):
            raise Exception('Unexpected attributes present in file')
        return True
    except Exception as e:
        print(e)
        sys.exit(1)


def meta_studies(path):
    files = list()
    try:
        meta_file = read_meta(path)
        for studyID in meta_file:
            this_study = study(studyID)
            for attr in meta_attributes:
                study_param = studyID.get(attr)
                if study_param:
                    meta_attributes.get(attr)(this_study)
            # append study objects to a list
            files.append(this_study)
        # return the list with study objects
        return files
    except Exception as e:
        print(e)