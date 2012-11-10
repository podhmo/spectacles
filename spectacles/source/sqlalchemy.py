from __future__ import absolute_import

import inspect
import sqlahelper
import sqlalchemy as sa

from ..utils import import_symbol

def setup(settings):
    engine = create_engine(settings.get("db.create_engine"), settings["db.url"]), 
    base = create_base(settings.get("db.base"))
    model_collector = ModelCollector(base)
    return {
        "name": "sqlalchemy", 
        "engine": engine, 
        "base": base, 
        "session": create_session(settings.get("db.session")), 
        "model_collector": model_collector
        }

def create_engine(create_engine_dotted, dburl):
    if create_engine_dotted:
        return import_symbol(create_engine_dotted)(dburl)
    else:
        engine = sa.create_engine(dburl)
        sqlahelper.add_engine(engine)
        return engine

def create_base(basedotted):
    """dotted = foo.bar:Base"""
    if basedotted:
        return import_symbol(basedotted)
    else:
        return sqlahelper.get_base()

def create_session(create_sessioin_dotted):
    if create_sessioin_dotted:
        return import_symbol(create_sessioin_dotted)
    else:
        return sqlahelper.get_session()

class ModelCollector(object):
    def __init__(self, baseclass):
        self.baseclass = baseclass

    def __call__(self, module):
        for k, v in vars(module).iteritems():
            if v != self.baseclass and inspect.isclass(v) and issubclass(v, self.baseclass):
                yield v
