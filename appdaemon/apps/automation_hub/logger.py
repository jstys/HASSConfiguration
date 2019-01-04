import logging

_logger = None

def set_logger(the_logger):
    global _logger
    
    _logger = the_logger
    # FORMAT = "[%(filename)s - %(funcName)20s() ] %(message)s"
    # formatter = logging.Formatter(fmt=FORMAT)
    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)
    # _logger.handlers = []
    # _logger.addHandler(handler)

def debug(message):
    if _logger:
        _logger.debug(message)
    
def info(message):
    if _logger:
        _logger.info(message)
        
def warning(message):
    if _logger:
        _logger.warning(message)

def error(message):
    if _logger:
        _logger.error(message)

def critical(message):
    if _logger:
        _logger.critical(message)