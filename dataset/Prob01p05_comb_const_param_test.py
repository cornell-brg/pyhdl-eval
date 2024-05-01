#=========================================================================
# Prob01p05_comb_const_param_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s, nbits, value ):
    s.out = OutPort(nbits)
    s.out //= value

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits, value ):
    s.out = OutPort(nbits)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, nbits, value ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nbits=nbits, value=value )

  ref.sim_tick()
  dut.sim_tick()

  assert ref.out == dut.out

  ref.sim_tick()
  dut.sim_tick()

  assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig, nbits=8, value=0xef )

#-------------------------------------------------------------------------
# test_case_nbits32_directed
#-------------------------------------------------------------------------

def test_case_nbits32_directed( pytestconfig ):
  run_sim( pytestconfig, nbits=32, value=0xcafecafe )

