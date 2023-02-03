import logging, logging.handlers

def get_configured_logger(name=None):
    logger = logging.getLogger(name) if name!=None else logging.getLogger()
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # Create RotatingFileHandler
        import os
        formatter = "%(asctime)s %(levelname)s %(process)s %(thread)s %(filename)s %(funcName)s():%(lineno)d %(message)s"
        fhandler = logging.handlers.RotatingFileHandler('app.log', maxBytes = 1024*1024*10, backupCount = 6)
        fhandler.setFormatter(logging.Formatter(formatter))
        fhandler.setLevel(logging.INFO)
        
        fhandler_d = logging.handlers.RotatingFileHandler('app_debug.log', maxBytes = 1024*1024*10, backupCount = 2)
        fhandler_d.setFormatter(logging.Formatter(formatter))
        fhandler_d.setLevel(logging.DEBUG)

        chandler = logging.StreamHandler()
        chandler.setLevel(logging.DEBUG)

        logger.addHandler(fhandler)
        logger.addHandler(fhandler_d)
        logger.addHandler(chandler)
        logger.setLevel(logging.DEBUG)
    else:
        pass
    return logger