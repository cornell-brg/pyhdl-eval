#=========================================================================
# Prob08p01_comb_fsm_4s1i1o_mo_tbl0_test
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
    ( "state",      InputPort (4) ),
    ( "in_",        InputPort (1) ),
    ( "state_next", OutputPort(4) ),
    ( "out",        OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b0001, 0 ),
    ( 0b0001, 1 ),
    ( 0b0010, 0 ),
    ( 0b0010, 1 ),
    ( 0b0100, 0 ),
    ( 0b0100, 1 ),
    ( 0b1000, 0 ),
    ( 0b1000, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b0000, 0 ),
    ( 0b0000, 1 ),
    # ( 0b0001, 0 ), valid
    # ( 0b0001, 1 ), valid

    # ( 0b0010, 0 ), valid
    # ( 0b0010, 1 ), valid
    ( 0b0011, 0 ),
    ( 0b0011, 1 ),

    # ( 0b0100, 0 ), valid
    # ( 0b0100, 1 ), valid
    ( 0b0101, 0 ),
    ( 0b0101, 1 ),

    ( 0b0110, 0 ),
    ( 0b0110, 1 ),
    ( 0b0111, 0 ),
    ( 0b0111, 1 ),

    # ( 0b1000, 0 ), valid
    # ( 0b1000, 1 ), valid
    ( 0b1001, 0 ),
    ( 0b1001, 1 ),

    ( 0b1010, 0 ),
    ( 0b1010, 1 ),
    ( 0b1011, 0 ),
    ( 0b1011, 1 ),

    ( 0b1100, 0 ),
    ( 0b1100, 1 ),
    ( 0b1101, 0 ),
    ( 0b1101, 1 ),

    ( 0b1110, 0 ),
    ( 0b1110, 1 ),
    ( 0b1111, 0 ),
    ( 0b1111, 1 ),
  ])
