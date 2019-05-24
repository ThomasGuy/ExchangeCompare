"""initalize package 'ticker' setting up logging"""
import logging
import os

from .async_rest.compare import Compare
from .start import main
# pylint: disable=C0103
current_dir = os.path.dirname(os.path.realpath(__file__))
package_dir = os.path.realpath(os.path.join(current_dir, os.pardir))

Name = 'ticker'

# Create a custom logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('.\\logs\\ticker.log', mode='w')

c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%b-%d %X')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the log
log.addHandler(c_handler)
log.addHandler(f_handler)

log.info('Admin Logged in now...')
# pylint: enable=C0103
