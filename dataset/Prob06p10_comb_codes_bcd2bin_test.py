#=========================================================================
# Prob06p10_comb_codes_bcd2bin_test
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
    s.in_ = InPort (8)
    s.out = OutPort(4)

    @update
    def up():

      ones = s.in_[0:4];
      tens = s.in_[4:8];

      if tens == 0 and ones < 10:
        s.out @= ones
      elif tens == 1 and ones < 10:
        s.out @= 10 + ones
      else:
        s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
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
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000,
    0b0000_0001,
    0b0000_0010,
    0b0000_0011,

    0b0000_0100,
    0b0000_0101,
    0b0000_0110,
    0b0000_0111,

    0b0000_1000,
    0b0000_1001,
    0b0001_0000,
    0b0001_0001,

    0b0001_0010,
    0b0001_0011,
    0b0001_0100,
    0b0001_0101,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_1010,
    0b0000_1011,
    0b0000_1100,
    0b0000_1101,
    0b0000_1110,
    0b0000_1111,

    0b0010_0000,
    0b0010_0001,
    0b0010_0010,
    0b0010_0011,
    0b0010_0100,
    0b0010_0101,
    0b0010_0110,
    0b0010_0111,
    0b0010_1000,
    0b0010_1001,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )
