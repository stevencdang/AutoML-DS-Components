
# Author: Steven C. Dang

# Convenience class and functions for supporting reading in configuration files

import logging
import configparser
import os

# logging.basicConfig()
logger = logging.getLogger(__name__)

class SettingsFactory(object):

    @staticmethod
    def get_settings(cfg_path=None, program_dir=None, working_dir=None):
        if os.environ.get(D3MSettings.__config_path_var__) is not None:
            return D3MSettings(cfg_path, program_dir, working_dir)
        else:
            return Settings(cfg_path, program_dir, working_dir)

class Settings(object):
    """
    A generic settings class including a few operators for reading in configuration files

    """
    def __init__(self, cfg_path=None, program_dir=None, working_dir=None):
        self.cfg_file = cfg_path
        self.cfg = configparser.ConfigParser()
        self.program_dir = program_dir
        self.working_dir = working_dir

        if cfg_path is None:
            self.cfg.read('settings.cfg')
        else:
            self.cfg.read(cfg_path)



    def parse_config(self):
        """
        Parse a given config file

        """
        
        cfg = {
            'dataset_dir': self.cfg.get('Dataset', 'dataset_dir'),
            'dataset_json': self.cfg.get('Dataset', 'dataset_json'),
            'out_file': self.cfg.get('Dataset', 'out_file'),
            'log_level': logging.getLevelName(self.cfg.get('Logging', 'log_level')),
            'enable_syslog': self.cfg.getboolean('Logging', 'enable_syslog'),
            'enable_file_log': self.cfg.getboolean('Logging', 'enable_file_log'),
            'file_log_path': self.cfg.get('Logging', 'file_log_path') 
        }
        return cfg

    def parse_logging(self):
        """
        Parse only settings from the logging part of the config

        """
        cfg = {
            'log_level': logging.getLevelName(self.cfg.get('Logging', 'log_level')),
            'enable_syslog': self.cfg.getboolean('Logging', 'enable_syslog'),
            'enable_file_log': self.cfg.getboolean('Logging', 'enable_file_log'),
            # 'file_log_path': self.cfg.get('Logging', 'file_log_path') 
            'file_log_path': os.path.join(self.working_dir)
        }

        return cfg


    def get(self, sect, key):
        """
        Manually retrieve specific configuration from settings. Basically a wrapper around
        configparser.get()

        """
        return self.cfg.get(sect, key)


class D3MSettings(Settings):

    __config_path_var__="D3MCONFIG"

    def __init__(self, cfg_path=None, program_dir=None, working_dir=None):
        super().__init__(cfg_path, program_dir, working_dir)

    
    def parse_logging(self):
        """
        Parse only settings from the logging part of the config

        """
        cfg = super().parse_logging()
        # Override logging level settings for deployment to d3m environments
        cfg['log_level'] =logging.INFO
        return cfg
