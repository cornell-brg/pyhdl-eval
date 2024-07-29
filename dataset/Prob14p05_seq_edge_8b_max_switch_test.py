#=========================================================================
# Prob14p05_seq_edge_8b_max_switch_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

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
    ( "clk",           InputPort (1) ),
    ( "in_",           InputPort (8) ),
    ( "max_switching", OutputPort(1) ),
  ],
  dead_cycles=1,
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_without_max_switching
#-------------------------------------------------------------------------

def test_case_without_max_switching( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0000_0000,
    0b1111_1111,
    0b0000_0000,
    0b0001_0001,
    0b0100_0100,
    0b0010_1001,
    0b0100_0010,
    0b0001_0001,
    0b0100_0010,
  ])

#-------------------------------------------------------------------------
# test_case_with_max_switching
#-------------------------------------------------------------------------

def test_case_with_max_switching( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0000_0000,
    0b0001_0001,
    0b0101_0101,
    0b1010_1010,
    0b1010_1010,
    0b0001_0001,
    0b1010_1010,
    0b0101_0101,
    0b1010_1010,
    0b0000_0000,
    0b0000_0000,
  ])

#-------------------------------------------------------------------------
# test_case_random1
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.sampled_from([ 0b0101_0101, 0b1010_1010 ])))
def test_case_random1( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random2
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random2( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

