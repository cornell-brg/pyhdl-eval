#=========================================================================
# Prob10p05_seq_gates_8b_dffre_test
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
    s.en = InPort ()
    s.d  = InPort (8)
    s.q  = OutPort(8)

    @update_ff
    def up():
      if s.reset:
        s.q <<= 0xff
      elif s.en:
        s.q <<= s.d

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.en = InPort ()
    s.d  = InPort (8)
    s.q  = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    reset,en,d = test_vector

    ref.reset @= reset
    ref.en    @= en
    ref.d     @= d

    dut.reset @= reset
    dut.en    @= en
    dut.d     @= d

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, ref.reset, ref.en, dut.d, ">", dut.q )

    assert ref.q == dut.q

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    # rs en d
    ( 0, 0, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x01 ),
    ( 0, 1, 0x01 ),
    ( 0, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x01 ),
    ( 0, 0, 0x01 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),

    ( 0, 1, 0x00 ),
    ( 0, 1, 0xab ),
    ( 0, 1, 0xcd ),
    ( 0, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0xab ),
    ( 0, 0, 0xcd ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig,
  [
    # rs en d
    ( 0, 0, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),

    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1), pst.bits(8) )))
def test_case_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(8) )))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

