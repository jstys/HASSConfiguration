import logging

_logger = None

def set_logger(the_logger):
    global _logger
    
    _logger = the_logger
    FORMAT = "[%(filename)s - %(funcName)20s() ] %(message)s"
    formatter = logging.Formatter(fmt=FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    _logger.propagate = False
    _logger.addHandler(handler)
    
def log(message):
    if _logger:
        _logger.log(message)