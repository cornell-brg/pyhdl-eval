#=========================================================================
# Prob04p14_comb_bool_nl_ringer_test
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
    ( "vibrate_mode",   InputPort (1) ),
    ( "ring",           InputPort (1) ),
    ( "turn_on_ringer", OutputPort(1) ),
    ( "turn_on_motor",  OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (0,0),
    (0,1),
    (1,0),
    (1,1),
  ])

