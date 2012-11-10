from ConfigParser import SafeConfigParser
from .utils import import_spectacles_symbol
from .utils import subsettings

_section = "spectacles"

def dict_from_config_file(settings_file, section=_section):
    with open(settings_file) as rf:
        config = SafeConfigParser()
        config.readfp(rf)
        return dict(config.items(section))

class Config(dict):
    def __init__(self, _kwargs=None, **kwargs):
        self._kwargs = _kwargs.copy() if _kwargs else {}
        self._kwargs.update(kwargs)
        self.setup(self._kwargs)

    def section_setup(self, settings, section, option_name):
        dottedname = "%s.%s:setup" % (section, settings[option_name])
        self[section] = import_spectacles_symbol(dottedname)(subsettings(settings, section))

    def setup(self, settings):
        self.section_setup(settings, "source", "source.orm")
        self.section_setup(settings, "finding", "finding.strategy")
        self.section_setup(settings, "rendering", "rendering.strategy")


def read_config_file(settings_file, section=_section):
    return read_config(dict_from_config_file(settings_file, section=section))

def read_config(setting):
    return Config(setting)

