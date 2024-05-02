#=========================================================================
# Prob06p12_comb_codes_ascii2bin_test
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
    s.out = OutPort( 4)

    @update
    def up():

      ASCII_ZERO = 0x30;

      ones = s.in_[0: 8] - ASCII_ZERO;
      tens = s.in_[8:16] - ASCII_ZERO;

      if tens == 0 and ones < 10:
        s.out @= trunc( ones, 4 )
      elif tens == 1 and ones < 10:
        s.out @= 10 + trunc( ones, 4 )
      else:
        s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (16)
    s.out = OutPort( 4)

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
    0x3030,
    0x3031,
    0x3032,
    0x3033,

    0x3034,
    0x3035,
    0x3036,
    0x3037,

    0x3038,
    0x3039,
    0x3130,
    0x3131,

    0x3132,
    0x3133,
    0x3134,
    0x3135,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x0000,
    0x1010,
    0x2020,
    0x4040,
    0x5050,
    0x6060,
    0x7070,
    0x8080,
    0x9090,
    0xa0a0,
    0xb0b0,
    0xc0c0,
    0xd0d0,
    0xe0e0,
    0xf0f0,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(16) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

