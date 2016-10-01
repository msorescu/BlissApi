__author__ = 'msorescu'

import logging
import logging.config
import json


def get_log_config(**args):
    """
    return json that defines log info, in reality it can be in db or config file in S3
    :return:
    """
    log_config_json = '{'\
        '"version": 1,'\
        '"disable_existing_loggers": false,'\
        '"formatters": {'\
            '"simple": {'\
                '"format": "%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s"'\
            '}'\
        '},'\
        '"handlers": {'\
            '"console": {'\
                '"class": "logging.StreamHandler",'\
                '"level": "DEBUG",'\
                '"formatter": "simple",'\
                '"stream": "ext://sys.stdout"'\
            '},'\
            '"file_handler": {'\
                '"class": "logging.handlers.RotatingFileHandler",'\
                '"level": "DEBUG",'\
                '"formatter": "simple",'\
                '"filename": "log.log",'\
                '"maxBytes": 10485760,'\
                '"backupCount": 20,'\
                '"encoding": "utf8"'\
            '}'\
        '},'\
        '"root": {'\
            '"level": "DEBUG",'\
            '"handlers": ["console", "file_handler"]'\
        '}' \
        '}'

    log_setup = json.loads(log_config_json)

    return log_setup


def setup_logging(**args):
    log_cfg = get_log_config(**args)
    if log_cfg:

        if args['filename']:
            log_cfg['handlers']['file_handler']['filename'] = args['filename']

        logging.config.dictConfig(log_cfg)
        # this is kind of strange, cannot disable boto from a config
        if safe_val(args, 'boto_debug'):
            logging.getLogger('boto').setLevel(logging.DEBUG)
            logging.getLogger('botocore').setLevel(logging.DEBUG)
        else:
            logging.getLogger('boto').setLevel(logging.CRITICAL)
            logging.getLogger('botocore').setLevel(logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.DEBUG)

    if args['loglevel']:
        logging.disable(int(args['loglevel']))


def safe_val(data, name, def_val=None):
    return data[name] if name in data else def_val
