#=========================================================================
# Prob04p14_comb_bool_nl_ringer_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.vibrate_mode   = InPort()
    s.ring           = InPort()
    s.turn_on_ringer = OutPort()
    s.turn_on_motor  = OutPort()

    @update
    def up():
      s.turn_on_ringer @= ~s.vibrate_mode & s.ring
      s.turn_on_motor  @=  s.vibrate_mode & s.ring

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.vibrate_mode   = InPort()
    s.ring           = InPort()
    s.turn_on_ringer = OutPort()
    s.turn_on_motor  = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    vibrate_mode,ring = test_vector

    ref.vibrate_mode @= vibrate_mode
    ref.ring         @= ring

    dut.vibrate_mode @= vibrate_mode
    dut.ring         @= ring

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.vibrate_mode, dut.ring, ">",
                      dut.turn_on_ringer, dut.turn_on_motor )

    assert ref.turn_on_ringer == dut.turn_on_ringer
    assert ref.turn_on_motor  == dut.turn_on_motor

    ref.sim_tick()
    dut.sim_tick()

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

