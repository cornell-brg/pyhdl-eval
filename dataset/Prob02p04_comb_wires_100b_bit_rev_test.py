#=========================================================================
# Prob02p04_comb_wires_100b_bit_rev_test
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
    s.in_ = InPort (100)
    s.out = OutPort(100)

    @update
    def up():
      for i in range(0,100):
        s.out[i] @= s.in_[99-i]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (100)
    s.out = OutPort(100)

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
    0x0_0000_0000_0000_0000_0000_0000,
    0x0_1234_1234_1234_1234_1234_1234,
    0x1_89ab_cdef_89ab_cdef_89ab_cdef,
    0x2_4567_89ab_cdef_4567_89ab_cdef,
    0x4_0123_4567_89ab_cdef_0123_4567,
    0x8_dead_beef_dead_beef_dead_beef,
    0xf_ffff_ffff_ffff_ffff_ffff_ffff,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists(pst.bits(100)) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

