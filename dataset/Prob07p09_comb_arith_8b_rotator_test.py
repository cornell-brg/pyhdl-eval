#=========================================================================
# Prob07p09_comb_arith_8b_rotator_test
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
  def construct( s ):
    s.in_ = InPort (8)
    s.amt = InPort (3)
    s.op  = InPort ()
    s.out = OutPort(8)

    s.temp = Wire(16)

    @update
    def up():
      if ( s.op == 0 ):
        s.temp @= concat( s.in_, s.in_ ) << zext( s.amt, 16 )
        s.out  @= s.temp[8:16]
      else:
        s.temp @= concat( s.in_, s.in_ ) >> zext( s.amt, 16 )
        s.out  @= s.temp[0:8]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
    s.amt = InPort (3)
    s.op  = InPort ()
    s.out = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_,amt,op = test_vector

    ref.in_ @= in_
    ref.amt @= amt
    ref.op  @= op

    dut.in_ @= in_
    dut.amt @= amt
    dut.op  @= op

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, f"{dut.in_.uint():#010b}", dut.amt, dut.op,
                      ">", f"{dut.out.uint():#010b}" )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_left_rotate
#-------------------------------------------------------------------------

def test_case_left_rotate( pytestconfig ):
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
  ])

#-------------------------------------------------------------------------
# test_case_right_rotate
#-------------------------------------------------------------------------

def test_case_right_rotate( pytestconfig ):
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
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3), pst.bits(1) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

