#=========================================================================
# Prob05p03_comb_mux_1b_1to8_test
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
    ( "in_",  InputPort (1) ),
    ( "sel",  InputPort (3) ),
    ( "out0", OutputPort(1) ),
    ( "out1", OutputPort(1) ),
    ( "out2", OutputPort(1) ),
    ( "out3", OutputPort(1) ),
    ( "out4", OutputPort(1) ),
    ( "out5", OutputPort(1) ),
    ( "out6", OutputPort(1) ),
    ( "out7", OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (0,0),
    (1,0),
    (0,1),
    (1,1),
    (0,2),
    (1,2),
    (0,3),
    (1,3),

    (0,4),
    (1,4),
    (0,5),
    (1,5),
    (0,6),
    (1,6),
    (0,7),
    (1,7),
  ])

