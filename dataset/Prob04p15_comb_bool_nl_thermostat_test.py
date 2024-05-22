#=========================================================================
# Prob04p15_comb_bool_nl_thermostat_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "mode",     InputPort (1) ),
    ( "too_cold", InputPort (1) ),
    ( "too_hot",  InputPort (1) ),
    ( "fan_on",   InputPort (1) ),
    ( "heater",   OutputPort(1) ),
    ( "aircon",   OutputPort(1) ),
    ( "fan",      OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
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
  ])

