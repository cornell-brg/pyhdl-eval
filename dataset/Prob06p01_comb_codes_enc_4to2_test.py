#=========================================================================
# Prob06p01_comb_codes_enc_4to2_test
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
    s.out = OutPort(2)

    @update
    def up():
      if   s.in_ == 0b0001: s.out @= 0
      elif s.in_ == 0b0010: s.out @= 1
      elif s.in_ == 0b0100: s.out @= 2
      elif s.in_ == 0b1000: s.out @= 3
      else:                 s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (4)
    s.out = OutPort(2)

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
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0001,
    0b0010,
    0b0100,
    0b1000,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000,
    # 0b0001, valid
    # 0b0010, valid
    0b0011,
    # 0b0100, valid
    0b0101,
    0b0110,
    0b0111,

    # 0b1000, valid
    0b1001,
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

