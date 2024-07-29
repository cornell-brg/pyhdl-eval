#=========================================================================
# Prob07p13_comb_arith_8b_ucmp_test
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
  trace_format=TraceFormat.UINT,
)

#-------------------------------------------------------------------------
# test_case_lt
#-------------------------------------------------------------------------

def test_case_lt( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,   1 ),
    (   1,   2 ),
    (   3,   9 ),
    (  13,  42 ),

    ( 127, 128 ),
    ( 150, 200 ),
    ( 250, 255 ),
    ( 254, 255 ),
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
# test_case_gt
#-------------------------------------------------------------------------

def test_case_gt( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   1,   0 ),
    (   2,   1 ),
    (   9,   3 ),
    (  42,  13 ),

    ( 128, 127 ),
    ( 200, 150 ),
    ( 255, 250 ),
    ( 255, 254 ),
  ])


#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

