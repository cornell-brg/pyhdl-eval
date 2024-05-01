#=========================================================================
# Prob03p07_comb_gates_4_input_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in0      = InPort()
    s.in1      = InPort()
    s.in2      = InPort()
    s.in3      = InPort()
    s.out_and  = OutPort()
    s.out_nand = OutPort()
    s.out_or   = OutPort()
    s.out_nor  = OutPort()

    @update
    def up():
      s.out_and  @=    s.in0 & s.in1 & s.in2 & s.in3
      s.out_nand @= ~( s.in0 & s.in1 & s.in2 & s.in3 )
      s.out_or   @=    s.in0 | s.in1 | s.in2 | s.in3
      s.out_nor  @= ~( s.in0 | s.in1 | s.in2 | s.in3 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0      = InPort()
    s.in1      = InPort()
    s.in2      = InPort()
    s.in3      = InPort()
    s.out_and  = OutPort()
    s.out_nand = OutPort()
    s.out_or   = OutPort()
    s.out_nor  = OutPort()

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

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out_and  == dut.out_and
    assert ref.out_nand == dut.out_nand
    assert ref.out_or   == dut.out_or
    assert ref.out_nor  == dut.out_nor

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

