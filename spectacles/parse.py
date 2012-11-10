from ConfigParser import SafeConfigParser

def read_config_file(settings_file):
    config = SafeConfigParser.read_fp(settings_file)
    return config

def read_config(settings):
    config = SafeConfigParser

