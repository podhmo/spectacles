from spectacles.utils import import_symbol
import os
import re
import glob
import functools

import logging
logger = logging.getLogger(__name__)

def setup(settings):
    filewalk = FilewalkFinding(
        settings["startpoint"], 
        settings["filename.match"]
        )
    loader = FileModuleLoader(settings["module.base"])
    action = functools.partial(lookup_targets, filewalk, loader)
    return {
        "name": "filewalk", 
        "filewalk": filewalk, 
        "loader": loader, 
        "action": action, 
    }

def lookup_targets(walker, loader, *args, **kwargs):
    targets = walker(*args, **kwargs)
    return loader.loads(targets)

class FileModuleLoader(object):
    def __init__(self, module_base):
        self.module_base = module_base
        self.base_path = os.path.abspath(os.path.dirname(import_symbol(module_base).__file__))

    def _dotted_from_filepath(self, filepath):
        replaced = filepath.replace(self.base_path, self.module_base)
        if replaced == filepath:
            logger.warn("*finding.filewalk: %s is not matched with %s. ignored." % (filepath, self.base_path))
            return None
        return os.path.splitext(replaced)[0].replace("/", ".")

    def load(self, filepath):
        dotted = self._dotted_from_filepath(filepath)
        if dotted is None:
            return None
        return import_symbol(dotted)

    def loads(self, files):
        modules = [self.load(f) for f in files]
        return [m for m in modules if m]

class FilewalkFinding(object):
    def __init__(self, startpoint, matchname):
        self.startpoint = self._startpoint_convert(startpoint)
        self.matchname = matchname

    def _startpoint_convert(self, startpoint):
        if any(x == startpoint for x in ("*cwd*", ".")):
            return os.getcwd()
        else:
            return os.path.abspath(startpoint)

    def _find_with_rx(self, matchname):
        result = []        
        rx = re.compile(matchname)
        def finder(arg, dirname, fnames):
            for fname in fnames:
                if rx.search(fname):
                    result.append(os.path.join(dirname, fname))
        os.path.walk(self.startpoint, finder, None)
        return result

    def _find_with_string(self, matchname):
        result = []        
        def finder_strict(arg, dirname, fnames):
            for fname in fnames:
                if fname == matchname:
                    result.append(os.path.join(dirname, fname))
        os.path.walk(self.startpoint, finder_strict, None)
        return result

    def __call__(self, matchname=None):
        matchname = matchname or self.matchname
        if matchname.startswith("/") and matchname.endswith("/"):
            matchname = matchname[1:-1]
            return self._find_with_rx(matchname)
        elif "*" in matchname:
            pattern = os.path.join(self.startpoint, "**", matchname)
            return glob.glob(pattern)
        else:
            return self._find_with_string(matchname)
