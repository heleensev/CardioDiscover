import simplejson as json
import logging
logger = logging.getLogger(__name__)

def update_meta(json_doc):
    # update with doc
    pass
    return json_doc


def write_meta(json_doc):
    try:
        json.dump(json_doc, '../')
    except Exception as e:
        logger.error('Error writing json doc to file')
