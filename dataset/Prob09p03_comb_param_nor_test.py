#=========================================================================
# Prob09p03_comb_param_nor_test
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
    s.in_ = InPort(nbits)
    s.out = OutPort()

    @update
    def up():
      s.out @= ~reduce_or ( s.in_ )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in_ = InPort(nbits)
    s.out = OutPort()

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
# test_case_nbits4_directed
#-------------------------------------------------------------------------

def test_case_nbits4_directed( pytestconfig ):
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
  ],
  nbits=4 )

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

