#=========================================================================
# Prob07p10_comb_arith_8b_smul_test
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
    s.out = OutPort(16)

    s.in0_abs      = Wire(8)
    s.in1_abs      = Wire(8)
    s.out_unsigned = Wire(16)

    @update
    def up():

      # absolute values of inputs

      if s.in0[7]:
        s.in0_abs @= ~s.in0 + 1
      else:
        s.in0_abs @= s.in0

      if s.in1[7]:
        s.in1_abs @= ~s.in1 + 1
      else:
        s.in1_abs @= s.in1

      # unsigned multiplication

      s.out_unsigned @= zext( s.in0_abs, 16 ) * zext( s.in1_abs, 16 )

      # adjust sign of the output

      if s.in0[7] != s.in1[7]:
        s.out @= ~s.out_unsigned + 1;
      else:
        s.out @= s.out_unsigned

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.out = OutPort(16)

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

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, f"({dut.in0.int():4})",
                           dut.in1, f"({dut.in1.int():4})",
                      ">", dut.out, f"({dut.out.int():7})" )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_pos_small
#-------------------------------------------------------------------------

def test_case_pos_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0 ),
    (   0,  1 ),
    (   1,  0 ),
    (   2,  2 ),
    (   2,  3 ),
    (   8,  9 ),
    (  12, 13 ),
  ])

#-------------------------------------------------------------------------
# test_case_pos_large
#-------------------------------------------------------------------------

def test_case_pos_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  16,  16 ),
    (  20,  16 ),
    (  42,  90 ),
    ( 100,  99 ),
    ( 127, 127 ),
  ])

#-------------------------------------------------------------------------
# test_case_neg_small
#-------------------------------------------------------------------------

def test_case_neg_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  -1 ),
    (  -1,   0 ),
    (  -2,   2 ),
    (   2,  -2 ),
    (  -2,  -2 ),
    (  -8,   9 ),
    (   8,  -9 ),
    ( -12, -13 ),
  ])

#-------------------------------------------------------------------------
# test_case_neg_large
#-------------------------------------------------------------------------

def test_case_neg_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  -16,  -16 ),
    (   20,  -16 ),
    (  -20,   16 ),
    (  -20,  -16 ),
    (  -42,   90 ),
    (  100,  -99 ),
    ( -128, -128 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

