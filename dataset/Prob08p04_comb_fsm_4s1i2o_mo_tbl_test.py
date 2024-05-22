#=========================================================================
# Prob08p04_comb_fsm_4s1i2o_mo_tbl_test
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
    ( "state",      InputPort (2) ),
    ( "in_",        InputPort (1) ),
    ( "state_next", OutputPort(2) ),
    ( "out0",       OutputPort(1) ),
    ( "out1",       OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0 ),
    ( 0, 1 ),
    ( 1, 0 ),
    ( 1, 1 ),
    ( 2, 0 ),
    ( 2, 1 ),
    ( 3, 0 ),
    ( 3, 1 ),
  ])

