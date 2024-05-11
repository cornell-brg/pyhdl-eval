#=========================================================================
# Prob03p13_comb_gates_nl1_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.in3 = InPort()
    s.out = OutPort()

    @update
    def up():
      s.out @= (~s.in0 | s.in1) & (s.in2 | ~s.in3)

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.in3 = InPort()
    s.out = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,in2,in3 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, dut.in1, dut.in2, dut.in3, ">", dut.out )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0,0),
    (0,0,0,1),
    (0,0,1,0),
    (0,0,1,1),
    (0,1,0,0),
    (0,1,0,1),
    (0,1,1,0),
    (0,1,1,1),

    (1,0,0,0),
    (1,0,0,1),
    (1,0,1,0),
    (1,0,1,1),
    (1,1,0,0),
    (1,1,0,1),
    (1,1,1,0),
    (1,1,1,1),
  ])

