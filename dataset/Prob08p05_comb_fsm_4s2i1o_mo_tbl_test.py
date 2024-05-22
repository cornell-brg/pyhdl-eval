#=========================================================================
# Prob08p05_comb_fsm_4s2i1o_mo_tbl_test
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
    ( "in_",        InputPort (2) ),
    ( "state_next", OutputPort(2) ),
    ( "out",        OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0b00 ),
    ( 0, 0b01 ),
    ( 0, 0b10 ),
    ( 0, 0b11 ),

    ( 1, 0b00 ),
    ( 1, 0b01 ),
    ( 1, 0b10 ),
    ( 1, 0b11 ),

    ( 2, 0b00 ),
    ( 2, 0b01 ),
    ( 2, 0b10 ),
    ( 2, 0b11 ),

    ( 3, 0b00 ),
    ( 3, 0b01 ),
    ( 3, 0b10 ),
    ( 3, 0b11 ),
  ])

