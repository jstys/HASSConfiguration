import logging
import datetime
import api_handle

    
def debug(message):
    logger: logging.Logger = api_handle.instance.get_main_log()
    filename, lineNumber, funcName, stackInfo = logger.findCaller()
    timestamp = datetime.datetime.now()
    logger.debug(f"DEBUG {timestamp} - [{filename} - {funcName}] {message}")
    
def info(message):
    logger: logging.Logger = api_handle.instance.get_main_log()
    filename, lineNumber, funcName, stackInfo = logger.findCaller()
    timestamp = datetime.datetime.now()
    logger.info(f"INFO {timestamp} - [{filename} - {funcName}] {message}")
    
        
def warning(message):
    logger: logging.Logger = api_handle.instance.get_main_log()
    filename, lineNumber, funcName, stackInfo = logger.findCaller()
    timestamp = datetime.datetime.now()
    logger.warning(f"WARN {timestamp} - [{filename} - {funcName}] {message}")
    

def error(message):
    logger: logging.Logger = api_handle.instance.get_main_log()
    filename, lineNumber, funcName, stackInfo = logger.findCaller()
    timestamp = datetime.datetime.now()
    logger.error(f"ERROR {timestamp} - [{filename} - {funcName}] {message}")
    

def critical(message):
    logger: logging.Logger = api_handle.instance.get_main_log()
    filename, lineNumber, funcName, stackInfo = logger.findCaller()
    timestamp = datetime.datetime.now()
    logger.critical(f"CRIT {timestamp} - [{filename} - {funcName}] {message}")
    
        
def set_level(level):
    logger: logging.Logger = api_handle.instance.get_main_log()
    logger.warning(f"Setting level to {level}")
    if logger and level.lower() == "debug":
        logger.setLevel("DEBUG")
    if logger and level.lower() == "normal":
        logger.setLevel("INFO")