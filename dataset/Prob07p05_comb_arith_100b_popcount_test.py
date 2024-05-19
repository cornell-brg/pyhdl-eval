#=========================================================================
# Prob07p05_comb_arith_100b_popcount_test
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
    s.out = OutPort(  7)

    @update
    def up():
      s.out @= 0
      for i in range(100):
        s.out @= s.out + zext( s.in_[i], 7 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (100)
    s.out = OutPort(  7)

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
    assert dut.out <= 100

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000,

    0b0000_0001,
    0b0000_0010,
    0b0000_0100,
    0b0000_1000,
    0b0001_0000,
    0b0010_0000,
    0b0100_0000,
    0b1000_0000,

    0b0000_0011,
    0b0000_1110,
    0b0011_1100,
    0b1111_1000,
    0b1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x0_0000_0000_0000_0000_0000_0001,
    0x0_0000_0000_0000_0000_0000_0011,
    0x0_0000_0000_0000_0000_0000_0111,
    0x0_0000_0000_0000_0000_0000_1111,

    0x0_0000_0000_0000_0000_0001_1111,
    0x0_0000_0000_0000_0000_0011_1111,
    0x0_0000_0000_0000_0000_0111_1111,
    0x0_0000_0000_0000_0000_1111_1111,

    0x0_0000_0000_0000_0001_1111_1111,
    0x0_0000_0000_0000_0011_1111_1111,
    0x0_0000_0000_0000_0111_1111_1111,
    0x0_0000_0000_0000_1111_1111_1111,

    0x0_0000_0000_0001_1111_1111_1111,
    0x0_0000_0000_0011_1111_1111_1111,
    0x0_0000_0000_0111_1111_1111_1111,
    0x0_0000_0000_1111_1111_1111_1111,

    0x0_0000_0001_1111_1111_1111_1111,
    0x0_0000_0011_1111_1111_1111_1111,
    0x0_0000_0111_1111_1111_1111_1111,
    0x0_0000_1111_1111_1111_1111_1111,

    0x0_0001_1111_1111_1111_1111_1111,
    0x0_0011_1111_1111_1111_1111_1111,
    0x0_0111_1111_1111_1111_1111_1111,
    0x0_1111_1111_1111_1111_1111_1111,

    0x1_1111_1111_1111_1111_1111_1111,
    0x3_3333_3333_3333_3333_3333_3333,
    0x7_7777_7777_7777_7777_7777_7777,
    0xf_ffff_ffff_ffff_ffff_ffff_ffff,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(100) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

