#=========================================================================
# Prob04p13_comb_bool_nl_lights_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.dark           = InPort()
    s.movement       = InPort()
    s.force_on       = InPort()
    s.turn_on_lights = OutPort()

    @update
    def up():
      s.turn_on_lights @= (s.dark & s.movement) | s.force_on

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.dark           = InPort()
    s.movement       = InPort()
    s.force_on       = InPort()
    s.turn_on_lights = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    dark,movement,force_on = test_vector

    ref.dark     @= dark
    ref.movement @= movement
    ref.force_on @= force_on

    dut.dark     @= dark
    dut.movement @= movement
    dut.force_on @= force_on

    ref.sim_tick()
    dut.sim_tick()

    assert ref.turn_on_lights == dut.turn_on_lights

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (0,1,1),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,1,1),
  ])

