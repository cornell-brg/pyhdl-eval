#=========================================================================
# Prob07p01_comb_arith_8b_incr_test
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
    s.out = OutPort(8)

    @update
    def up():
      s.out @= s.in_ + 1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (8)
    s.out = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_ = test_vector

    ref.in_ @= in_
    dut.in_ @= in_

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in_, f"({dut.in_.int():4})",
                      ">", dut.out, f"({dut.out.int():4})" )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig,
  [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
     16,
     64,
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig,
  [
      -1,
      -2,
      -3,
      -4,
      -5,
      -6,
      -7,
      -8,
     -16,
     -64,
    -128,
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, [127] )

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

