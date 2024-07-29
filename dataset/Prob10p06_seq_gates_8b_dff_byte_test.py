#=========================================================================
# Prob10p06_seq_gates_8b_dff_byte_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

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
    ( "clk", InputPort ( 1) ),
    ( "en",  InputPort ( 2) ),
    ( "d",   InputPort (16) ),
    ( "q",   OutputPort(16) ),
  ],
  dead_cycles=1,
)

#-------------------------------------------------------------------------
# test_case_both_enabled
#-------------------------------------------------------------------------

def test_case_both_enabled( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ), # prev: 0 -> 0 0
    ( 0b11, 0x0201 ), # prev: 0 -> 1 0
    ( 0b11, 0x0201 ), # prev: 1 -> 1 1
    ( 0b11, 0x0000 ), # prev: 1 -> 0 1
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ),
    ( 0b11, 0x4567 ),
    ( 0b11, 0x89ab ),
    ( 0b11, 0xcdef ),
    ( 0b11, 0x0000 ),
    ( 0b11, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_one_enabled
#-------------------------------------------------------------------------

def test_case_one_enabled( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ), # prev: 0 -> 0 0
    ( 0b01, 0x0201 ), # prev: 0 -> 1 0
    ( 0b01, 0x0201 ), # prev: 1 -> 1 1
    ( 0b01, 0x0000 ), # prev: 1 -> 0 1
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ),
    ( 0b01, 0x4567 ),
    ( 0b01, 0x89ab ),
    ( 0b01, 0xcdef ),
    ( 0b01, 0x0000 ),
    ( 0b01, 0x0000 ),

    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ), # prev: 0 -> 0 0
    ( 0b10, 0x0201 ), # prev: 0 -> 1 0
    ( 0b10, 0x0201 ), # prev: 1 -> 1 1
    ( 0b10, 0x0000 ), # prev: 1 -> 0 1
    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ),
    ( 0b10, 0x4567 ),
    ( 0b10, 0x89ab ),
    ( 0b10, 0xcdef ),
    ( 0b10, 0x0000 ),
    ( 0b10, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_none_enabled
#-------------------------------------------------------------------------

def test_case_none_enabled( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ), # prev: 0 -> 0 0
    ( 0b00, 0x0201 ), # prev: 0 -> 1 0
    ( 0b00, 0x0201 ), # prev: 1 -> 1 1
    ( 0b00, 0x0000 ), # prev: 1 -> 0 1
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ),
    ( 0b00, 0x4567 ),
    ( 0b00, 0x89ab ),
    ( 0b00, 0xcdef ),
    ( 0b00, 0x0000 ),
    ( 0b00, 0x0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(2), pst.bits(16) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

