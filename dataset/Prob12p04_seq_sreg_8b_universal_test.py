#=========================================================================
# Prob12p04_seq_sreg_8b_universal_test
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
    ( "ld",    InputPort (1) ),
    ( "pin",   InputPort (8) ),
    ( "sin",   InputPort (1) ),
    ( "pout",  OutputPort(8) ),
    ( "sout",  OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_single_ld
#-------------------------------------------------------------------------

def test_case_single_ld( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en ld pin          sin
    ( 0, 0, 0, 0b0000_0000, 0 ), #  0: 0000_0000
    ( 0, 0, 1, 0b1101_0110, 0 ), #  1: 0000_0000
    ( 0, 1, 0, 0b0000_0000, 0 ), #  2: 1101_0110
    ( 0, 1, 0, 0b0000_0000, 1 ), #  3: 1010_1100
    ( 0, 1, 0, 0b0000_0000, 1 ), #  4: 0101_1001
    ( 0, 1, 0, 0b0000_0000, 0 ), #  5: 1011_0011
    ( 0, 1, 0, 0b0000_0000, 1 ), #  6: 0110_0110
    ( 0, 1, 0, 0b0000_0000, 1 ), #  7: 1100_1101
    ( 0, 1, 0, 0b0000_0000, 0 ), #  8: 1001_1011
    ( 0, 1, 0, 0b0000_0000, 1 ), #  9: 0011_0110
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 0110_1101
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 1101_1010
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 1011_0100
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 0110_1000
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 1101_0000
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 1010_0000
    ( 0, 1, 0, 0b0000_0000, 0 ), # 10: 0100_0000
    ( 0, 0, 0, 0b0000_0000, 0 ), # 11: 0100_0000
    ( 0, 0, 0, 0b0000_0000, 0 ), # 12: 0100_0000
  ])

#-------------------------------------------------------------------------
# test_case_multi_ld
#-------------------------------------------------------------------------

def test_case_multi_ld( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en ld pin          sin
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b1101_0110, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b0110_0101, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 1 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b1100_1001, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b1111_1111, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_enable
#-------------------------------------------------------------------------

def test_case_enable( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en ld pin          sin
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b1111_1111, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en ld pin          sin
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 1, 0b1111_1111, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 1, 0, 0, 0b0000_0000, 0 ),
    ( 1, 0, 0, 0b0000_0000, 0 ),
    ( 1, 0, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 1, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
    ( 0, 0, 0, 0b0000_0000, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------
# We need to make sure our random tests are long enough so we can
# observe the output of what we are shifting into the shift register.

@settings(derandomize=True,deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      st.just(0), pst.bits(1), pst.bits(1), pst.bits(8), pst.bits(1)
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

