import logging


def debug(*message):
    # pass
    # print "------------   ",datetime.now(), message
    log(logging.DEBUG, *message)


def log(level, *message):
    logging.log(level, message)