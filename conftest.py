#=========================================================================
# conftest.py
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

#-------------------------------------------------------------------------
# pytest Command Line Options
#-------------------------------------------------------------------------

def pytest_addoption(parser):

  parser.addoption( "--verilog",  action="store", default=None,
                                  help="Verilog file name to test" )

  parser.addoption( "--pymtl",    action="store", default=None,
                                  help="PyMTL file name to test"   )

  parser.addoption( "--pyrtl",    action="store", default=None,
                                  help="PyRTL file name to test"   )

  parser.addoption( "--myhdl",    action="store", default=None,
                                  help="MyHDL file name to test"   )

  parser.addoption( "--migen",    action="store", default=None,
                                  help="Migen file name to test"   )

  parser.addoption( "--amaranth", action="store", default=None,
                                  help="Amaranth file name to test"   )

#-------------------------------------------------------------------------
# Assertion Rewriting
#-------------------------------------------------------------------------
# Enable assertion rewriting in our pyhdl_eval test harness

pytest.register_assert_rewrite("pyhdl_eval.core")

#-------------------------------------------------------------------------
# multi_reset
#-------------------------------------------------------------------------
# PyRTL can only reset a module at the very beginning of the simulation,
# but some of our tests reset a module multiple times during a simulat.
# We need to mark these tests and skip them when using PyRTL.

def pytest_configure(config):
  config.addinivalue_line(
    "markers", "multi_reset: mark test with multiple resets in single simulation" )

def pytest_collection_modifyitems(config, items):
  if config.getoption("pyrtl"):
    skip_multi_reset = pytest.mark.skip(
      reason="PyRTL cannot handle multiple resets in single simulation" )
    for item in items:
      if "multi_reset" in item.keywords:
        item.add_marker(skip_multi_reset)

