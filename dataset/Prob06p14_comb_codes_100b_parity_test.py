#=========================================================================
# Prob06p14_comb_codes_100b_parity_test
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
    s.out = OutPort()

    @update
    def up():
      s.out @= reduce_xor( s.in_ )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (100)
    s.out = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_ = test_vector

    ref.in_ @= in_
    dut.in_ @= in_

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in_, ">", dut.out )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000,
    0b0001,
    0b0010,
    0b0011,

    0b0100,
    0b0101,
    0b0110,
    0b0111,

    0b1000,
    0b1001,
    0b1010,
    0b1011,

    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x0_0000_0000_0000_0000_0000_0000,
    0xa_aaaa_aaaa_aaaa_aaaa_aaaa_aaaa,
    0x5_5555_5555_5555_5555_5555_5555,
    0xf_ffff_ffff_ffff_ffff_ffff_ffff,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(100) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

