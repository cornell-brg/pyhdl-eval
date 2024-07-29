#=========================================================================
# Prob13p03_seq_count_3b_bin_dn_test
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
    ( "out",   OutputPort(3) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_basic
#-------------------------------------------------------------------------

def test_case_basic( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [0]*5 )

#-------------------------------------------------------------------------
# test_case_wraparound
#-------------------------------------------------------------------------

def test_case_wraparound( pytestconfig ):
  run_sim( pytestconfig, __file__, config, [0]*20 )

#-------------------------------------------------------------------------
# test_case_directed_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
def test_case_directed_reset( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
           [ 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0 ])

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------

@pytest.mark.multi_reset
@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(1), min_size=20 ) )
def test_case_random_reset( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

