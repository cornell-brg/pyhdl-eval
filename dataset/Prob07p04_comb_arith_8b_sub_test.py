#=========================================================================
# Prob07p04_comb_arith_8b_sub_test
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
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.out = OutPort(8)

    @update
    def up():
      s.out @= s.in0 - s.in1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.out = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1

    dut.in0 @= in0
    dut.in1 @= in1

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in0, f"({dut.in0.int():4})",
                           dut.in1, f"({dut.in1.int():4})",
                      ">", dut.out, f"({dut.out.int():4})" )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,   0 ),
    (   0,   1 ),
    (   1,   0 ),
    (  42,  13 ),
    (  13,  42 ),
    ( 127,   0 ),
    (   0, 128 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig,
  [
    (    0,  -1 ),
    (   -1,   0 ),
    (   42, -13 ),
    (  -42,  13 ),
    (  -42, -13 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( -128,   1 ),
    ( -127,   2 ),
    ( -120,  13 ),
    (  127,  -1 ),
    (  126,  -2 ),
    (  120, -13 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

