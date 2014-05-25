import logging
import graypy

my_logger = logging.getLogger('test_logger')
my_logger.setLevel(logging.DEBUG)

handler = graypy.GELFHandler('127.0.0.1', 12201)
my_logger.addHandler(handler)

my_logger.debug('Hello Graylog2.')
