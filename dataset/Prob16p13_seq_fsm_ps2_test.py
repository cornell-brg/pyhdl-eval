#=========================================================================
# Prob16p13_seq_fsm_ps2_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim
from pyhdl_eval      import strategies as pst

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "clk",   InputPort (1) ),
    ( "reset", InputPort (1) ),
    ( "in_",   InputPort (8) ),
    ( "done",  OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_simple
#-------------------------------------------------------------------------

def test_case_simple( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 0, 0b0000_0000 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 0, 0b0000_0000 ), # C -> A done=1
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 0, 0b0000_0000 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
  ])

#-------------------------------------------------------------------------
# test_case_consecutive_ones
#-------------------------------------------------------------------------

def test_case_consecutive_ones( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_1000 ), # B -> C
    ( 0, 0b0000_1000 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_1000 ), # B -> C
    ( 0, 0b0000_1000 ), # C -> A done=1
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_1000 ), # B -> C
    ( 0, 0b0000_1000 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0010_0101 ), # A -> A
    ( 0, 0b0101_0010 ), # A -> A
    ( 0, 0b0011_1000 ), # A -> B
    ( 0, 0b1100_1000 ), # B -> C
    ( 0, 0b0011_0010 ), # C -> A done=1
    ( 0, 0b1010_0011 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0101_0100 ), # B -> C
    ( 0, 0b0000_0010 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 1, 0b0000_0000 ), # reset
    ( 1, 0b0000_0000 ), # reset
    ( 1, 0b0000_0000 ), # reset
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 0, 0b0000_0000 ), # C -> A done=1
    ( 0, 0b0000_0000 ), # A -> A
    ( 0, 0b0000_1000 ), # A -> B
    ( 0, 0b0000_0000 ), # B -> C
    ( 0, 0b0000_0000 ), # C -> A done=1
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(8) ), min_size=20 ) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(8) ), min_size=20 ) )
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

