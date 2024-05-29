#=========================================================================
# Prob16p12_seq_fsm_stop_light_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "clk",             InputPort (1) ),
    ( "reset",           InputPort (1) ),
    ( "starting_yellow", InputPort (1) ),
    ( "change",          InputPort (1) ),
    ( "green_on",        OutputPort(1) ),
    ( "yellow_on",       OutputPort(1) ),
    ( "red_on",          OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_startyellow0
#-------------------------------------------------------------------------

def test_case_startyellow0( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs sy ch
    ( 0, 0, 0 ), # G  -> G
    ( 0, 0, 1 ), # G  -> Y1
    ( 0, 0, 0 ), # Y1 -> Y1
    ( 0, 0, 1 ), # Y1 -> R
    ( 0, 0, 0 ), # R  -> R
    ( 0, 0, 1 ), # R  -> G
    ( 0, 0, 0 ), # G  -> G
  ])

#-------------------------------------------------------------------------
# test_case_startyellow1
#-------------------------------------------------------------------------

def test_case_startyellow1( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs sy ch
    ( 0, 1, 0 ), # G  -> G
    ( 0, 1, 1 ), # G  -> Y1
    ( 0, 1, 0 ), # Y1 -> Y1
    ( 0, 1, 1 ), # Y1 -> R
    ( 0, 1, 0 ), # R  -> R
    ( 0, 1, 1 ), # R  -> Y2
    ( 0, 1, 0 ), # Y2 -> Y2
    ( 0, 1, 1 ), # Y2 -> G
    ( 0, 1, 0 ), # G  -> G
  ])

#-------------------------------------------------------------------------
# test_case_startyellow_switch
#-------------------------------------------------------------------------

def test_case_startyellow_switch( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs sy ch
    ( 0, 0, 0 ), # G  -> G
    ( 0, 0, 1 ), # G  -> Y1
    ( 0, 0, 0 ), # Y1 -> Y1
    ( 0, 0, 1 ), # Y1 -> R
    ( 0, 0, 0 ), # R  -> R
    ( 0, 0, 1 ), # R  -> G
    ( 0, 0, 0 ), # G  -> G

    ( 0, 1, 0 ), # G  -> G

    ( 0, 1, 0 ), # G  -> G
    ( 0, 1, 1 ), # G  -> Y1
    ( 0, 1, 0 ), # Y1 -> Y1
    ( 0, 1, 1 ), # Y1 -> R
    ( 0, 1, 0 ), # R  -> R
    ( 0, 1, 1 ), # R  -> Y2
    ( 0, 1, 0 ), # Y2 -> Y2
    ( 0, 1, 1 ), # Y2 -> G
    ( 0, 1, 0 ), # G  -> G
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs sy ch
    ( 0, 0, 0 ), # G  -> G
    ( 0, 0, 1 ), # G  -> Y1
    ( 0, 0, 1 ), # Y1 -> R
    ( 0, 0, 1 ), # R  -> G
    ( 0, 0, 1 ), # G  -> Y1

    ( 1, 1, 0 ),
    ( 1, 1, 0 ),
    ( 1, 1, 0 ),

    ( 0, 1, 0 ), # G  -> G
    ( 0, 1, 1 ), # G  -> Y1
    ( 0, 1, 1 ), # Y1 -> R
    ( 0, 1, 1 ), # R  -> Y2
    ( 0, 1, 1 ), # Y2 -> G
    ( 0, 1, 1 ), # G  -> Y1

    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),

    ( 0, 0, 0 ), # G  -> G
    ( 0, 0, 1 ), # G  -> Y1
    ( 0, 0, 1 ), # Y1 -> R
    ( 0, 0, 1 ), # R  -> G
    ( 0, 0, 1 ), # G  -> Y1
  ])

