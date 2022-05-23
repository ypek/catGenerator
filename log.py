import configparser
import logging
import sys
from logging import FileHandler

FORMATTER = logging.Formatter('[%(asctime)s | %(levelname)s]: %(message)s', datefmt='%m.%d.%Y %H:%M:%S')

config = configparser.ConfigParser()
config.read('config.ini')
LOG_FILE = config.get('LOG', 'PATH')


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = FileHandler(LOG_FILE)
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # melhor ter muito log do que não ter
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # com esse patern raramente é necessário remover o handler, mas como é um arquivo, é necessário remover! ^^
    logger.propagate = False
    return logger
