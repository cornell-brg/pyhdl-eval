#=========================================================================
# Prob07p17_comb_arith_2x8b_minmax_test
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
    s.min = OutPort(8)
    s.max = OutPort(8)

    @update
    def up():
      if s.in0 < s.in1:
        s.min @= s.in0
        s.max @= s.in1
      else:
        s.max @= s.in0
        s.min @= s.in1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.min = OutPort(8)
    s.max = OutPort(8)

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
                      ">", dut.min, f"({dut.min.uint():4})",
                           dut.max, f"({dut.max.uint():4})" )

    assert ref.min == dut.min
    assert ref.max == dut.max
    assert dut.min <= dut.max

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,   0 ),
    (   0,   1 ),
    (   1,   0 ),
    (   1,   1 ),
    (  13,  42 ),
    (  42,  13 ),
    ( 255,  13 ),
    (  13, 255 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

