#=========================================================================
# Prob01p03_comb_const_lohi_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.lo = OutPort()
    s.hi = OutPort()
    s.lo //= 0
    s.hi //= 1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.lo = OutPort()
    s.hi = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  ref.sim_tick()
  dut.sim_tick()

  assert ref.lo == dut.lo
  assert ref.hi == dut.hi

  ref.sim_tick()
  dut.sim_tick()

  assert ref.lo == dut.lo
  assert ref.hi == dut.hi

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig )

