#=========================================================================
# test_utils
#=========================================================================

import types
import pathlib

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from importlib.machinery import SourceFileLoader

#-------------------------------------------------------------------------
# construct
#-------------------------------------------------------------------------

def construct( pytestconfig, python_file_name, RefModule, TopModule, **kwargs ):

  # Instantiate, elaborate, reset the reference model

  ref = RefModule(**kwargs)
  ref.apply( DefaultPassGroup() )
  ref.sim_reset()

  # Instantiate, elaborate, reset the design under test

  dut = None

  # If the design under test is a PyMTL model ...

  if pytestconfig.getoption("pymtl"):

    loader = SourceFileLoader("TopModule",pytestconfig.getoption("pymtl"))
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    dut = mod.TopModule(**kwargs)

    dut.apply( DefaultPassGroup(linetrace=True) )
    dut.sim_reset()

  # ... otherwise the design under test is a Verilog model

  else:

    dut = TopModule(**kwargs)

    # If no verilog file name is supplied, use Verilog reference

    vin_file_name = pytestconfig.getoption("verilog")
    if not vin_file_name:
      dut.set_metadata( VerilogPlaceholderPass.top_module, "RefModule" )
      assert python_file_name.endswith("_test.py")
      vin_file_name = python_file_name.replace("_test.py","_ref.v")

    # Append parameters as string to ensure filename is unique
    vout_prob_name = pathlib.Path(vin_file_name).stem
    for key,value in kwargs.items():
      vout_prob_name += "_" + key + "_" + str(value)

    vout_file_name = vout_prob_name + "_translated.v"
    print(vout_prob_name)
    print(vout_file_name)

    dut.set_metadata( VerilogPlaceholderPass.src_file, vin_file_name )
    dut.set_metadata( VerilogTranslationImportPass.enable, True )
    dut.set_metadata( VerilogTranslationPass.explicit_file_name, vout_file_name )
    dut.set_metadata( VerilogTranslationPass.explicit_module_name, vout_prob_name )
    dut.apply( VerilogPlaceholderPass() )
    dut = VerilogTranslationImportPass()( dut )
    dut.apply( DefaultPassGroup(linetrace=True) )
    dut.sim_reset()

  return ref,dut

