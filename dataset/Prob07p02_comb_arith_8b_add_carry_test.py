#=========================================================================
# Prob07p02_comb_arith_8b_add_carry_test
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
    ( "in0",  InputPort (8) ),
    ( "in1",  InputPort (8) ),
    ( "cin",  InputPort (1) ),
    ( "out",  OutputPort(8) ),
    ( "cout", OutputPort(1) ),
  ],
  trace_format=TraceFormat.INT,
)

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 0 ),
    (   0,  1, 0 ),
    (   1,  0, 0 ),
    (  42, 13, 0 ),
    (  13, 42, 0 ),
    ( 100, 27, 0 ),

    (   0,  0, 1 ),
    (   0,  1, 1 ),
    (   1,  0, 1 ),
    (  42, 13, 1 ),
    (  13, 42, 1 ),
    ( 100, 26, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (    0,  -1, 0 ),
    (   -1,   0, 0 ),
    (   42, -13, 0 ),
    (  -42,  13, 0 ),
    (  -42, -13, 0 ),
    ( -128, 127, 0 ),

    (    0,  -1, 1 ),
    (   -1,   0, 1 ),
    (   42, -13, 1 ),
    (  -42,  13, 1 ),
    (  -42, -13, 1 ),
    ( -128, 127, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  127,   1, 0 ),
    (  126,   2, 0 ),
    (  120,  13, 0 ),
    ( -128,  -1, 0 ),
    ( -127,  -2, 0 ),
    ( -120, -13, 0 ),

    (  127,   0, 1 ),
    (  126,   1, 1 ),
    (  120,  12, 1 ),
    ( -128,  -2, 1 ),
    ( -127,  -3, 1 ),
    ( -120, -14, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(1) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

