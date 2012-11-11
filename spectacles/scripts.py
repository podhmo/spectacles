from spectacles.config_parse import read_config_file
from collections import OrderedDict

def grouping(xs, f):
    D = OrderedDict()
    for x in xs:
        k = f(x)
        if not k in D:
            D[k] = []
        D[k].append(x)
    return D

def listing_models(context):
    modules = context["finding"]["action.load_modules"]()
    models = []
    for module in modules:
        models.extend(context["source"]["action.collect_models"](module))

    grouped = grouping(set(models), lambda m: m.__module__)
    for module_name,  models in grouped.iteritems():
        for model in models:
            print "%s.%s" % (module_name, model.__name__)

class Match(Exception):
    pass

def listing_properties(context, modelname):
    modules = context["finding"]["action.load_modules"]()
    matched_model = None

    try:
        for module in modules:
            for model in context["source"]["action.collect_models"](module):
                if model.__name__ == modelname:
                    matched_model = model
                    raise Match
    except Match:
        pass

    for prop in context["source"]["action.collect_properties"](matched_model):
        print prop

def main():
    context = read_config_file("./demo.cfg")
    modules = context["finding"]["action.load_modules"]("models.py")
    models = list(context["source"]["action.collect_models"](modules[0]))
    print context["source"]["action.relationship_from_models"](models[0], depth=1)
    

if __name__ == "__main__":
    # main()
    # context = read_config_file("./demo.cfg")
    # listing_models(context)
    # listing_properties(context, "Layout")
    pass
