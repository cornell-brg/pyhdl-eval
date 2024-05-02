#=========================================================================
# Prob04p04_comb_bool_truth_tbl0_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.f = OutPort()

    @update
    def up():
      temp = concat(s.a,s.b)
      if   temp == 0b00: s.f @= 1
      elif temp == 0b01: s.f @= 1
      elif temp == 0b10: s.f @= 1
      elif temp == 0b11: s.f @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.f = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    a,b = test_vector

    ref.a @= a
    ref.b @= b

    dut.a @= a
    dut.b @= b

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.a, dut.b, ">", dut.f )

    assert ref.f == dut.f

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0),
    (0,1),
    (1,0),
    (1,1),
  ])

