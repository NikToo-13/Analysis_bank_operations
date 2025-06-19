import logging

from project_sys import PATH_HOME

path_ = f"{PATH_HOME}/logs/services.log"
logger = logging.getLogger("services")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)