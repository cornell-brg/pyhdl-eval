#=========================================================================
# Prob02p08_comb_wires_5x3b_to_4x4b_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.datatypes import strategies as pst

from test_utils import construct, print_line_trace

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in0  = InPort (3)
    s.in1  = InPort (3)
    s.in2  = InPort (3)
    s.in3  = InPort (3)
    s.in4  = InPort (3)
    s.out0 = OutPort(4)
    s.out1 = OutPort(4)
    s.out2 = OutPort(4)
    s.out3 = OutPort(4)

    @update
    def up():
      temp = concat( b1(1), s.in4, s.in3, s.in2, s.in1, s.in0 )
      s.out0 @= temp[ 0: 4]
      s.out1 @= temp[ 4: 8]
      s.out2 @= temp[ 8:12]
      s.out3 @= temp[12:16]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0  = InPort (3)
    s.in1  = InPort (3)
    s.in2  = InPort (3)
    s.in3  = InPort (3)
    s.in4  = InPort (3)
    s.out0 = OutPort(4)
    s.out1 = OutPort(4)
    s.out2 = OutPort(4)
    s.out3 = OutPort(4)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0, in1, in2, in3, in4 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3
    ref.in4 @= in4

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3
    dut.in4 @= in4

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, dut.in1, dut.in2, dut.in3, ">",
                      dut.out0, dut.out1, dut.out2, dut.out3 )

    assert ref.out0 == dut.out0
    assert ref.out1 == dut.out1
    assert ref.out2 == dut.out2
    assert ref.out3 == dut.out3

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0, 0, 0 ),
    ( 1, 1, 1, 1, 1 ),
    ( 0, 0, 0, 0, 1 ),
    ( 0, 0, 0, 1, 0 ),
    ( 0, 0, 1, 0, 0 ),
    ( 0, 1, 0, 0, 0 ),
    ( 1, 0, 0, 0, 0 ),
    ( 1, 2, 3, 4, 5 ),
    ( 3, 4, 5, 6, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(3), pst.bits(3), pst.bits(3), pst.bits(3), pst.bits(3)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

