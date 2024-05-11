#=========================================================================
# Prob01p01_comb_const_zero_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.zero = OutPort()
    s.zero //= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.zero = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  ref.sim_eval_combinational()
  dut.sim_eval_combinational()

  print_line_trace( dut, dut.zero )

  assert ref.zero == dut.zero

  ref.sim_tick()
  dut.sim_tick()

  ref.sim_eval_combinational()
  dut.sim_eval_combinational()

  print_line_trace( dut, dut.zero )

  assert ref.zero == dut.zero

  ref.sim_tick()
  dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig )

