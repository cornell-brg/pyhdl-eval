#=========================================================================
# Prob07p03_comb_arith_8b_add_carry_test
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
    s.in0  = InPort (8)
    s.in1  = InPort (8)
    s.cin  = InPort ()
    s.out  = OutPort(8)
    s.cout = OutPort()

    s.temp = Wire(9)

    @update
    def up():
      s.temp @= zext( s.in0, 9 ) + zext( s.in1, 9 ) + zext( s.cin, 9 )
      s.out  @= s.temp[0:8]
      s.cout @= s.temp[8]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0  = InPort (8)
    s.in1  = InPort (8)
    s.cin  = InPort ()
    s.out  = OutPort(8)
    s.cout = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,cin = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.cin @= cin

    dut.in0 @= in0
    dut.in1 @= in1
    dut.cin @= cin

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in0, f"({dut.in0.int():4})",
                           dut.in1, f"({dut.in1.int():4})", dut.cin,
                      ">", dut.out, f"({dut.out.int():4})", dut.cout )

    assert ref.out  == dut.out
    assert ref.cout == dut.cout

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 0 ),
    (   0,  1, 0 ),
    (   1,  0, 0 ),
    (  42, 13, 0 ),
    (  13, 42, 0 ),
    ( 100, 27, 0 ),

    (   0,  0, 1 ),
    (   0,  1, 1 ),
    (   1,  0, 1 ),
    (  42, 13, 1 ),
    (  13, 42, 1 ),
    ( 100, 26, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig,
  [
    (    0,  -1, 0 ),
    (   -1,   0, 0 ),
    (   42, -13, 0 ),
    (  -42,  13, 0 ),
    (  -42, -13, 0 ),
    ( -128, 127, 0 ),

    (    0,  -1, 1 ),
    (   -1,   0, 1 ),
    (   42, -13, 1 ),
    (  -42,  13, 1 ),
    (  -42, -13, 1 ),
    ( -128, 127, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  127,   1, 0 ),
    (  126,   2, 0 ),
    (  120,  13, 0 ),
    ( -128,  -1, 0 ),
    ( -127,  -2, 0 ),
    ( -120, -13, 0 ),

    (  127,   0, 1 ),
    (  126,   1, 1 ),
    (  120,  12, 1 ),
    ( -128,  -2, 1 ),
    ( -127,  -3, 1 ),
    ( -120, -14, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(1) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

