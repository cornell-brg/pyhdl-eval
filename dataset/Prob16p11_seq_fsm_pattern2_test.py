#=========================================================================
# Prob16p11_seq_fsm_pattern2_test
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
    ( "in_",   InputPort (1) ),
    ( "out",   OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0 ), # A -> A
    ( 0, 1 ), # A -> B
    ( 0, 0 ), # B -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 0 ), # C -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 1 ), # C -> D
    ( 0, 1 ), # D -> D
    ( 0, 0 ), # D -> E out=1
    ( 0, 0 ), # E -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 1 ), # C -> D
    ( 0, 0 ), # D -> E out=1
    ( 0, 1 ), # E -> B
    ( 0, 0 ), # B -> A
    ( 0, 0 ), # A -> A
  ])

#-------------------------------------------------------------------------
# test_case_patterns
#-------------------------------------------------------------------------

def test_case_patterns( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 1 ), # 1110
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 1 ), # 11110
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 1 ), # 11101110
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 1 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0 ), # A -> A
    ( 0, 1 ), # A -> B
    ( 0, 0 ), # B -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 0 ), # C -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 1 ), # C -> D
    ( 0, 1 ), # D -> D
    ( 0, 0 ), # D -> E out=1
    ( 0, 1 ), # E -> B
    ( 1, 0 ), # reset
    ( 0, 0 ), # A -> A
    ( 0, 1 ), # A -> B
    ( 0, 0 ), # B -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 0 ), # C -> A
    ( 0, 1 ), # A -> B
    ( 0, 1 ), # B -> C
    ( 0, 1 ), # C -> D
    ( 0, 1 ), # D -> D
    ( 0, 0 ), # D -> E out=1
    ( 0, 1 ), # E -> B
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1) ), min_size=20 ) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1) ), min_size=20 ) )
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

