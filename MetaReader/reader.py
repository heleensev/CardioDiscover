import simplejson as json
import sys, copy, logging
from json.decoder import JSONDecodeError
from MetaReader.config import Study, Preferences

logger = logging.getLogger(__name__)

# required attributes, if not
meta_req_attributes = {'studyID', 'path', 'n_studies', 'phenotype'}

meta_attributes = {'path': Study.set_path, 'n_studies': Study.set_study_size, 'phenotype': Study.set_phenotype,
                   'separator': Study.set_sep, 'headers': Study.set_headers, 'chunk_size': Study.set_chunksize,
                   'num_variants': Study.set_num_variants, 'lambda': Study.set_lambda, 'build': Study.set_build,
                   'ethnicity': Study.set_ethnicity, 'header_idx': Study.set_indices,
                   'corr_factor': Study.set_correction, 'sum_eff': Study.set_sum_eff}


def read_meta(path):
    try:
        with open(path) as json_file:
            meta_json = json.load(json_file, encoding='utf-8')[0]
        # for all the studies in the meta data file
        study_info = meta_json.get('study_info')
        pref_info = meta_json.get('preferences')
        check_meta(study_info)
        return meta_json, study_info, pref_info
    except FileNotFoundError:
        print('study meta data file not found')
        raise Exception
    except JSONDecodeError:
        print('problem loading meta data json file')
        raise Exception
    except Exception as e:
        print(e)
        sys.exit(1)


def check_meta(meta_file):
    try:
        # all the unique keys from the meta (json) file
        meta_keys = set([key for dic in meta_file for key in dic])
        # set with all the attributes that may be present in the meta file
        all_attr = copy.deepcopy(set(meta_attributes))
        all_attr.update(meta_req_attributes)
        # check if the required attributes are present in the file
        if not set(meta_req_attributes).issubset(meta_keys):
            raise Exception('Required attributes: path, size, phenotype not present')
        elif not meta_keys.issubset(all_attr):
            raise Exception('Unexpected attributes present in file')
        return True
    except Exception as e:
        print(e)
        sys.exit(1)


def set_preferences(pref_info):
    options = {'hpc': Preferences.set_hpc}
    prefs = Preferences()
    for pref in pref_info:
        if pref in options:
            options.get(pref)(prefs, pref)
    return prefs


def meta_studies(path):
    studies = list()
    try:
        _, study_info, pref_info = read_meta(path)
        prefs = set_preferences(pref_info)

        for GWAS in study_info:
            studyID = GWAS.get('studyID')
            this_study = Study(studyID)
            for attr in meta_attributes:
                param = GWAS.get(attr)
                # if study parameter is in meta file
                if param:
                    # call the setters for the parameters
                    meta_attributes.get(attr)(this_study, param)
            # append study objects to a list
            studies.append(this_study)
        # return the list with study objects
        return studies, prefs
    except Exception as e:
        print(e)
