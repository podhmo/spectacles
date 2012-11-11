from zope.interface import Interface

class ITraversingHelper(Interface):
    def iterate_relationship_from_model(model):
        pass

    def model_from_property(prop):
        pass

    def create_relation_item(parent_model, prop, child_model):
        pass
