#=========================================================================
# Prob07p15_comb_arith_8b_scmp_test
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
    s.lt  = OutPort()
    s.eq  = OutPort()
    s.gt  = OutPort()

    s.temp_lt = Wire(33)
    s.temp_gt = Wire(33)

    @update
    def up():

      s.temp_lt @= sext( s.in0, 33 ) - sext( s.in1, 33 )
      s.temp_gt @= sext( s.in1, 33 ) - sext( s.in0, 33 )

      s.lt @= s.temp_lt[32]
      s.eq @= s.in0 == s.in1
      s.gt @= s.temp_gt[32]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.lt  = OutPort()
    s.eq  = OutPort()
    s.gt  = OutPort()

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
                      ">", dut.lt, dut.eq, dut.gt )

    assert ref.lt == dut.lt
    assert ref.eq == dut.eq
    assert ref.gt == dut.gt

#-------------------------------------------------------------------------
# test_case_lt_pos
#-------------------------------------------------------------------------

def test_case_lt_pos( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,   1 ),
    (   1,   2 ),
    (   3,   9 ),
    (  13,  42 ),
  ])

#-------------------------------------------------------------------------
# test_case_lt_neg
#-------------------------------------------------------------------------

def test_case_lt_neg( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   -1,    0 ),
    (   -1,    1 ),
    (   -1,    2 ),
    ( -128,    0 ),
    ( -128,    1 ),
    ( -128,    2 ),

    (   -5,    0 ),
    (   -5,   -1 ),
    (   -5,   -2 ),
    ( -128, -100 ),
    ( -128, -127 ),
  ])

#-------------------------------------------------------------------------
# test_case_eq
#-------------------------------------------------------------------------

def test_case_eq( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,   0 ),
    (  16,  16 ),
    (  32,  32 ),
    ( 100, 100 ),
    ( 128, 128 ),
    ( 255, 255 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt_pos
#-------------------------------------------------------------------------

def test_case_gt_pos( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   1,   0 ),
    (   2,   1 ),
    (   9,   3 ),
    (  42,  13 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt_neg
#-------------------------------------------------------------------------

def test_case_gt_neg( pytestconfig ):
  run_sim( pytestconfig,
  [
    (    0,   -1 ),
    (    1,   -1 ),
    (    2,   -1 ),
    (    0, -128 ),
    (    1, -128 ),
    (    2, -128 ),

    (    0,   -5 ),
    (   -1,   -5 ),
    (   -2,   -5 ),
    ( -100, -128 ),
    ( -127, -128 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

