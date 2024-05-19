#=========================================================================
# Prob19p06_seq_pipe_add3_2stage_test
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
    s.in0   = InPort (8)
    s.in1   = InPort (8)
    s.in2   = InPort (8)
    s.out01 = OutPort(8)
    s.out   = OutPort(8)

    #---------------------------------------------------------------------
    # stage 0
    #---------------------------------------------------------------------

    s.in0_X0 = Wire(8)
    s.in1_X0 = Wire(8)
    s.in2_X0 = Wire(8)

    @update_ff
    def pipe_X0():
      s.in0_X0 <<= s.in0
      s.in1_X0 <<= s.in1
      s.in2_X0 <<= s.in2

    s.sum01_X0 = Wire(8)

    @update
    def comb_X0():
      s.sum01_X0 @= s.in0_X0 + s.in1_X0
      s.out01    @= s.sum01_X0

    #---------------------------------------------------------------------
    # stage 1
    #---------------------------------------------------------------------

    s.sum01_X1 = Wire(8)
    s.in2_X1   = Wire(8)

    @update_ff
    def pipe_X1():
      s.sum01_X1 <<= s.sum01_X0
      s.in2_X1   <<= s.in2_X0

    @update
    def comb_X1():
      s.out @= s.sum01_X1 + s.in2_X1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0   = InPort (8)
    s.in1   = InPort (8)
    s.in2   = InPort (8)
    s.out01 = OutPort(8)
    s.out   = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ (0,0,0), (0,0,0) ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    in0,in1,in2 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0,   f"({dut.in0.int():4})",
                           dut.in1,   f"({dut.in1.int():4})",
                           dut.in2,   f"({dut.in2.int():4})",
                      ">", dut.out01, f"({dut.out01.int():4})",
                           dut.out,   f"({dut.out.int():4})" )

    if i > 1:
      assert ref.out01 == dut.out01
      assert ref.out   == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_input2
#-------------------------------------------------------------------------

def test_case_input2( pytestconfig ):
  run_sim( pytestconfig,
  [
    (    0,    0,   0 ),

    (    0,    1,   0 ),
    (    1,    0,   0 ),
    (   42,   13,   0 ),
    (   13,   42,   0 ),
    (  100,   27,   0 ),

    (    0,   -1,   0 ),
    (   -1,    0,   0 ),
    (   -1,    0,   0 ),
    (   42,  -13,   0 ),
    (  -42,   13,   0 ),
    (  -42,  -13,   0 ),
    ( -128,  127,   0 ),

    (    0,    0,   1 ),
    (    0,    1,   0 ),
    (    0,   42,  13 ),
    (    0,   13,  42 ),
    (    0,  100,  27 ),

    (    0,    0,  -1 ),
    (    0,   -1,   0 ),
    (    0,   -1,   0 ),
    (    0,   42, -13 ),
    (    0,  -42,  13 ),
    (    0,  -42, -13 ),
    (    0, -128, 127 ),

    (    0,    0,   1 ),
    (    1,    0,   0 ),
    (   42,    0,  13 ),
    (   13,    0,  42 ),
    (  100,    0,  27 ),

    (    0,    0,  -1 ),
    (   -1,    0,   0 ),
    (   -1,    0,   0 ),
    (   42,    0, -13 ),
    (  -42,    0,  13 ),
    (  -42,    0, -13 ),
    ( -128,    0, 127 ),

    (    0,    0,   0 ),
    (    0,    0,   0 ),
    (    0,    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_input3
#-------------------------------------------------------------------------

def test_case_input3( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0 ),
    ( 1, 1, 1 ),
    ( 1, 2, 3 ),
    ( 3, 1, 2 ),
    ( 2, 3, 1 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  127,    1,    0 ),
    (    0,  127,    1 ),
    (    1,    0,  127 ),
    ( -128,   -1,    0 ),
    (    0, -128,   -1 ),
    (   -1,    0, -128 ),
    (   64,   64,   64 ),
    (  -64,  -64,  -64 ),
    (  128,  128,  128 ),
    (    0,    0,    0 ),
    (    0,    0,    0 ),
    (    0,    0,    0 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x01, 0x02, 0x04 ),
    ( 0x02, 0x03, 0x04 ),
    ( 0x03, 0x04, 0x05 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

