import logging.config
import os
import re
import string
import sys
import random


def random_string_lowercase(size=6, chars=string.ascii_lowercase):
    return "".join(random.choice(chars) for _ in range(size))


def create_logger(log_file):
    # CRITICAL -> ERROR -> WARN -> INFO -> DEBUG
    # DEBUG means CRITICAL, ERROR, WARN, INFO, DEBUG
    logging_level = logging.DEBUG

    # create logger
    # log = logging.getLogger('__name__')
    log = logging.getLogger(random_string_lowercase())
    log.setLevel(logging_level)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file, mode="w")
    fh.setLevel(logging_level)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)

    # create formatter and add it to the handlers
    # noinspection SpellCheckingInspection
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-5s LN : %(lineno)-4d[ %(filename)-20s] [ %(funcName)-15s()] %(message)s",
        datefmt="%d-%b %I:%M:%S %p",
    )
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log



current_path = os.path.dirname(
    os.path.abspath(__file__)
)  # Get Current absolute path of this file

project_root_path = current_path
assert project_root_path is not None, print(
    "Unable to find the project root path : " + project_root_path
)
print("project_root_path : " + project_root_path)

log_file = None


if "win" in sys.platform:
    log_file = project_root_path + "\\" + "test.log"
else:
    log_file = project_root_path + "//" + "test.log"

logger = create_logger(log_file)
