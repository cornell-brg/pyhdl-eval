#=========================================================================
# Prob05p01_comb_mux_1b_2to1_test
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
    s.sel = InPort()
    s.out = OutPort()

    @update
    def up():
      if s.sel == 0:
        s.out @= s.in0
      else:
        s.out @= s.in1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.sel = InPort()
    s.out = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,sel = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.sel @= sel

    dut.in0 @= in0
    dut.in1 @= in1
    dut.sel @= sel

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (0,1,1),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,1,1),
  ])

