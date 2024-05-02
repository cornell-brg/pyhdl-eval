#=========================================================================
# Prob06p06_comb_codes_penc_16to4_test
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
    s.in_ = InPort (16)
    s.out = OutPort(4)

    @update
    def up():
      s.out @= 0
      for i in reversed(range(16)):
        if s.in_[i] == 1:
          s.out @= i

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (16)
    s.out = OutPort(4)

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
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000_0000_0000,
    0b0000_0000_0000_0001,
    0b0000_0000_0000_0010,
    0b0000_0000_0000_0011,

    0b0000_0000_0000_0100,
    0b0000_0000_0000_0101,
    0b0000_0000_0000_0110,
    0b0000_0000_0000_0111,

    0b0000_0000_0000_1000,
    0b0000_0000_0000_1001,
    0b0000_0000_0000_1010,
    0b0000_0000_0000_1011,

    0b0000_0000_0000_1100,
    0b0000_0000_0000_1101,
    0b0000_0000_0000_1110,
    0b0000_0000_0000_1111,

    0b0000_0000_0000_0000,
    0b0001_0000_0000_0000,
    0b0010_0000_0000_0000,
    0b0011_0000_0000_0000,

    0b0100_0000_0000_0000,
    0b0101_0000_0000_0000,
    0b0110_0000_0000_0000,
    0b0111_0000_0000_0000,

    0b1000_0000_0000_0000,
    0b1001_0000_0000_0000,
    0b1010_0000_0000_0000,
    0b1011_0000_0000_0000,

    0b1100_0000_0000_0000,
    0b1101_0000_0000_0000,
    0b1110_0000_0000_0000,
    0b1111_0000_0000_0000,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(16) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

