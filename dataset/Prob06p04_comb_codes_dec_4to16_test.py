#=========================================================================
# Prob06p04_comb_codes_dec_4to16_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in_ = InPort (4)
    s.out = OutPort(16)

    @update
    def up():

      if   s.in_ == 0:  s.out @= 0b0000_0000_0000_0001
      elif s.in_ == 1:  s.out @= 0b0000_0000_0000_0010
      elif s.in_ == 2:  s.out @= 0b0000_0000_0000_0100
      elif s.in_ == 3:  s.out @= 0b0000_0000_0000_1000

      elif s.in_ == 4:  s.out @= 0b0000_0000_0001_0000
      elif s.in_ == 5:  s.out @= 0b0000_0000_0010_0000
      elif s.in_ == 6:  s.out @= 0b0000_0000_0100_0000
      elif s.in_ == 7:  s.out @= 0b0000_0000_1000_0000

      elif s.in_ == 8:  s.out @= 0b0000_0001_0000_0000
      elif s.in_ == 9:  s.out @= 0b0000_0010_0000_0000
      elif s.in_ == 10: s.out @= 0b0000_0100_0000_0000
      elif s.in_ == 11: s.out @= 0b0000_1000_0000_0000

      elif s.in_ == 12: s.out @= 0b0001_0000_0000_0000
      elif s.in_ == 13: s.out @= 0b0010_0000_0000_0000
      elif s.in_ == 14: s.out @= 0b0100_0000_0000_0000
      elif s.in_ == 15: s.out @= 0b1000_0000_0000_0000

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (4)
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

