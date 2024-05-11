#=========================================================================
# Prob07p07_comb_arith_8b_shifter_test
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
    s.out = OutPort(8)

    @update
    def up():
      s.out @= trunc( sext( s.in_, 16 ) >> zext( s.amt, 16 ), 8 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
    s.amt = InPort (3)
    s.out = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_,amt = test_vector

    ref.in_ @= in_
    ref.amt @= amt

    dut.in_ @= in_
    dut.amt @= amt

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, f"{dut.in_.uint():#010b}", dut.amt,
                      ">", f"{dut.out.uint():#010b}" )

    assert ref.out == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b0110_0101, 0 ),
    ( 0b0110_0101, 1 ),
    ( 0b0110_0101, 2 ),
    ( 0b0110_0101, 3 ),
    ( 0b0110_0101, 4 ),
    ( 0b0110_0101, 5 ),
    ( 0b0110_0101, 6 ),
    ( 0b0110_0101, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b1101_0101, 0 ),
    ( 0b1101_0101, 1 ),
    ( 0b1101_0101, 2 ),
    ( 0b1101_0101, 3 ),
    ( 0b1101_0101, 4 ),
    ( 0b1101_0101, 5 ),
    ( 0b1101_0101, 6 ),
    ( 0b1101_0101, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

