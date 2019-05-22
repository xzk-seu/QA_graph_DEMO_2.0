import logging
import logging.handlers
import datetime

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

all_handler = logging.handlers.TimedRotatingFileHandler('all.log', when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
all_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

# error_handler = logging.FileHandler('error.log')
screen_handler = logging.StreamHandler()
screen_handler.setLevel(logging.INFO)
screen_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(all_handler)
logger.addHandler(screen_handler)
logger.addHandler(error_handler)

# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warning message')
# logger.error('error message')
# logger.critical('critical message')
