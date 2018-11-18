import logging

# Setup flask logger to also follow gunicorn logger setup
gunicorn_logger = logging.getLogger('gunicorn.error')

logger = logging.getLogger('Houdini')
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)
