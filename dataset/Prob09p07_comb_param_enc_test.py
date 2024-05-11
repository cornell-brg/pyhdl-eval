#=========================================================================
# Prob09p07_comb_param_enc_test
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

    s.found = Wire()

    @update
    def up():

      s.out   @= 0
      s.found @= 0

      for i in range(nbits):

        # if this is the first bit set to one then record the index to
        # potentially use as the output

        if not s.found and (s.in_[i] == 1):
          s.out   @= i
          s.found @= 1

        # if there is more than one bit set to one then it is an invalid
        # input and we need to set the output to zero

        elif s.found and (s.in_[i] == 1):
          s.out @= 0

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
# test_case_nbit8_valid
#-------------------------------------------------------------------------

def test_case_nbits8_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0001,
    0b0000_0010,
    0b0000_0100,
    0b0000_1000,
    0b0001_0000,
    0b0010_0000,
    0b0100_0000,
    0b1100_0000,
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits8_invalid
#-------------------------------------------------------------------------

def test_case_nbits8_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000,
    0b0001_0001,
    0b0010_0010,
    0b0100_0100,
    0b1000_1000,
    0b1111_1111,
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_nbits6_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits10_valid
#-------------------------------------------------------------------------

def test_case_nbits10_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b00_0000_0001,
    0b00_0000_0010,
    0b00_0000_0100,
    0b00_0000_1000,

    0b00_0001_0000,
    0b00_0010_0000,
    0b00_0100_0000,
    0b00_1000_0000,

    0b01_0000_0000,
    0b10_0000_0000,
  ],
  nbits=10 )

#-------------------------------------------------------------------------
# test_case_nbits10_invalid
#-------------------------------------------------------------------------

def test_case_nbits10_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b00_0000_0000,
    0b00_0001_0001,
    0b00_0010_0010,
    0b00_0100_0100,

    0b00_1000_1000,
    0b01_0001_0000,
    0b10_0010_0000,
    0b11_1111_1111,
  ],
  nbits=10 )

#-------------------------------------------------------------------------
# test_case_nbits10_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(10) ))
def test_case_nbits10_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=10 )

