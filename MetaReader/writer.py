import simplejson as json
import logging
logger = logging.getLogger(__name__)


def update_meta(meta_doc, add_meta):
    # maybe perform some sanity checks?
    meta_doc.update(add_meta)
    return meta_doc


def write_meta(json_doc):
    try:
        json.dump(json_doc, '../')
    except Exception as e:
        logger.error('Error writing json doc to file')
