#=========================================================================
# Prob14p04_seq_edge_8b_any_count_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, InputPort, OutputPort, TraceFormat
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
    ( "clear", InputPort (1) ),
    ( "in_",   InputPort (8) ),
    ( "count", OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_one_bit_toggle
#-------------------------------------------------------------------------

def test_case_one_bit_toggle( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_one_bit_repeat
#-------------------------------------------------------------------------

def test_case_one_bit_repeat( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0001 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_many_bits
#-------------------------------------------------------------------------

def test_case_many_bits( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b1010_1010 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b1010_1010 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b1111_1111 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b1111_1111 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b1010_1010 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b1010_1010 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0100_0100 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_clear
#-------------------------------------------------------------------------

def test_case_directed_clear( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0100_0100 ),
    ( 0, 1, 0b0000_0000 ),
    ( 0, 1, 0b0000_0000 ),
    ( 0, 1, 0b0000_0000 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0100_0100 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs cl in_
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0100_0100 ),
    ( 1, 0, 0b0000_0000 ),
    ( 1, 0, 0b0000_0000 ),
    ( 1, 0, 0b0000_0000 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0101_0101 ),
    ( 0, 0, 0b0001_0001 ),
    ( 0, 0, 0b0100_0100 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
    ( 0, 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), st.just(0), pst.bits(8) ),
                  min_size=20 ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_clear
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1), pst.bits(8) ),
                  min_size=20 ))
def test_case_random_clear( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(8) ),
                  min_size=20 ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

