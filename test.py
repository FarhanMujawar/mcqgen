import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from mcqgenerator.logger import logging

logging.info("This is a test log message to check the logger configuration.")