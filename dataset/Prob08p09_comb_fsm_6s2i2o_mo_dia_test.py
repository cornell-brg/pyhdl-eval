#=========================================================================
# Prob08p09_comb_fsm_6s2i2o_mo_dia_test
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
    ( "state",      InputPort (3) ),
    ( "in_",        InputPort (2) ),
    ( "state_next", OutputPort(3) ),
    ( "out",        OutputPort(2) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
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

    ( 4, 0b00 ),
    ( 4, 0b01 ),
    ( 4, 0b10 ),
    ( 4, 0b11 ),

    ( 5, 0b00 ),
    ( 5, 0b01 ),
    ( 5, 0b10 ),
    ( 5, 0b11 ),
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 6, 0b00 ),
    ( 6, 0b01 ),
    ( 6, 0b10 ),
    ( 6, 0b11 ),

    ( 7, 0b00 ),
    ( 7, 0b01 ),
    ( 7, 0b10 ),
    ( 7, 0b11 ),
  ])

