class Relation(list):
    def __init__(self, model):
        self.model = model

def start_traverse(helper, root, depth=3, history=None):
    history = history or {}
    return traverse(helper, root, depth, history)

def traverse(helper, model, life, history):
    history[str(model)] = Relation(model)
    for prop in helper.iterate_relationship_from_model(model):
        assoced = helper.model_from_property(prop)
        history[str(model)].append(helper.create_relation_item(model, prop, assoced))
        if life > 0 and str(assoced) not in history:
            traverse(helper, assoced, life-1, history)
    return history
