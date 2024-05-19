#=========================================================================
# Prob07p15_comb_arith_8b_alu_test
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
    s.op  = InPort (3)
    s.out = OutPort(8)

    @update
    def up():
      if   s.op == 0 : s.out @= s.in0 +  s.in1
      elif s.op == 1 : s.out @= s.in0 -  s.in1
      elif s.op == 2 : s.out @= s.in0 << zext( s.in1[0:3], 8 )
      elif s.op == 3 : s.out @= s.in0 >> zext( s.in1[0:3], 8 )
      elif s.op == 4 : s.out @= zext( s.in0 <  s.in1, 8 )
      elif s.op == 5 : s.out @= zext( s.in0 == s.in1, 8 )
      elif s.op == 6 : s.out @= zext( s.in0 >  s.in1, 8 )
      else           : s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.op  = InPort (3)
    s.out = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,op = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.op  @= op

    dut.in0 @= in0
    dut.in1 @= in1
    dut.op  @= op

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, f"({dut.in0.uint():4})",
                           dut.in1, f"({dut.in1.uint():4})",
                           dut.op,
                      ">", dut.out, f"({dut.out.uint():4})" )

    assert ref.out == dut.out
    assert op <= 6 or dut.out == 0

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_add
#-------------------------------------------------------------------------

def test_case_add( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 0 ),
    (   1,  1, 0 ),
    (   2,  1, 0 ),
    (   1,  2, 0 ),
    (  13,  2, 0 ),
    (  42,  9, 0 ),
    (  42, 13, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_sub
#-------------------------------------------------------------------------

def test_case_sub( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 1 ),
    (   1,  1, 1 ),
    (   2,  1, 1 ),
    (   1,  2, 1 ),
    (  13,  2, 1 ),
    (  42,  9, 1 ),
    (  42, 13, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_srl
#-------------------------------------------------------------------------

def test_case_srl( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 2 ),
    (   1,  1, 2 ),
    (   2,  1, 2 ),
    (   1,  2, 2 ),
    (  13,  2, 2 ),
    (  42,  9, 2 ),
    (  42, 13, 2 ),
  ])

#-------------------------------------------------------------------------
# test_case_sll
#-------------------------------------------------------------------------

def test_case_sll( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 3 ),
    (   1,  1, 3 ),
    (   2,  1, 3 ),
    (   1,  2, 3 ),
    (  13,  2, 3 ),
    (  42,  9, 3 ),
    (  42, 13, 3 ),
])

#-------------------------------------------------------------------------
# test_case_lt
#-------------------------------------------------------------------------

def test_case_lt( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 4 ),
    (   1,  1, 4 ),
    (   2,  1, 4 ),
    (   1,  2, 4 ),
    (  13,  2, 4 ),
    (  42,  9, 4 ),
    (  42, 13, 4 ),
  ])

#-------------------------------------------------------------------------
# test_case_eq
#-------------------------------------------------------------------------

def test_case_eq( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 5 ),
    (   1,  1, 5 ),
    (   2,  1, 5 ),
    (   1,  2, 5 ),
    (  13,  2, 5 ),
    (  42,  9, 5 ),
    (  42, 13, 5 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt
#-------------------------------------------------------------------------

def test_case_gt( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0, 6 ),
    (   1,  1, 6 ),
    (   2,  1, 6 ),
    (   1,  2, 6 ),
    (  13,  2, 6 ),
    (  42,  9, 6 ),
    (  42, 13, 6 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(3) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

