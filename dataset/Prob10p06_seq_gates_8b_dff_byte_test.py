#=========================================================================
# Prob10p06_seq_gates_8b_dff_byte_test
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
    s.en = InPort ( 2)
    s.d  = InPort (16)
    s.q  = OutPort(16)

    s.tmp = Wire(16)

    @update
    def wdata():
      s.tmp[0:8]  @= s.d[ 0:8] if s.en[0] else s.q[ 0:8]
      s.tmp[8:16] @= s.d[8:16] if s.en[1] else s.q[8:16]

    @update_ff
    def up():
      s.q <<= s.tmp

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.en = InPort ( 2)
    s.d  = InPort (16)
    s.q  = OutPort(16)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  # module does not include a reset, so we need to add initial inputs to
  # avoid checking outputs when those outputs are undefined

  test_vectors = [ (0,0) ] + test_vectors

  for i,test_vector in enumerate(test_vectors):

    en,d = test_vector

    ref.en @= en
    ref.d  @= d

    dut.en @= en
    dut.d  @= d

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.en, dut.d, ">", dut.q )

    if i > 0:
      assert ref.q == dut.q

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_both_enabled
#-------------------------------------------------------------------------

def test_case_both_enabled( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ), # prev: 0 -> 0 0
    ( 0b11, 0x0201 ), # prev: 0 -> 1 0
    ( 0b11, 0x0201 ), # prev: 1 -> 1 1
    ( 0b11, 0x0000 ), # prev: 1 -> 0 1
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ),
    ( 0b11, 0x4567 ),
    ( 0b11, 0x89ab ),
    ( 0b11, 0xcdef ),
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_one_enabled
#-------------------------------------------------------------------------

def test_case_one_enabled( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ), # prev: 0 -> 0 0
    ( 0b01, 0x0201 ), # prev: 0 -> 1 0
    ( 0b01, 0x0201 ), # prev: 1 -> 1 1
    ( 0b01, 0x0000 ), # prev: 1 -> 0 1
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ),
    ( 0b01, 0x4567 ),
    ( 0b01, 0x89ab ),
    ( 0b01, 0xcdef ),
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ),

    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ), # prev: 0 -> 0 0
    ( 0b10, 0x0201 ), # prev: 0 -> 1 0
    ( 0b10, 0x0201 ), # prev: 1 -> 1 1
    ( 0b10, 0x0000 ), # prev: 1 -> 0 1
    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ),
    ( 0b10, 0x4567 ),
    ( 0b10, 0x89ab ),
    ( 0b10, 0xcdef ),
    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_none_enabled
#-------------------------------------------------------------------------

def test_case_none_enabled( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ), # prev: 0 -> 0 0
    ( 0b00, 0x0201 ), # prev: 0 -> 1 0
    ( 0b00, 0x0201 ), # prev: 1 -> 1 1
    ( 0b00, 0x0000 ), # prev: 1 -> 0 1
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ),
    ( 0b00, 0x4567 ),
    ( 0b00, 0x89ab ),
    ( 0b00, 0xcdef ),
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(2), pst.bits(16) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

