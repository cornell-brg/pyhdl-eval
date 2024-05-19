#=========================================================================
# Prob10p04_seq_gates_8b_dff_test
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
    s.d = InPort (8)
    s.q = OutPort(8)

    @update_ff
    def up():
      s.q <<= s.d

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.d = InPort (8)
    s.q = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ 0 ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    d = test_vector

    ref.d @= d
    dut.d @= d

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.d, ">", dut.q )

    if i > 0:
      assert ref.q == dut.q

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x00,
    0x00, # prev: 0 -> 0 0
    0x01, # prev: 0 -> 1 0
    0x01, # prev: 1 -> 1 1
    0x00, # prev: 1 -> 0 1
    0x00,
    0x00,
    0xab,
    0xcd,
    0xef,
    0x00,
    0x00,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

