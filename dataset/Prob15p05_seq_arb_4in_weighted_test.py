#=========================================================================
# Prob15p05_seq_arb_4in_weighted_test
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
    ( "clk",    InputPort (1) ),
    ( "reset",  InputPort (1) ),
    ( "preset", InputPort (1) ),
    ( "reqs",   InputPort (4) ),
    ( "grants", OutputPort(4) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_one_req
#-------------------------------------------------------------------------

def test_case_one_req( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b0000 ),
    ( 0, 0, 0b0001 ),
    ( 0, 0, 0b0010 ),
    ( 0, 0, 0b0100 ),
    ( 0, 0, 0b1000 ),
    ( 0, 0, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_all_requesters
#-------------------------------------------------------------------------

def test_case_all_reqs( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b0000 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b0000 ),
  ])

#-------------------------------------------------------------------------
# test_case_weighted_all
#-------------------------------------------------------------------------

def test_case_weighted_all( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
  ])

#-------------------------------------------------------------------------
# test_case_weighted_01
#-------------------------------------------------------------------------

def test_case_weighted_01( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b0011 ),
  ])

#-------------------------------------------------------------------------
# test_case_weighted_23
#-------------------------------------------------------------------------

def test_case_weighted_23( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1100 ),
  ])

#-------------------------------------------------------------------------
# test_case_weighted_12
#-------------------------------------------------------------------------

def test_case_weighted_12( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0110 ),
  ])

#-------------------------------------------------------------------------
# test_case_weighted_mixed
#-------------------------------------------------------------------------

def test_case_weighted_mixed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0111 ),
    ( 0, 0, 0b1110 ),
    ( 0, 0, 0b0000 ),
    ( 0, 0, 0b0100 ),
    ( 0, 0, 0b0010 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b0110 ),
    ( 0, 0, 0b0011 ),
    ( 0, 0, 0b1100 ),
    ( 0, 0, 0b1111 ),
  ])

#-------------------------------------------------------------------------
# test_case_preset
#-------------------------------------------------------------------------

def test_case_preset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 1, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs pr reqs
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 1, 0, 0b1111 ),
    ( 1, 0, 0b1111 ),
    ( 1, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
    ( 0, 0, 0b1111 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), st.just(0), pst.bits(4) ),
                  min_size=5 ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_preset
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(1), pst.bits(4) ),
                  min_size=20 ))
def test_case_random_preset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(4) ),
                  min_size=20 ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

