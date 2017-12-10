import simplejson as json
import logging
import traceback
logger = logging.getLogger(__name__)


def update_meta(meta_doc, study_list):
    meta_doc['study_info'] = study_list

    return meta_doc


def write_meta(json_doc, path):
    print(json_doc)
    try:
        with open(path, 'w') as config:
            json.dump(json_doc, config, indent=4)
        flat = json.dumps(json_doc)
        file = open('newjson.json', 'w')
        file.write(flat)
        file.close()
    except AttributeError:
        logger.error('Not a dict, cannot write to json format')
    except Exception:
        logger.error(traceback.format_exc())
