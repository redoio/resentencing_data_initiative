from dotenv import load_dotenv
import os
import json
from dataclasses import dataclass    
from typing import List, Dict
from loguru import logger

load_dotenv()

@dataclass
class DevConfig:
    ENV_VARS = {
        "data_conn": os.getenv('DATA_CONN'),
        "config_file_path": os.getenv('CONFIG_FILE_PATH'),
        "pickle_input": os.getenv('PICKLE_INPUT'),
        "parallel": os.getenv('PARALLEL')
    }



@dataclass
class UserConfig:
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
    to_excel: bool
    id_label: str

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
        with open(DevConfig.ENV_VARS['config_file_path'], 'r') as config_file:
            all_config = json.load(config_file)
            loaded_config = UserConfig(**all_config.get(DevConfig.ENV_VARS['data_conn']))
        return loaded_config
    except Exception as e:
        logger.error(f"Failed to load config from {DevConfig.ENV_VARS['config_file_path']} - {e}")


# This is an instance of loaded config to be imported nad consumed further
config = load_config()
dev_config = DevConfig()