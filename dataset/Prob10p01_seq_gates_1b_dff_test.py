#=========================================================================
# Prob10p01_seq_gates_1b_dff_test
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
    ( "clk", InputPort (1) ),
    ( "d",   InputPort (1) ),
    ( "q",   OutputPort(1) ),
  ],
  dead_cycles=1,
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0,
    0, # prev: 0 -> 0 0
    1, # prev: 0 -> 1 0
    1, # prev: 1 -> 1 1
    0, # prev: 1 -> 0 1
    0,
  ])

