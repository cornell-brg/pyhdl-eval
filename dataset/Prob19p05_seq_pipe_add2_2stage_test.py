#=========================================================================
# Prob19p05_seq_pipe_add2_2stage_test
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
    s.in0     = InPort (8)
    s.in1     = InPort (8)
    s.out_lsn = OutPort(4)
    s.out     = OutPort(8)

    #---------------------------------------------------------------------
    # stage 0
    #---------------------------------------------------------------------

    s.in0_X0 = Wire(8)
    s.in1_X0 = Wire(8)

    @update_ff
    def pipe_X0():
      s.in0_X0 <<= s.in0
      s.in1_X0 <<= s.in1

    s.out_tmp_X0      = Wire(5)
    s.out_lsn_X0      = Wire(4)
    s.out_lsn_cout_X0 = Wire()

    @update
    def comb_X0():
      s.out_tmp_X0      @= zext( s.in0_X0[0:4], 5 ) + zext( s.in1_X0[0:4], 5 )
      s.out_lsn_X0      @= s.out_tmp_X0[0:4]
      s.out_lsn_cout_X0 @= s.out_tmp_X0[4]

    connect( s.out_lsn, s.out_lsn_X0 )

    #---------------------------------------------------------------------
    # stage 1
    #---------------------------------------------------------------------

    s.in0_msn_X1      = Wire(4)
    s.in1_msn_X1      = Wire(4)
    s.out_lsn_X1      = Wire(4)
    s.out_lsn_cout_X1 = Wire()

    @update_ff
    def pipe_X1():
      s.in0_msn_X1      <<= s.in0_X0[4:8]
      s.in1_msn_X1      <<= s.in1_X0[4:8]
      s.out_lsn_X1      <<= s.out_lsn_X0
      s.out_lsn_cout_X1 <<= s.out_lsn_cout_X0

    s.out_msn_X1 = Wire(4)

    @update
    def comb_X1():
      s.out_msn_X1 @= s.in0_msn_X1 + s.in1_msn_X1 + zext( s.out_lsn_cout_X1, 4) 
      s.out        @= concat( s.out_msn_X1, s.out_lsn_X1 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0     = InPort (8)
    s.in1     = InPort (8)
    s.out_lsn = OutPort(4)
    s.out     = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ (0,0) ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    in0,in1 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1

    dut.in0 @= in0
    dut.in1 @= in1

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, f"({dut.in0.int():4})",
                           dut.in1, f"({dut.in1.int():4})",
                      ">", dut.out_lsn, f"({dut.out_lsn.int():4})",
                           dut.out, f"({dut.out.int():4})" )

    if i > 0:
      assert ref.out_lsn == dut.out_lsn
      assert ref.out     == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig,
  [
    (   0,  0 ),
    (   0,  1 ),
    (   1,  0 ),
    (  42, 13 ),
    (  13, 42 ),
    ( 100, 27 ),
    (   0,  0 ),
    (   0,  0 ),
    (   0,  0 ),
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
    ( -128, 127 ),
    (    0,   0 ),
    (    0,   0 ),
    (    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    (  127,   1 ),
    (  126,   2 ),
    (  120,  13 ),
    ( -128,  -1 ),
    ( -127,  -2 ),
    ( -120, -13 ),
    (    0,   0 ),
    (    0,   0 ),
    (    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_mid_carry
#-------------------------------------------------------------------------

def test_case_mid_carry( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x00, 0x00 ),
    ( 0x08, 0x08 ),
    ( 0x0c, 0x0c ),
    ( 0x0d, 0x0d ),
    ( 0x18, 0x18 ),
    ( 0x1c, 0x1c ),
    ( 0x1d, 0x1d ),
    ( 0x38, 0x38 ),
    ( 0x3c, 0x3c ),
    ( 0x3d, 0x3d ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x00, 0x00 ),
    ( 0x01, 0x01 ),
    ( 0x02, 0x03 ),
    ( 0x03, 0x04 ),
    ( 0x11, 0x11 ),
    ( 0x12, 0x13 ),
    ( 0x13, 0x14 ),
    ( 0x09, 0x09 ),
    ( 0x19, 0x19 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

