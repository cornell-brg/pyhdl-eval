#=========================================================================
# Prob11p05_seq_bool_waveform1_test
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
    ( "a",   InputPort (1) ),
    ( "f",   OutputPort(1) ),
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

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------
# This was the example provided in the prompt.

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    1,
    0,
    0,
    0,
    0,
    1,
    1,
    0,
    1,
    0,
    0,
    1,
    1,
    0,
    1,
    0,
    1,
    1,
    0,
    1,
    0,
  ])

