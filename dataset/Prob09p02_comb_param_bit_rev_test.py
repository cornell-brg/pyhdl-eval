#=========================================================================
# Prob09p02_comb_param_bit_rev_test
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
    s.out = OutPort(nbits)

    @update
    def up():
      for i in range(0,nbits):
        s.out[i] @= s.in_[nbits-1-i]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in_ = InPort (nbits)
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

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in_, ">", dut.out )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000,
    0b0000_0001,
    0b0000_0010,
    0b0000_0100,
    0b0000_0100,
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
@given( st.lists(pst.bits(8)) )
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0_0000_0000_0000,
    0b0_0000_0000_0001,
    0b0_0000_0000_0010,
    0b0_0000_0000_0100,
    0b0_0000_0000_1000,
    0b0_0000_0001_0001,
    0b0_0000_0010_0010,
    0b0_0000_0100_0100,
    0b0_0000_1000_1000,
    0b0_0001_0001_0001,
    0b0_0010_0010_0010,
    0b0_0100_0100_0100,
    0b0_1000_1000_1000,
    0b1_0001_0001_0001,
    0b1_0101_0101_0101,
    0b0_1010_1010_1010,
    0b1_1111_1111_1111,
  ],
  nbits=13 )

#-------------------------------------------------------------------------
# test_case_nbits13_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists(pst.bits(13)) )
def test_case_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=13 )

