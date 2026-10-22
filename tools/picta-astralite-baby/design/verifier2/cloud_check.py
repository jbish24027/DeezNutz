import sys, numpy as np
sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('m','indep_model.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
from indep_model import *
