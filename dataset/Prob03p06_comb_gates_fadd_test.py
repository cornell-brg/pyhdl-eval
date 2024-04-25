#=========================================================================
# Prob03p06_comb_gates_fadd_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.a    = InPort()
    s.b    = InPort()
    s.cin  = InPort()
    s.sum  = OutPort()
    s.cout = OutPort()

    @update
    def up():
      s.sum  @= s.a ^ s.b ^ s.cin
      s.cout @= ( s.a & s.b ) | ( s.a & s.cin ) | ( s.b & s.cin )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.a    = InPort()
    s.b    = InPort()
    s.cin  = InPort()
    s.sum  = OutPort()
    s.cout = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    a,b,cin = test_vector

    ref.a   @= a
    ref.b   @= b
    ref.cin @= cin

    dut.a   @= a
    dut.b   @= b
    dut.cin @= cin

    ref.sim_tick()
    dut.sim_tick()

    assert ref.sum  == dut.sum
    assert ref.cout == dut.cout

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, [
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (0,1,1),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,1,1),
  ] )

