#=========================================================================
# Prob07p10_comb_arith_8b_umul_test
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
    s.in2 = InPort (16)
    s.out = OutPort(16)

    @update
    def up():
      s.out @= ( zext( s.in0, 16 ) * zext( s.in1, 16 ) ) + s.in2

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.in2 = InPort (16)
    s.out = OutPort(16)

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

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, f"({dut.in0.uint():4})",
                           dut.in1, f"({dut.in1.uint():4})",
                           dut.in2, f"({dut.in2.uint():5})",
                      ">", dut.out, f"({dut.out.uint():7})" )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0,  0 ),
    (   0,  1,  0 ),
    (   1,  0,  0 ),
    (   2,  2,  0 ),
    (   2,  3,  0 ),
    (   8,  9,  0 ),
    (  12, 13,  0 ),

    (   0,  0,  1 ),
    (   0,  1,  1 ),
    (   1,  0,  1 ),
    (   2,  2,  1 ),
    (   2,  3,  1 ),
    (   8,  9,  1 ),
    (  12, 13,  1 ),

    (   0,  0,  2 ),
    (   0,  1,  2 ),
    (   1,  0,  2 ),
    (   2,  2,  2 ),
    (   2,  3,  2 ),
    (   8,  9,  2 ),
    (  12, 13,  2 ),
])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  16,  16,     0 ),
    (  20,  16,     0 ),
    (  42,  90,     0 ),
    ( 130, 100,     0 ),
    ( 255, 255,     0 ),
    ( 255, 255,    10 ),

    (  16,  16,   255 ),
    (  20,  16,   255 ),
    (  42,  90,   255 ),
    ( 130, 100,   255 ),
    ( 250, 250,   255 ),

    (  16,  16, 10000 ),
    (  20,  16, 10000 ),
    (  42,  90, 10000 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 255, 255, 1     ),
    ( 255, 255, 255   ),
    ( 255, 255, 10000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(16) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

