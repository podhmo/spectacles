import inspect
import sqlahelper
import functools
from sqlalchemy.orm.properties import RelationshipProperty
import sqlalchemy as sa
from zope.interface import provider

from ..interfaces import ITraversingHelper


from ..utils import import_symbol
from ..traversing import start_traverse as start_traverse_original


def setup(settings):
    engine = create_engine(settings.get("db.create_engine"), settings["db.url"]), 
    base = create_base(settings.get("db.base"))

    model_collector = functools.partial(collect_model, base)
    start_traverse = functools.partial(start_traverse_original, TraversingHelper)
    return {
        "name": "sqlalchemy", 
        "engine": engine, 
        "base": base, 
        "session": create_session(settings.get("db.session")), 
        "action.collect_models": model_collector, 
        "action.collect_properties": lambda m: m.__mapper__.iterate_properties, 
        "action.relationship_from_models": start_traverse
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

def collect_model(baseclass, module):
    for k, v in vars(module).iteritems():
        if v != baseclass and inspect.isclass(v) and issubclass(v, baseclass):
            yield v

## traverse
@provider(ITraversingHelper)
class TraversingHelper(object):
    @classmethod
    def iterate_relationship_from_model(cls, model):
        for prop in model.__mapper__.iterate_properties:
            if isinstance(prop, RelationshipProperty):
                yield prop
                
    @classmethod
    def model_from_property(cls, prop):
        return prop.mapper.class_

    @classmethod
    def create_relation_item(cls, parent_model, prop, model):
        return str(prop), prop._dependency_processor, parent_model, model

