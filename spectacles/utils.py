import pkg_resources

def import_symbol(symbol): #todo cache
    return pkg_resources.EntryPoint.parse("x=%s" % symbol).load(False)

def import_spectacles_symbol(symbol):
    dotted = "spectacles.%s" % (symbol)
    return import_symbol(dotted)

##
def subsettings(D, section):
    return {k.split(".", 1)[1]:v for k, v in D.iteritems() if k.startswith(section)}
