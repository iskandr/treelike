import sys
import time 

import numpy as np
from nose.tools import nottest

def run_local_functions(prefix, locals_dict = None):
  if locals_dict is None:
    last_frame = sys._getframe()
    locals_dict = last_frame.f_back.f_locals

  good = set([])
  # bad = set([])
  for k, test in locals_dict.iteritems():
    if k.startswith(prefix):
      print "Running %s..." % k
      try:
        test()
        print "\n --- %s passed\n" % k
        good.add(k)
      except:
        raise

  print "\n%d tests passed: %s\n" % (len(good), ", ".join(good))

@nottest
def run_local_tests(locals_dict = None):
  if locals_dict is None:
    last_frame = sys._getframe()
    locals_dict = last_frame.f_back.f_locals
  return run_local_functions("test_", locals_dict)

def eq(x,y):
  if isinstance(x, np.ndarray) and not isinstance(y, np.ndarray):
    return False
  if isinstance(y, np.ndarray):
    if isinstance(x, np.ndarray) and x.shape == y.shape:
      err = abs(np.mean(np.ravel(x) - np.ravel(y)))
      m = abs(np.mean(np.ravel(x)))
      if not np.all(np.ravel(x) == np.ravel(y)) and err/m > 0.000001:
        print "err:", err
        print "err/m:", err/m
        return False
      else:
        return True
  elif np.isscalar(x) and np.isnan(x):
    return np.isscalar(x) and np.isnan(y)
  else:
    return np.allclose(x,y)
  
def expect_eq(actual,expected):
  assert eq(actual,expected), "Expected %s but got %s" % (expected,actual)
  
def copy(x):
  if isinstance(x, np.ndarray):
    return x.copy()
  else:
    return x
