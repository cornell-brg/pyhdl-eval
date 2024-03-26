#=========================================================================
# conftest.py
#=========================================================================

def pytest_addoption(parser):

  parser.addoption( "--verilog", action="store", default=None,
                                 help="Verilog file name to test" )

  parser.addoption( "--pymtl",   action="store", default=None,
                                 help="PyMTL file name to test"   )

