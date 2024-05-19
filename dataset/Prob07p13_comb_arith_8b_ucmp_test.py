#=========================================================================
# Prob07p13_comb_arith_8b_ucmp_test
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

    @update
    def up():
      s.lt @= s.in0 <  s.in1
      s.eq @= s.in0 == s.in1
      s.gt @= s.in0 >  s.in1

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

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, f"({dut.in0.uint():4})",
                           dut.in1, f"({dut.in1.uint():4})",
                      ">", dut.lt, dut.eq, dut.gt )

    assert ref.lt == dut.lt
    assert ref.eq == dut.eq
    assert ref.gt == dut.gt

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_lt
#-------------------------------------------------------------------------

def test_case_lt( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,   1 ),
    (   1,   2 ),
    (   3,   9 ),
    (  13,  42 ),

    ( 127, 128 ),
    ( 150, 200 ),
    ( 250, 255 ),
    ( 254, 255 ),
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
# test_case_gt
#-------------------------------------------------------------------------

def test_case_gt( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   1,   0 ),
    (   2,   1 ),
    (   9,   3 ),
    (  42,  13 ),

    ( 128, 127 ),
    ( 200, 150 ),
    ( 255, 250 ),
    ( 255, 254 ),
  ])


#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

