
from collections import OrderedDict
from collections import defaultdict
from sqlalchemy.orm.properties import RelationshipProperty
import pprint as p


class Node(object):
    def __init__(self, v, parent=None):
        self.parent = parent
        self.v = v
        self.children = OrderedDict()

    def add(self, name, child):
        self.children[name] = child

    @property
    def iterate_children(self):
        return self.children.itervalues()

    def describe(self):
        return "[[%r, parent=%s, children=%s]]" % (self.v, self.parent.__class__,  self.children.keys())

class Relation(list):
    def __init__(self, model):
        self.model = model

def start_traverse(root, depth=3, history=None):
    history = history or {}
    node = Node(root)
    traverse(node, root, depth, history)
    return node, history

def traverse(node, model, life, history):
    history[str(model)] = Relation(model)

    for prop in model.__mapper__.iterate_properties:
        if isinstance(prop, RelationshipProperty):
            assoced = prop.mapper.class_
            child = Node(assoced, parent=node)
            node.add(str(prop), child)

            history[str(model)].append((str(prop), prop._dependency_processor, model, assoced))
            if life > 0 and str(assoced) not in history:
                traverse(child, assoced, life-1, history)
    return node

