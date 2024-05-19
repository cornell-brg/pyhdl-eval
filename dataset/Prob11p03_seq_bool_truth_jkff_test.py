#=========================================================================
# Prob11p03_seq_bool_truth_jkff_test
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
    s.a = InPort()
    s.b = InPort()
    s.q = OutPort()

    @update_ff
    def up():
      if   ( s.a == 0 and s.b == 0 ): s.q <<=  s.q # hold
      elif ( s.a == 0 and s.b == 1 ): s.q <<=    0 # reset
      elif ( s.a == 1 and s.b == 0 ): s.q <<=    1 # set
      elif ( s.a == 1 and s.b == 1 ): s.q <<= ~s.q # toggle

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.q = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # need explicit reset sequence since there is no explicit reset signal

  test_vectors = [ (0,1), (0,1), (0,1) ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    a,b = test_vector

    ref.a @= a
    ref.b @= b

    dut.a @= a
    dut.b @= b

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.a, dut.b, ">", dut.q )

    if i > 2:
      assert ref.q == dut.q

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    # J  K
    ( 0, 0 ),
    ( 0, 0 ),
    ( 1, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 1, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

