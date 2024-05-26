#=========================================================================
# Prob07p10_comb_arith_8b_umul_test
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
    ( "in2", InputPort (16) ),
    ( "out", OutputPort(16) ),
  ],
  trace_format=TraceFormat.UINT,
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0,  0 ),
    (   0,  1,  0 ),
    (   1,  0,  0 ),
    (   2,  2,  0 ),
    (   2,  3,  0 ),
    (   8,  9,  0 ),
    (  12, 13,  0 ),

    (   0,  0,  1 ),
    (   0,  1,  1 ),
    (   1,  0,  1 ),
    (   2,  2,  1 ),
    (   2,  3,  1 ),
    (   8,  9,  1 ),
    (  12, 13,  1 ),

    (   0,  0,  2 ),
    (   0,  1,  2 ),
    (   1,  0,  2 ),
    (   2,  2,  2 ),
    (   2,  3,  2 ),
    (   8,  9,  2 ),
    (  12, 13,  2 ),
])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  16,  16,     0 ),
    (  20,  16,     0 ),
    (  42,  90,     0 ),
    ( 130, 100,     0 ),
    ( 255, 255,     0 ),
    ( 255, 255,    10 ),

    (  16,  16,   255 ),
    (  20,  16,   255 ),
    (  42,  90,   255 ),
    ( 130, 100,   255 ),
    ( 250, 250,   255 ),

    (  16,  16, 10000 ),
    (  20,  16, 10000 ),
    (  42,  90, 10000 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 255, 255, 1     ),
    ( 255, 255, 255   ),
    ( 255, 255, 10000 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(16) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )
