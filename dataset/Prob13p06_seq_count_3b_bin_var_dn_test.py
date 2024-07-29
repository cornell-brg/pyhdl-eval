#=========================================================================
# Prob13p06_seq_count_3b_bin_var_dn_test
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
    ( "ld",    InputPort (1) ),
    ( "in_",   InputPort (3) ),
    ( "out",   OutputPort(3) ),
    ( "done",  OutputPort(1) ),
  ],
  dead_cycles=1,
  dead_cycle_inputs=(1,0),
)

#-------------------------------------------------------------------------
# test_case_done
#-------------------------------------------------------------------------

def test_case_done( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ld in_
    ( 1, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_count4
#-------------------------------------------------------------------------

def test_case_count4( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ld in_
    ( 1, 4 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_count7
#-------------------------------------------------------------------------

def test_case_count7( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ld in_
    ( 1, 7 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_multi_ld
#-------------------------------------------------------------------------

def test_case_multi_ld( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ld in_
    ( 1, 5 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 1, 3 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(3) ), min_size=20 ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

