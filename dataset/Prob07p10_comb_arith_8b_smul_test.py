#=========================================================================
# Prob07p10_comb_arith_8b_smul_test
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
    ( "in0", InputPort ( 8) ),
    ( "in1", InputPort ( 8) ),
    ( "out", OutputPort(16) ),
  ],
  trace_format=TraceFormat.INT,
)

#-------------------------------------------------------------------------
# test_case_pos_small
#-------------------------------------------------------------------------

def test_case_pos_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0 ),
    (   0,  1 ),
    (   1,  0 ),
    (   2,  2 ),
    (   2,  3 ),
    (   8,  9 ),
    (  12, 13 ),
  ])

#-------------------------------------------------------------------------
# test_case_pos_large
#-------------------------------------------------------------------------

def test_case_pos_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  16,  16 ),
    (  20,  16 ),
    (  42,  90 ),
    ( 100,  99 ),
    ( 127, 127 ),
  ])

#-------------------------------------------------------------------------
# test_case_neg_small
#-------------------------------------------------------------------------

def test_case_neg_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  -1 ),
    (  -1,   0 ),
    (  -2,   2 ),
    (   2,  -2 ),
    (  -2,  -2 ),
    (  -8,   9 ),
    (   8,  -9 ),
    ( -12, -13 ),
  ])

#-------------------------------------------------------------------------
# test_case_neg_large
#-------------------------------------------------------------------------

def test_case_neg_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  -16,  -16 ),
    (   20,  -16 ),
    (  -20,   16 ),
    (  -20,  -16 ),
    (  -42,   90 ),
    (  100,  -99 ),
    ( -128, -128 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

