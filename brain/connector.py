#!/usr/bin/env python3
from datadog import initialize, api
from configparser import ConfigParser
from pathlib import Path

def api(config_file='ddctl.conf'):
    # Pulling in API and APP Token from config
    try:
        config_file_check = Path(config_file)
        if config_file_check.is_file():
            config = ConfigParser()
            config.read(config_file)
            api_key  = config['ddctl']['api_key']
            app_key  = config['ddctl']['app_key']
            dd_login = config['ddctl']['dd_login']
        else:
            raise SystemExit("Config file not found at {}".format(config))
    except Exception as err:
        raise SystemExit("There is an issue near {} in the config.".format(err))
    # Initialize the connection
    options = {'api_key': api_key, 'app_key': app_key}
    try:
        initialize(**options)
    except Exception as err:
        raise SystemExit("Unable to initialize due to: {}".format(err))
    return {'api_key': api_key, 'app_key': app_key, 'dd_login': dd_login}
