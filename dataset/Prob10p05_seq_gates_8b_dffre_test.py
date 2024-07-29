#=========================================================================
# Prob10p05_seq_gates_8b_dffre_test
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
    ( "en",    InputPort (1) ),
    ( "d",     InputPort (8) ),
    ( "q",     OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    # rs en d
    ( 0, 0, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x01 ),
    ( 0, 1, 0x01 ),
    ( 0, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x01 ),
    ( 0, 0, 0x01 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),

    ( 0, 1, 0x00 ),
    ( 0, 1, 0xab ),
    ( 0, 1, 0xcd ),
    ( 0, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0xab ),
    ( 0, 0, 0xcd ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    # rs en d
    ( 0, 0, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 1, 1, 0x01 ),
    ( 0, 1, 0x00 ),
    ( 0, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 1, 1, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),

    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 1, 0, 0x01 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 1, 0, 0x00 ),
    ( 0, 0, 0x00 ),
    ( 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(8) )))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

