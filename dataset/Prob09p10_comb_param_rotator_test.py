#=========================================================================
# Prob09p10_comb_param_rotator_test
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
    s.amt = InPort (clog2(nbits))
    s.op  = InPort ()
    s.out = OutPort(nbits)

    s.temp = Wire(2*nbits)

    @update
    def up():
      if ( s.op == 0 ):
        s.temp @= concat( s.in_, s.in_ ) << zext( s.amt, 2*nbits )
        s.out  @= s.temp[nbits:2*nbits]
      else:
        s.temp @= concat( s.in_, s.in_ ) >> zext( s.amt, 2*nbits )
        s.out  @= s.temp[0:nbits]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in_ = InPort (nbits)
    s.amt = InPort (clog2(nbits))
    s.op  = InPort ()
    s.out = OutPort(nbits)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors, nbits ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nbits=nbits )

  for test_vector in test_vectors:

    in_,amt,op = test_vector

    ref.in_ @= in_
    ref.amt @= amt
    ref.op  @= op

    dut.in_ @= in_
    dut.amt @= amt
    dut.op  @= op

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in_, dut.amt, dut.op, ">", dut.out )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_nbits4_left_rotate
#-------------------------------------------------------------------------

def test_case_nbits4_left_rotate( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b1101, 0, 0 ),
    ( 0b1101, 1, 0 ),
    ( 0b1101, 2, 0 ),
    ( 0b1101, 3, 0 ),
  ],
  nbits=4 )

#-------------------------------------------------------------------------
# test_case_nbits4_right_rotate
#-------------------------------------------------------------------------

def test_case_nbits4_right_rotate( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b1101, 0, 1 ),
    ( 0b1101, 1, 1 ),
    ( 0b1101, 2, 1 ),
    ( 0b1101, 3, 1 ),
  ],
  nbits=4 )

#-------------------------------------------------------------------------
# test_case_nbits4_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(4), pst.bits(2), pst.bits(1) ) ))
def test_case_nbits4_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=4 )

#-------------------------------------------------------------------------
# test_case_nbits8_left_rotate
#-------------------------------------------------------------------------

def test_case_nbits8_left_rotate( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b0101_1101, 0, 0 ),
    ( 0b0101_1101, 1, 0 ),
    ( 0b0101_1101, 2, 0 ),
    ( 0b0101_1101, 3, 0 ),
    ( 0b0101_1101, 4, 0 ),
    ( 0b0101_1101, 5, 0 ),
    ( 0b0101_1101, 6, 0 ),
    ( 0b0101_1101, 7, 0 ),
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits8_right_rotate
#-------------------------------------------------------------------------

def test_case_nbits8_right_rotate( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b1101_0101, 0, 1 ),
    ( 0b1101_0101, 1, 1 ),
    ( 0b1101_0101, 2, 1 ),
    ( 0b1101_0101, 3, 1 ),
    ( 0b1101_0101, 4, 1 ),
    ( 0b1101_0101, 5, 1 ),
    ( 0b1101_0101, 6, 1 ),
    ( 0b1101_0101, 7, 1 ),
  ],
  nbits=8 )

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3), pst.bits(1) ) ))
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=8 )

