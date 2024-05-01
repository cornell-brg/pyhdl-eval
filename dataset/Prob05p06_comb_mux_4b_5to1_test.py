#=========================================================================
# Prob05p06_comb_mux_4b_5to1_test
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
    s.in0 = InPort(4)
    s.in1 = InPort(4)
    s.in2 = InPort(4)
    s.in3 = InPort(4)
    s.in4 = InPort(4)
    s.sel = InPort(3)
    s.out = OutPort(4)

    @update
    def up():
      if   s.sel == 0: s.out @= s.in0
      elif s.sel == 1: s.out @= s.in1
      elif s.sel == 2: s.out @= s.in2
      elif s.sel == 3: s.out @= s.in3
      elif s.sel == 4: s.out @= s.in4
      else:            s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0 = InPort(4)
    s.in1 = InPort(4)
    s.in2 = InPort(4)
    s.in3 = InPort(4)
    s.in4 = InPort(4)
    s.sel = InPort(3)
    s.out = OutPort(4)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,in2,in3,in4,sel = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3
    ref.in4 @= in4
    ref.sel @= sel

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3
    dut.in4 @= in4
    dut.sel @= sel

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0,0,0,0),
    (1,0,0,0,0,0),
    (0,0,0,0,0,1),
    (0,1,0,0,0,1),
    (0,0,0,0,0,2),
    (0,0,1,0,0,2),
    (0,0,0,0,0,3),
    (0,0,0,1,0,3),

    (0,0,0,0,0,4),
    (0,0,0,0,1,4),
    (0,0,0,0,0,5),
    (1,1,1,1,1,5),
    (0,0,0,0,0,6),
    (1,1,1,1,1,6),
    (0,0,0,0,0,7),
    (1,1,1,1,1,7),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples( pst.bits(4), pst.bits(4), pst.bits(4), pst.bits(4),
               pst.bits(4), pst.bits(3) )
    ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

