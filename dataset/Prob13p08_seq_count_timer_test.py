#=========================================================================
# Prob13p08_seq_count_timer_test
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
    ( "clk",     InputPort (1) ),
    ( "reset",   InputPort (1) ),
    ( "restart", InputPort (1) ),
    ( "tick",    InputPort (1) ),
    ( "run",     InputPort (1) ),
    ( "mins",    OutputPort(6) ),
    ( "secs",    OutputPort(6) ),
  ],
  trace_format=TraceFormat.UINT,
)

#-------------------------------------------------------------------------
# test_case_basic
#-------------------------------------------------------------------------

def test_case_basic( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs st tk rn
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_tick
#-------------------------------------------------------------------------

def test_case_tick( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs st tk rn
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 0, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 0, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_run
#-------------------------------------------------------------------------

def test_case_run( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs st tk rn
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_sec_wraparound
#-------------------------------------------------------------------------

def test_case_sec_wraparound( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,0,1,1)]*150 )

#-------------------------------------------------------------------------
# test_case_saturate
#-------------------------------------------------------------------------

def test_case_saturate( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,0,1,1)]*(60*60+10) )

#-------------------------------------------------------------------------
# test_case_directed_restart
#-------------------------------------------------------------------------

def test_case_directed_restart( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs st tk rn
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 1, 1, 1 ),
    ( 0, 1, 1, 1 ),
    ( 0, 1, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs st tk rn
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 1, 0, 1, 1 ),
    ( 1, 0, 1, 1 ),
    ( 1, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
    ( 0, 0, 1, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      st.just(0), st.just(0), pst.bits(1), pst.bits(1),
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_restart
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      st.just(0), pst.bits(1), pst.bits(1), pst.bits(1),
    ),
    min_size=30
  ))
def test_case_random_restart( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(1), pst.bits(1), pst.bits(1), pst.bits(1),
    ),
    min_size=30
  ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

