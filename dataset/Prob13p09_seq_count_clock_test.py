#=========================================================================
# Prob13p09_seq_count_clock_test
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
# Need to use set_ instead of set otherwise Verilator will complain that
# set is a C++ common word.

config = Config(
  ports = [
    ( "clk",       InputPort (1) ),
    ( "reset",     InputPort (1) ),
    ( "tick",      InputPort (1) ),
    ( "set_en",    InputPort (1) ),
    ( "set_hours", InputPort (4) ),
    ( "set_mins",  InputPort (6) ),
    ( "set_pm",    InputPort (1) ),
    ( "hours",     OutputPort(4) ),
    ( "mins",      OutputPort(6) ),
    ( "pm",        OutputPort(1) ),
  ],
  trace_format=TraceFormat.UINT,
)

#-------------------------------------------------------------------------
# test_case_basic
#-------------------------------------------------------------------------

def test_case_basic( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr mi pm
    ( 0, 0, 1, 1, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_tick
#-------------------------------------------------------------------------

def test_case_tick( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr mi pm
    ( 0, 0, 1, 1, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 0, 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_multi_set
#-------------------------------------------------------------------------

def test_case_multi_set( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr  mi pm
    ( 0, 0, 1,  1,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),

    ( 0, 0, 1, 10, 30, 1 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),

    ( 0, 0, 1,  7, 45, 1 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_min_wraparound
#-------------------------------------------------------------------------

def test_case_min_wraparound( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr mi pm
    ( 0, 0, 1, 1, 50, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
    ( 0, 1, 0, 0,  0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_hour_wraparound
#-------------------------------------------------------------------------

def test_case_hour_wraparound( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr  mi pm
    ( 0, 0, 1, 11, 55, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),

    ( 0, 0, 1, 12, 55, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),

    ( 0, 0, 1, 11, 55, 1 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),

    ( 0, 0, 1, 12, 55, 1 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
    ( 0, 1, 0,  0,  0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs tk st hr mi pm
    ( 0, 0, 1, 1, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 1, 1, 0, 0, 0, 0 ),
    ( 1, 1, 0, 0, 0, 0 ),
    ( 1, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
    ( 0, 1, 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      st.just(0), pst.bits(1), pst.bits(1),
      pst.bits(4, min_value=1, max_value=12 ), # hours
      pst.bits(6, min_value=0, max_value=59 ), # mins
      pst.bits(1)
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(1), pst.bits(1), pst.bits(1),
      pst.bits(4, min_value=1, max_value=12 ), # hours
      pst.bits(6, min_value=0, max_value=59 ), # mins
      pst.bits(1)
    ),
    min_size=30
  ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

