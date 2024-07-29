#=========================================================================
# Prob07p07_comb_arith_8b_shifter_test
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
    ( "out", OutputPort(8) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b0110_0101, 0 ),
    ( 0b0110_0101, 1 ),
    ( 0b0110_0101, 2 ),
    ( 0b0110_0101, 3 ),
    ( 0b0110_0101, 4 ),
    ( 0b0110_0101, 5 ),
    ( 0b0110_0101, 6 ),
    ( 0b0110_0101, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b1101_0101, 0 ),
    ( 0b1101_0101, 1 ),
    ( 0b1101_0101, 2 ),
    ( 0b1101_0101, 3 ),
    ( 0b1101_0101, 4 ),
    ( 0b1101_0101, 5 ),
    ( 0b1101_0101, 6 ),
    ( 0b1101_0101, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

