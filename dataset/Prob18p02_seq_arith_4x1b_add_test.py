#=========================================================================
# Prob18p02_seq_arith_4x1b_add_test
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
    ( "in0",   InputPort (1) ),
    ( "in1",   InputPort (1) ),
    ( "out",   OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs i0 i1
    ( 0, 0, 0 ), # 0000 + 0000
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 1, 0 ), # 0001 + 0000
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 1 ), # 0010 + 0011
    ( 0, 1, 1 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 1, 0 ), # 0011 + 0010
    ( 0, 1, 1 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs i0 i1
    ( 0, 1, 0 ), # 1011 + 0100
    ( 0, 1, 0 ),
    ( 0, 0, 1 ),
    ( 0, 1, 0 ),
    ( 0, 0, 1 ), # 1100 + 0011
    ( 0, 0, 1 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ), # 1101 + 0010
    ( 0, 0, 1 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 0, 0 ), # 0100 + 0100
    ( 0, 0, 0 ),
    ( 0, 1, 1 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs i0 i1
    ( 0, 1, 1 ), # 1111 + 0001
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 0, 1 ), # 1100 + 0111
    ( 0, 0, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 0 ),
    ( 0, 0, 0 ), # 1000 + 1000
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 1, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs i0 i1
    ( 0, 1, 1 ), # 1111 + 0001
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 1 ), # 1111
    ( 0, 1, 0 ),
    ( 1, 0, 0 ), # reset
    ( 1, 0, 0 ), # reset
    ( 1, 0, 0 ), # reset
    ( 0, 1, 1 ), # 1111 + 0001
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 1 ), # 1111 + 0001
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1), pst.bits(1) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(1) ) ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

