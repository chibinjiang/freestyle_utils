import json
import traceback
from hashlib import sha1


def generate_sha1_image_name(url, logger=None):
    name = sha1(url.encode('utf-8')).hexdigest()
    try:
        postfix = url.split('/')[-1].split('.')[-1]
        postfix = postfix if postfix.endswith('g') else 'jpg'
        return name + '.' + postfix
    except Exception as e:
        if logger:
            logger.error("Wrong Image Url: {}".format(url))
            logger.error(traceback.format_exc())
        return name


def is_json(text):
    try:
        json.loads(text)
        return True
    except Exception:
        return False

