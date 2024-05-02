#=========================================================================
# Prob06p11_comb_codes_bin2ascii_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in_ = InPort ( 4)
    s.out = OutPort(16)

    @update
    def up():

      # An ASCII value of 0x30 is the digit 0
      ASCII_ZERO = 0x30

      # Zero extended version of input so we can add to 8b ASCII_ZERO
      in_zext = zext( s.in_, 8 )

      if s.in_ < 10:
        ones = ASCII_ZERO + in_zext
        tens = ASCII_ZERO
      else:
        ones = ASCII_ZERO + in_zext - 10
        tens = ASCII_ZERO + 1

      # set the appropriate fields in output

      s.out[0: 8] @= ones
      s.out[8:16] @= tens

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort ( 4)
    s.out = OutPort(16)

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

