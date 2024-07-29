#=========================================================================
# Prob18p03_seq_arith_2x4b_add_test
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
    ( "in0",   InputPort (4) ),
    ( "in1",   InputPort (4) ),
    ( "out",   OutputPort(4) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in0     i1
    ( 0, 0b0000, 0b0000 ), # 0000_0000 + 0000_0000
    ( 0, 0b0000, 0b0000 ),
    ( 0, 0b0001, 0b0001 ), # 0000_0001 + 0000_0001
    ( 0, 0b0000, 0b0000 ),
    ( 0, 0b0010, 0b0011 ), # 0000_0010 + 0000_0011
    ( 0, 0b0000, 0b0000 ),
    ( 0, 0b0011, 0b0010 ), # 0000_0011 + 0000_0010
    ( 0, 0b0000, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in0     in1
    ( 0, 0b0000, 0b0000 ), # 1011_0000 + 0100_0000
    ( 0, 0b1011, 0b0100 ),
    ( 0, 0b0000, 0b0000 ), # 1100_0000 + 0011_0000
    ( 0, 0b1100, 0b0011 ),
    ( 0, 0b0000, 0b0000 ), # 1101_0000 + 0010_0000
    ( 0, 0b1101, 0b0010 ),
    ( 0, 0b0000, 0b0000 ), # 0100_0000 + 0100_000
    ( 0, 0b0100, 0b0100 ),
  ])

#-------------------------------------------------------------------------
# test_case_carry
#-------------------------------------------------------------------------

def test_case_carry( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in0     in1
    ( 0, 0b1000, 0b1000 ), # 0000_1000 + 0000_1000
    ( 0, 0b0000, 0b0000 ),
    ( 0, 0b1000, 0b1000 ), # 0000_1000 + 0001_1000
    ( 0, 0b0000, 0b0001 ),
    ( 0, 0b1000, 0b1000 ), # 0001_1000 + 0000_1000
    ( 0, 0b0001, 0b0000 ),
    ( 0, 0b1111, 0b0001 ), # 0111_1111 + 0000_0001
    ( 0, 0b0111, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs in0     in1
    ( 0, 0b0000, 0b0000 ), # 1111_0000 + 0001_0000
    ( 0, 0b1111, 0b0001 ),
    ( 0, 0b0000, 0b0000 ), # 1100_0000 + 0111_0000
    ( 0, 0b1100, 0b0111 ),
    ( 0, 0b0000, 0b0000 ), # 1000_0000 + 1000_0000
    ( 0, 0b1000, 0b1000 ),
    ( 0, 0b1111, 0b0001 ), # 1111_1111 + 0000_0001
    ( 0, 0b1111, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs i0 i1
    ( 0, 0b1111, 0b0001 ), # 1111_1111 + 0000_0001
    ( 0, 0b1111, 0b0000 ),
    ( 0, 0b1111, 0b0001 ), # 1111_1111 + 0000_0001
    ( 1, 0b0000, 0b0000 ), # reset
    ( 1, 0b0000, 0b0000 ), # reset
    ( 1, 0b0000, 0b0000 ), # reset
    ( 0, 0b1111, 0b0001 ), # 1111_1111 + 0000_0001
    ( 0, 0b1111, 0b0000 ),
    ( 0, 0b1111, 0b0001 ), # 1111_1111 + 0000_0001
    ( 0, 0b1111, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(4), pst.bits(4) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(4), pst.bits(4) ) ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

