import simplejson as json
import logging
logger = logging.getLogger(__name__)


def update_meta(meta_doc, add_meta):
    meta_doc.update(add_meta)

    return meta_doc


def write_meta(json_doc):
    try:
        json.dump(json_doc, '../config.json')
    except AttributeError:
        logger.error('Not a dict, cannot write to json format')
    except Exception as e:
        logger.error('')
