#=========================================================================
# Prob09p09_comb_param_penc_test
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
  def construct( s, nbits ):
    s.in_ = InPort (nbits)
    s.out = OutPort(clog2(nbits))

    @update
    def up():
      s.out @= 0
      for i in reversed(range(nbits)):
        if s.in_[i] == 1:
          s.out @= i

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in_ = InPort (nbits)
    s.out = OutPort(clog2(nbits))

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
    0b0000_1010,
    0b0000_1011,

    0b0000_1100,
    0b0000_1101,
    0b0000_1110,
    0b0000_1111,

    0b0000_0000,
    0b0001_0000,
    0b0010_0000,
    0b0011_0000,

    0b0100_0000,
    0b0101_0000,
    0b0110_0000,
    0b0111_0000,

    0b1000_0000,
    0b1001_0000,
    0b1010_0000,
    0b1011_0000,

    0b1100_0000,
    0b1101_0000,
    0b1110_0000,
    0b1111_0000,
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits10_directed
#-------------------------------------------------------------------------

def test_case_nbits10_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b00_0000_0000,
    0b00_0000_0001,
    0b00_0000_0010,
    0b00_0000_0011,

    0b00_0000_0100,
    0b00_0000_0101,
    0b00_0000_0110,
    0b00_0000_0111,

    0b00_0000_1000,
    0b00_0000_1001,
    0b00_0000_1010,
    0b00_0000_1011,

    0b00_0000_1100,
    0b00_0000_1101,
    0b00_0000_1110,
    0b00_0000_1111,

    0b00_0000_0000,
    0b00_0001_0000,
    0b00_0010_0000,
    0b00_0011_0000,

    0b00_0100_0000,
    0b00_0101_0000,
    0b00_0110_0000,
    0b00_0111_0000,

    0b00_1000_0000,
    0b00_1001_0000,
    0b00_1010_0000,
    0b00_1011_0000,

    0b00_1100_0000,
    0b00_1101_0000,
    0b00_1110_0000,
    0b00_1111_0000,

    0b00_0000_0000,
    0b01_0000_0000,
    0b10_0000_0000,
    0b11_0000_0000,
  ],
  nbits=10 )

#-------------------------------------------------------------------------
# test_case_nbits10_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(10) ))
def test_case_nbits10_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=10 )

