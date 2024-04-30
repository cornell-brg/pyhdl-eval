#=========================================================================
# Prob04p15_comb_bool_nl_thermostat_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.mode     = InPort()
    s.too_cold = InPort()
    s.too_hot  = InPort()
    s.fan_on   = InPort()
    s.heater   = OutPort()
    s.aircon   = OutPort()
    s.fan      = OutPort()

    @update
    def up():
      s.heater @=  s.mode & s.too_cold;
      s.aircon @= ~s.mode & s.too_hot;
      s.fan    @= s.heater | s.aircon | s.fan_on;

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.mode     = InPort()
    s.too_cold = InPort()
    s.too_hot  = InPort()
    s.fan_on   = InPort()
    s.heater   = OutPort()
    s.aircon   = OutPort()
    s.fan      = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    mode,too_cold,too_hot,fan_on = test_vector

    ref.mode     @= mode
    ref.too_cold @= too_cold
    ref.too_hot  @= too_hot
    ref.fan_on   @= fan_on

    dut.mode     @= mode
    dut.too_cold @= too_cold
    dut.too_hot  @= too_hot
    dut.fan_on   @= fan_on

    ref.sim_tick()
    dut.sim_tick()

    assert ref.heater == dut.heater
    assert ref.aircon == dut.aircon
    assert ref.fan    == dut.fan

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, [

    (0,0,0,0),
    (0,0,0,1),
    (0,0,1,0),
    (0,0,1,1),
    (0,1,0,0),
    (0,1,0,1),
    (0,1,1,0),
    (0,1,1,1),

    (1,0,0,0),
    (1,0,0,1),
    (1,0,1,0),
    (1,0,1,1),
    (1,1,0,0),
    (1,1,0,1),
    (1,1,1,0),
    (1,1,1,1),

  ] )

