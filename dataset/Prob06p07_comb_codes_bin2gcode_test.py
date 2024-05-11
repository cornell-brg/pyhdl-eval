#=========================================================================
# Prob06p07_comb_codes_bin2gcode_test
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
    s.out = OutPort(4)

    @update
    def up():

      if   s.in_ == 0b0000 : s.out @= 0b0000
      elif s.in_ == 0b0001 : s.out @= 0b0001
      elif s.in_ == 0b0010 : s.out @= 0b0011
      elif s.in_ == 0b0011 : s.out @= 0b0010

      elif s.in_ == 0b0100 : s.out @= 0b0110
      elif s.in_ == 0b0101 : s.out @= 0b0111
      elif s.in_ == 0b0110 : s.out @= 0b0101
      elif s.in_ == 0b0111 : s.out @= 0b0100

      elif s.in_ == 0b1000 : s.out @= 0b1100
      elif s.in_ == 0b1001 : s.out @= 0b1101
      elif s.in_ == 0b1010 : s.out @= 0b1111
      elif s.in_ == 0b1011 : s.out @= 0b1110

      elif s.in_ == 0b1100 : s.out @= 0b1010
      elif s.in_ == 0b1101 : s.out @= 0b1011
      elif s.in_ == 0b1110 : s.out @= 0b1001
      elif s.in_ == 0b1111 : s.out @= 0b1000

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (4)
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

