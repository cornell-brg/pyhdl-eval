#=========================================================================
# Prob10p09_seq_gates_nl2
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
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.in3 = InPort()
    s.out = OutPort()

    s.in0_dff = Wire()
    s.in1_dff = Wire()
    s.in2_dff = Wire()
    s.in3_dff = Wire()

    @update_ff
    def dff():
      s.in0_dff <<= s.in0
      s.in1_dff <<= s.in1
      s.in2_dff <<= s.in2
      s.in3_dff <<= s.in3

    @update
    def comb():
      s.out @= (~s.in0_dff | s.in1_dff) & (s.in2_dff | ~s.in3_dff)

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort()
    s.in1 = InPort()
    s.in2 = InPort()
    s.in3 = InPort()
    s.out = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ (0,0,0,0) ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    in0,in1,in2,in3 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, dut.in1, dut.in2, dut.in3, ">", dut.out )

    if i > 0:
      assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 1, 0, 0 ),
    ( 0, 1, 0, 1 ),
    ( 0, 1, 1, 0 ),
    ( 0, 1, 1, 1 ),

    ( 1, 0, 0, 0 ),
    ( 1, 0, 0, 1 ),
    ( 1, 0, 1, 0 ),
    ( 1, 0, 1, 1 ),
    ( 1, 1, 0, 0 ),
    ( 1, 1, 0, 1 ),
    ( 1, 1, 1, 0 ),
    ( 1, 1, 1, 1 ),

    ( 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(1), pst.bits(1), pst.bits(1), pst.bits(1)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

