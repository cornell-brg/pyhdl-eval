#=========================================================================
# Prob02p02_comb_wires_16b_split_test
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
    s.lo  = OutPort(4)
    s.hi  = OutPort(4)

    @update
    def up():
      s.lo @= s.in_[0:4]
      s.hi @= s.in_[4:8]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
    s.lo  = OutPort(4)
    s.hi  = OutPort(4)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_ = test_vector

    ref.in_ @= in_
    dut.in_ @= in_

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in_, ">", dut.lo, dut.hi )

    assert ref.lo == dut.lo
    assert ref.hi == dut.hi

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0x00,
    0x01,
    0x10,
    0x23,
    0x45,
    0x67,
    0x89,
    0xab,
    0xcd,
    0xef,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists(pst.bits(8)) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

