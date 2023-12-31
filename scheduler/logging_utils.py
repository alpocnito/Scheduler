import logging

class CustomFormatter(logging.Formatter):
    """ Class for colorized and formatted output of logs """
    grey       = "\x1b[38;20m"
    blue       = "\x1b[34;20m"
    bold_green = "\x1b[32;1m"
    yellow     = "\x1b[33;20m"
    red        = "\x1b[31;20m"
    bold_red   = "\x1b[31;1m"
    reset      = "\x1b[0m"
    fmt = "%(message)s"

    FORMATS = {
        logging.DEBUG    : grey       + fmt + reset,
        logging.INFO     : blue       + fmt + reset,
        logging.WARNING  : bold_green + fmt + reset,
        logging.ERROR    : red        + fmt + reset,
        logging.CRITICAL : bold_red   + fmt + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_default_logger(logger_name: str):
    """
    Returns logger with the CustomFormatter and out in the stdout
    """

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter())

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

def get_file_logger(logger_name: str, file_name: str):
    """
    Returns logger with the CustomFormatter and out in the file
    """

    handler = logging.FileHandler(file_name)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter())

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
