#=========================================================================
# Prob02p05_comb_wires_64b_byte_rev_test
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
    s.in_ = InPort (64)
    s.out = OutPort(64)

    @update
    def up():
      s.out[ 0: 8] @= s.in_[56:64];
      s.out[ 8:16] @= s.in_[48:56];
      s.out[16:24] @= s.in_[40:48];
      s.out[24:32] @= s.in_[32:40];
      s.out[32:40] @= s.in_[24:32];
      s.out[40:48] @= s.in_[16:24];
      s.out[48:56] @= s.in_[ 8:16];
      s.out[56:64] @= s.in_[ 0: 8];

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (64)
    s.out = OutPort(64)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_ = test_vector

    ref.in_ @= in_
    dut.in_ @= in_

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in_, ">", dut.out )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x0000_0000_0000_0000,
    0x1234_1234_1234_1234,
    0x89ab_cdef_89ab_cdef,
    0x4567_89ab_cdef_4567,
    0x0123_4567_89ab_cdef,
    0xdead_beef_dead_beef,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists(pst.bits(64)) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

