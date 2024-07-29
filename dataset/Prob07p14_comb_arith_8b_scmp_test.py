#=========================================================================
# Prob07p14_comb_arith_8b_scmp_test
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
    ( "in0", InputPort (8) ),
    ( "in1", InputPort (8) ),
    ( "lt",  OutputPort(1) ),
    ( "eq",  OutputPort(1) ),
    ( "gt",  OutputPort(1) ),
  ],
  trace_format=TraceFormat.INT,
)

#-------------------------------------------------------------------------
# test_case_lt_pos
#-------------------------------------------------------------------------

def test_case_lt_pos( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,   1 ),
    (   1,   2 ),
    (   3,   9 ),
    (  13,  42 ),
  ])

#-------------------------------------------------------------------------
# test_case_lt_neg
#-------------------------------------------------------------------------

def test_case_lt_neg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   -1,    0 ),
    (   -1,    1 ),
    (   -1,    2 ),
    ( -128,    0 ),
    ( -128,    1 ),
    ( -128,    2 ),

    (   -5,    0 ),
    (   -5,   -1 ),
    (   -5,   -2 ),
    ( -128, -100 ),
    ( -128, -127 ),
  ])

#-------------------------------------------------------------------------
# test_case_eq
#-------------------------------------------------------------------------

def test_case_eq( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,   0 ),
    (  16,  16 ),
    (  32,  32 ),
    ( 100, 100 ),
    ( 128, 128 ),
    ( 255, 255 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt_pos
#-------------------------------------------------------------------------

def test_case_gt_pos( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   1,   0 ),
    (   2,   1 ),
    (   9,   3 ),
    (  42,  13 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt_neg
#-------------------------------------------------------------------------

def test_case_gt_neg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (    0,   -1 ),
    (    1,   -1 ),
    (    2,   -1 ),
    (    0, -128 ),
    (    1, -128 ),
    (    2, -128 ),

    (    0,   -5 ),
    (   -1,   -5 ),
    (   -2,   -5 ),
    ( -100, -128 ),
    ( -127, -128 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

