#=========================================================================
# Prob07p06_comb_arith_8b_shifter_test
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
    ( "in_", InputPort (8) ),
    ( "amt", InputPort (3) ),
    ( "op",  InputPort (1) ),
    ( "out", OutputPort(8) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_left_shift
#-------------------------------------------------------------------------

def test_case_left_shift( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b0101_1101, 0, 0 ),
    ( 0b0101_1101, 1, 0 ),
    ( 0b0101_1101, 2, 0 ),
    ( 0b0101_1101, 3, 0 ),
    ( 0b0101_1101, 4, 0 ),
    ( 0b0101_1101, 5, 0 ),
    ( 0b0101_1101, 6, 0 ),
    ( 0b0101_1101, 7, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_right_shift
#-------------------------------------------------------------------------

def test_case_right_shift( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b1101_0101, 0, 1 ),
    ( 0b1101_0101, 1, 1 ),
    ( 0b1101_0101, 2, 1 ),
    ( 0b1101_0101, 3, 1 ),
    ( 0b1101_0101, 4, 1 ),
    ( 0b1101_0101, 5, 1 ),
    ( 0b1101_0101, 6, 1 ),
    ( 0b1101_0101, 7, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3), pst.bits(1) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )
