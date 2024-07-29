#=========================================================================
# Prob19p08_seq_pipe_minmax4_2stage_test
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
    ( "in0", InputPort (8) ),
    ( "in1", InputPort (8) ),
    ( "in2", InputPort (8) ),
    ( "in3", InputPort (8) ),
    ( "min", OutputPort(8) ),
    ( "max", OutputPort(8) ),
  ],
  dead_cycles=2,
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 1, 2, 3, 4 ),
    ( 4, 3, 2, 1 ),
    ( 3, 4, 1, 2 ),
    ( 1, 4, 3, 2 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_dups
#-------------------------------------------------------------------------

def test_case_dups( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0, 0, 0 ),
    ( 9, 9, 9, 9 ),
    ( 1, 1, 2, 2 ),
    ( 2, 2, 1, 1 ),
    ( 2, 1, 2, 1 ),
    ( 1, 1, 2, 1 ),
    ( 1, 2, 2, 2 ),
    ( 2, 2, 1, 2 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
    ( 0, 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 101, 102, 103, 104 ),
    ( 104, 103, 102, 101 ),
    ( 103, 104, 101, 102 ),
    ( 101, 104, 103, 102 ),
    ( 255, 254, 252, 253 ),
    ( 252, 253, 254, 255 ),
    ( 253, 252, 255, 254 ),
    ( 255, 252, 253, 254 ),
    (   0,   0,   0,   0 ),
    (   0,   0,   0,   0 ),
    (   0,   0,   0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x01, 0x02, 0x03, 0x04 ),
    ( 0x04, 0x05, 0x03, 0x02 ),
    ( 0x06, 0x03, 0x04, 0x05 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(8), pst.bits(8), pst.bits(8), pst.bits(8)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

