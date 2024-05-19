#=========================================================================
# Prob19p08_seq_pipe_minmax4_2stage_test
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
    s.in2 = InPort (8)
    s.in3 = InPort (8)
    s.min = OutPort(8)
    s.max = OutPort(8)

    #---------------------------------------------------------------------
    # stage 0
    #---------------------------------------------------------------------

    s.in0_X0 = Wire(8)
    s.in1_X0 = Wire(8)
    s.in2_X0 = Wire(8)
    s.in3_X0 = Wire(8)

    @update_ff
    def pipe_X0():
      s.in0_X0 <<= s.in0
      s.in1_X0 <<= s.in1
      s.in2_X0 <<= s.in2
      s.in3_X0 <<= s.in3

    s.min01_X0 = Wire(8)
    s.max01_X0 = Wire(8)
    s.min23_X0 = Wire(8)
    s.max23_X0 = Wire(8)

    @update
    def comb_X0():
      s.min01_X0 @= s.in0_X0 if s.in0_X0 < s.in1_X0 else s.in1_X0
      s.max01_X0 @= s.in0_X0 if s.in0_X0 > s.in1_X0 else s.in1_X0
      s.min23_X0 @= s.in2_X0 if s.in2_X0 < s.in3_X0 else s.in3_X0
      s.max23_X0 @= s.in2_X0 if s.in2_X0 > s.in3_X0 else s.in3_X0

    #---------------------------------------------------------------------
    # stage 1
    #---------------------------------------------------------------------

    s.min01_X1 = Wire(8)
    s.max01_X1 = Wire(8)
    s.min23_X1 = Wire(8)
    s.max23_X1 = Wire(8)

    @update_ff
    def pipe_X1():
      s.min01_X1 <<= s.min01_X0
      s.max01_X1 <<= s.max01_X0
      s.min23_X1 <<= s.min23_X0
      s.max23_X1 <<= s.max23_X0

    @update
    def comb_X1():
      s.min @= s.min01_X1 if s.min01_X1 < s.min23_X1 else s.min23_X1
      s.max @= s.max01_X1 if s.max01_X1 > s.max23_X1 else s.max23_X1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort (8)
    s.in1 = InPort (8)
    s.in2 = InPort (8)
    s.in3 = InPort (8)
    s.min = OutPort(8)
    s.max = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ (0,0,0,0), (0,0,0,0) ] + test_vectors

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

    print_line_trace( dut, dut.in0, dut.in1, dut.in2, dut.in3,
                      ">", dut.min, dut.max )

    if i > 1:
      assert ref.min == dut.min
      assert ref.max == dut.max

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 1, 2, 3, 4 ),
    ( 4, 3, 2, 1 ),
    ( 3, 4, 1, 2 ),
    ( 1, 4, 3, 2 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_dups
#-------------------------------------------------------------------------

def test_case_dups( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0, 0 ),
    ( 9, 9, 9, 9 ),
    ( 1, 1, 2, 2 ),
    ( 2, 2, 1, 1 ),
    ( 2, 1, 2, 1 ),
    ( 1, 1, 2, 1 ),
    ( 1, 2, 2, 2 ),
    ( 2, 2, 1, 2 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 101, 102, 103, 104 ),
    ( 104, 103, 102, 101 ),
    ( 103, 104, 101, 102 ),
    ( 101, 104, 103, 102 ),
    ( 255, 254, 252, 253 ),
    ( 252, 253, 254, 255 ),
    ( 253, 252, 255, 254 ),
    ( 255, 252, 253, 254 ),
    (   0,   0,   0,   0 ),
    (   0,   0,   0,   0 ),
    (   0,   0,   0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x01, 0x02, 0x03, 0x04 ),
    ( 0x04, 0x05, 0x03, 0x02 ),
    ( 0x06, 0x03, 0x04, 0x05 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(8), pst.bits(8), pst.bits(8), pst.bits(8)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

