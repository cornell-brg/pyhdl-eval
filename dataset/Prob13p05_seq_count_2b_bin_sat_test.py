#=========================================================================
# Prob13p05_seq_count_2b_bin_sat_test
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
    ( "op",    InputPort (1) ),
    ( "out",   OutputPort(2) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_up
#-------------------------------------------------------------------------

def test_case_up( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,1,0)]*2 )

#-------------------------------------------------------------------------
# test_case_up_saturate
#-------------------------------------------------------------------------

def test_case_up_saturate( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,1,0)]*7 )

#-------------------------------------------------------------------------
# test_case_dn
#-------------------------------------------------------------------------

def test_case_dn( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,1,1)]*3 )

#-------------------------------------------------------------------------
# test_case_dn_saturate
#-------------------------------------------------------------------------

def test_case_dn_saturate( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [(0,1,1)]*7 )

#-------------------------------------------------------------------------
# test_case_up_dn
#-------------------------------------------------------------------------

def test_case_up_dn( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en op
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_enable
#-------------------------------------------------------------------------

def test_case_enable( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en op
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 0, 1 ),
    ( 0, 0, 1 ),
    ( 0, 0, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # rs en op
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 1, 1, 0 ),
    ( 1, 1, 0 ),
    ( 1, 1, 0 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 0, 1, 1 ),
    ( 1, 1, 0 ),
    ( 1, 1, 0 ),
    ( 1, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
    ( 0, 1, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      st.just(0), pst.bits(1), pst.bits(1)
    ),
    min_size=20
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
      pst.bits(1), pst.bits(1), pst.bits(1)
    ),
    min_size=20
  ))
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

