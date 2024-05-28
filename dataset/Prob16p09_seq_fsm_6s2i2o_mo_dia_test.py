#=========================================================================
# Prob16p09_seq_fsm_6s2i2o_mo_dia_test
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
    ( "in_",   InputPort (2) ),
    ( "state", OutputPort(3) ),
    ( "out",   OutputPort(2) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b00 ), # A -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b01 ), # B -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b00 ), # C -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b00 ), # D -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b00 ), # D -> C
    ( 0, 0b00 ), # C -> A
    ( 0, 0b00 ), # A -> A

    ( 0, 0b10 ), # A -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b10 ), # B -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b10 ), # C -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b10 ), # D -> A
    ( 0, 0b00 ), # A -> A

    ( 0, 0b11 ), # A -> E
    ( 0, 0b10 ), # E -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b11 ), # B -> E
    ( 0, 0b10 ), # E -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b11 ), # C -> E
    ( 0, 0b10 ), # E -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b11 ), # D -> E
    ( 0, 0b10 ), # E -> A
    ( 0, 0b11 ), # A -> E
    ( 0, 0b11 ), # E -> E
    ( 0, 0b10 ), # E -> A
    ( 0, 0b00 ), # A -> A

    ( 0, 0b11 ), # A -> E
    ( 0, 0b00 ), # E -> F
    ( 0, 0b00 ), # F -> A
    ( 0, 0b11 ), # A -> E
    ( 0, 0b01 ), # E -> F
    ( 0, 0b01 ), # F -> A
    ( 0, 0b11 ), # A -> E
    ( 0, 0b00 ), # E -> F
    ( 0, 0b10 ), # F -> A
    ( 0, 0b11 ), # A -> E
    ( 0, 0b00 ), # E -> F
    ( 0, 0b11 ), # F -> A
    ( 0, 0b00 ), # A -> A
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b00 ), # A -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b01 ), # B -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b00 ), # C -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b00 ), # D -> C
    ( 1, 0b00 ), # reset
    ( 0, 0b00 ), # A -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b01 ), # B -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b00 ), # C -> A
    ( 0, 0b01 ), # A -> B
    ( 0, 0b00 ), # B -> C
    ( 0, 0b01 ), # C -> D
    ( 0, 0b00 ), # D -> C
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(2) ), min_size=30 ) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(2) ), min_size=20 ) )
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

