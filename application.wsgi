import sys
import logging

logging.basicConfig(stream=sys.stderr)

activate_this = '/var/www/data-miner/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/var/www/data-miner/data-miner')
from main import app as application

