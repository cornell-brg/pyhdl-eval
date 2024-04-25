#=========================================================================
# Prob03p10_comb_gates_nl0_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.out = OutPort()

    @update
    def up():
      s.out @= ~(s.in0 ^ s.in1) & s.in2

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.out = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,in2 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, [
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (0,1,1),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,1,1),
  ] )

