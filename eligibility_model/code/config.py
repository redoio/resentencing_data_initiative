from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass    
from typing import List, Dict
from loguru import logger

load_dotenv()

DATA_CONN = os.getenv('DATA_CONN')
CONFIG_FILE_PATH = os.getenv('CONFIG_FILE_PATH')


@dataclass
class Config:
    """
    This dataclass defines all the plausible fields required in a config, as to be
    intilaized on successful loadig of the config.
    """
    county_name: str
    month: List[str]
    naming_convention: str
    read_data_path: str
    comp_path: Dict
    comp_info: List
    write_data_path: str
    pickle_input: bool
    to_excel: bool
    id_label: str
    parallel: bool

    def __post_init__(self):
        self.month = '/'.join(self.month)


def load_config():
    """
    This method is responsible for loading the config JSON file from the path
    provided in env variable and also retrieving the applicable config based on
    the data connection env variable.

    Parameters
    ----------
    None

    Returns
    -------
    loaded_config : instace of Config
        Object of Config dataclass containing all the input configurations required,
        as per provided data connection.

    """
    try:
        loaded_config = None
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            all_config = json.load(config_file)
            loaded_config = Config(**all_config.get(DATA_CONN))
        return loaded_config
    except Exception as e:
        logger.error(f"Failed to load config from {CONFIG_FILE_PATH} - {e}")


# This is an instance of loaded config to be imported nad consumed further
config = load_config()
