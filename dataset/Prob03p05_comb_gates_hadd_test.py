#=========================================================================
# Prob03p05_comb_gates_hadd_test
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
    ( "a",    InputPort (1) ),
    ( "b",    InputPort (1) ),
    ( "sum",  OutputPort(1) ),
    ( "cout", OutputPort(1) ),
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
    (1,1)
  ])

