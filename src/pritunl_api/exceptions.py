import logging as log


# Error exception handler
class PritunlErr(Exception):
    def __init__(self, msg):
        log.error(msg)
        pass
