#=========================================================================
# Prob03p09_comb_gates_bitwise_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.datatypes import strategies as pst

from test_utils import construct

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in0      = InPort(4)
    s.in1      = InPort(4)
    s.out_and  = OutPort(4)
    s.out_nand = OutPort(4)
    s.out_or   = OutPort(4)
    s.out_nor  = OutPort(4)

    @update
    def up():
      s.out_and  @=    s.in0 & s.in1
      s.out_nand @= ~( s.in0 & s.in1 )
      s.out_or   @=    s.in0 | s.in1
      s.out_nor  @= ~( s.in0 | s.in1 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0      = InPort(4)
    s.in1      = InPort(4)
    s.out_and  = OutPort(4)
    s.out_nand = OutPort(4)
    s.out_or   = OutPort(4)
    s.out_nor  = OutPort(4)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1

    dut.in0 @= in0
    dut.in1 @= in1

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out_and  == dut.out_and
    assert ref.out_nand == dut.out_nand
    assert ref.out_or   == dut.out_or
    assert ref.out_nor  == dut.out_nor

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b0000, 0b0000 ),
    ( 0b0000, 0b1111 ),
    ( 0b1111, 0b0000 ),
    ( 0b1111, 0b1111 ),
    ( 0b1100, 0b1010 ),
    ( 0b0011, 0b0101 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(4), pst.bits(4)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

