import logging
import datetime
import sys

logger_map = {}

def get_logger(name):
    global logger_map
    logger = None
    if name in logger_map:
        wrapper = logger_map[name]
    else:
        logger = logging.getLogger(name)
        handler = logging.StreamHandler(sys.stdout)
        logger.handlers = []
        logger.addHandler(handler)
        wrapper = LogWrapper(logger)
        wrapper.set_level("normal") # Default to normal
        logger_map[name] = wrapper
        
    return wrapper

class LogWrapper(object):
    def __init__(self, logger):
        self.logger = logger
    
    def debug(self, message):
        if self.logger:
            filename, lineNumber, funcName, stackInfo = self.logger.findCaller()
            timestamp = datetime.datetime.now()
            self.logger.debug(f"DEBUG {timestamp} - [{filename} - {funcName}] {message}")
        
    def info(self, message):
        if self.logger:
            filename, lineNumber, funcName, stackInfo = self.logger.findCaller()
            timestamp = datetime.datetime.now()
            self.logger.info(f"INFO {timestamp} - [{filename} - {funcName}] {message}")
        
            
    def warning(self, message):
        if self.logger:
            filename, lineNumber, funcName, stackInfo = self.logger.findCaller()
            timestamp = datetime.datetime.now()
            self.logger.warning(f"WARN {timestamp} - [{filename} - {funcName}] {message}")
        
    
    def error(self, message):
        if self.logger:
            filename, lineNumber, funcName, stackInfo = self.logger.findCaller()
            timestamp = datetime.datetime.now()
            self.logger.error(f"ERROR {timestamp} - [{filename} - {funcName}] {message}")
        
    
    def critical(self, message):
        if self.logger:
            filename, lineNumber, funcName, stackInfo = self.logger.findCaller()
            timestamp = datetime.datetime.now()
            self.logger.critical(f"CRIT {timestamp} - [{filename} - {funcName}] {message}")
        
            
    def set_level(self, level):
        self.logger.warning(f"Setting level to {level}")
        if self.logger and level.lower() == "debug":
            self.logger.setLevel("DEBUG")
        if self.logger and level.lower() == "normal":
            self.logger.setLevel("INFO")