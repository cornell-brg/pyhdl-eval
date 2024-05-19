#=========================================================================
# Prob10p03_seq_gates_1b_dffr_test
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
    s.d  = InPort()
    s.q  = OutPort()

    @update_ff
    def up():
      if s.reset:
        s.q <<= 0
      else:
        s.q <<= s.d

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.d  = InPort()
    s.q  = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    reset,d = test_vector

    ref.reset @= reset
    ref.d     @= d

    dut.reset @= reset
    dut.d     @= d

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.reset, dut.d, ">", dut.q )

    assert ref.q == dut.q

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    # rs d
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig,
  [
    # rs d
    ( 0, 0 ),
    ( 0, 1 ),
    ( 0, 1 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 1, 0 ),
    ( 1, 0 ),
    ( 1, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1) ) ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

