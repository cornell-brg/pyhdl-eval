#=========================================================================
# Prob02p07_comb_wires_4x2b_array_test
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
    s.in_ = [ InPort (2) for _ in range(4) ]
    s.out = [ OutPort(2) for _ in range(4) ]

    @update
    def up():
      s.out[0] @= s.in_[0]
      s.out[1] @= s.in_[1]
      s.out[2] @= s.in_[2]
      s.out[3] @= s.in_[3]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = [ InPort (2) for _ in range(4) ]
    s.out = [ OutPort(2) for _ in range(4) ]

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0, in1, in2, in3 = test_vector

    ref.in_[0] @= in0
    ref.in_[1] @= in1
    ref.in_[2] @= in2
    ref.in_[3] @= in3

    dut.in_[0] @= in0
    dut.in_[1] @= in1
    dut.in_[2] @= in2
    dut.in_[3] @= in3

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out[0] == dut.out[0] 
    assert ref.out[1] == dut.out[1] 
    assert ref.out[2] == dut.out[2] 
    assert ref.out[3] == dut.out[3] 

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0, 0 ),
    ( 0, 1, 2, 3 ),
    ( 3, 0, 1, 2 ),
    ( 2, 3, 0, 1 ),
    ( 1, 2, 3, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 1, 1, 0 ),
    ( 1, 1, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(2), pst.bits(2), pst.bits(2), pst.bits(2)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

