_logger = None

def set_logger(the_logger):
    _logger = the_logger
    
def log(message):
    if _logger:
        _logger.log(message)