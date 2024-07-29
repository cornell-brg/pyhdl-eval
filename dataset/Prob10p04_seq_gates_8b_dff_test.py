#=========================================================================
# Prob10p04_seq_gates_8b_dff_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

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
    ( "clk", InputPort (1) ),
    ( "d",   InputPort (8) ),
    ( "q",   OutputPort(8) ),
  ],
  dead_cycles=1,
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0x00,
    0x00, # prev: 0 -> 0 0
    0x01, # prev: 0 -> 1 0
    0x01, # prev: 1 -> 1 1
    0x00, # prev: 1 -> 0 1
    0x00,
    0x00,
    0xab,
    0xcd,
    0xef,
    0x00,
    0x00,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

