#=========================================================================
# Prob05p09_comb_mux_1b_1to128_test
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
    s.in_ = InPort()
    s.sel = InPort(7)
    s.out = OutPort(128)

    @update
    def up():
      s.out @= Bits128(0)
      s.out[s.sel] @= s.in_

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort()
    s.sel = InPort(7)
    s.out = OutPort(128)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_,sel = test_vector

    ref.in_ @= in_
    ref.sel @= sel

    dut.in_ @= in_
    dut.sel @= sel

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in_, dut.sel, ">", dut.out )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0,   0 ),
    ( 1,   0 ),
    ( 0,   1 ),
    ( 1,   1 ),
    ( 0,   2 ),
    ( 1,   2 ),
    ( 0,   3 ),
    ( 1,   3 ),

    ( 0,  15 ),
    ( 1,  15 ),
    ( 0, 100 ),
    ( 1, 100 ),
    ( 0, 127 ),
    ( 1, 127 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(7) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

