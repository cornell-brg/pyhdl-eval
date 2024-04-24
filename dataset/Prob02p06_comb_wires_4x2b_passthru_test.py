#=========================================================================
# Prob02p06_comb_wires_4x2b_passthru_test
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
    s.in0  = InPort (2)
    s.in1  = InPort (2)
    s.in2  = InPort (2)
    s.in3  = InPort (2)
    s.out0 = OutPort(2)
    s.out1 = OutPort(2)
    s.out2 = OutPort(2)
    s.out3 = OutPort(2)

    @update
    def up():
      s.out0 @= s.in0
      s.out1 @= s.in1
      s.out2 @= s.in2
      s.out3 @= s.in3

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0  = InPort (2)
    s.in1  = InPort (2)
    s.in2  = InPort (2)
    s.in3  = InPort (2)
    s.out0 = OutPort(2)
    s.out1 = OutPort(2)
    s.out2 = OutPort(2)
    s.out3 = OutPort(2)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0, in1, in2, in3 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out0 == dut.out0
    assert ref.out1 == dut.out1
    assert ref.out2 == dut.out2
    assert ref.out3 == dut.out3

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, [
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

