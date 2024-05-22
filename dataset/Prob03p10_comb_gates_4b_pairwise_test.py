#=========================================================================
# Prob03p10_comb_gates_4b_pairwise_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort, TraceFormat
from pyhdl_eval.core import run_sim

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "in_",      InputPort (4) ),
    ( "out_and",  OutputPort(3) ),
    ( "out_or",   OutputPort(3) ),
    ( "out_xnor", OutputPort(3) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0000,
    0b0001,
    0b0010,
    0b0011,
    0b0100,
    0b0101,
    0b0110,
    0b0111,

    0b1000,
    0b1001,
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

