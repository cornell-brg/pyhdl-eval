#=========================================================================
# Prob14p03_seq_edge_8b_capture_test
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
    ( "in_",   InputPort (8) ),
    ( "out",   OutputPort(8) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_one_bit_toggle
#-------------------------------------------------------------------------

def test_case_one_bit_toggle( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_one_bit_repeat
#-------------------------------------------------------------------------

def test_case_one_bit_repeat( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0001 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_many_bits
#-------------------------------------------------------------------------

def test_case_many_bits( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ),
    ( 0, 0b1010_1010 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b1010_1010 ),
    ( 0, 0b0101_0101 ),
    ( 0, 0b1111_1111 ),
    ( 0, 0b0101_0101 ),
    ( 0, 0b1111_1111 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b1010_1010 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b1010_1010 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0101_0101 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0100_0100 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in_
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0101_0101 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0100_0100 ),
    ( 1, 0b0000_0000 ),
    ( 1, 0b0000_0000 ),
    ( 1, 0b0000_0000 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0101_0101 ),
    ( 0, 0b0001_0001 ),
    ( 0, 0b0100_0100 ),
    ( 0, 0b0000_0000 ),
    ( 0, 0b0000_0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(8) )))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

