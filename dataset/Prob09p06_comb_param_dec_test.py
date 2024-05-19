#=========================================================================
# Prob09p06_comb_param_dec_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s, nbits ):
    s.in_ = InPort (clog2(nbits))
    s.out = OutPort(nbits)

    @update
    def up():

      s.out @= 0
      if ( s.in_ <= nbits-1 ):
        s.out[s.in_] @= 1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in_ = InPort (clog2(nbits))
    s.out = OutPort(nbits)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors, nbits ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nbits=nbits )

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
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b000,
    0b001,
    0b010,
    0b011,
    0b100,
    0b101,
    0b110,
    0b111,
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits10_valid
#-------------------------------------------------------------------------

def test_case_nbits10_valid( pytestconfig ):
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
  ],
  nbits=10 )

#-------------------------------------------------------------------------
# test_case_nbits10_invalid
#-------------------------------------------------------------------------

def test_case_nbits10_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ],
  nbits=10 )

