#=========================================================================
# Prob07p15_comb_arith_8b_alu_test
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
    ( "op",  InputPort (3) ),
    ( "out", OutputPort(8) ),
  ],
  trace_format=TraceFormat.UINT,
)

#-------------------------------------------------------------------------
# test_case_add
#-------------------------------------------------------------------------

def test_case_add( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 0 ),
    (   1,  1, 0 ),
    (   2,  1, 0 ),
    (   1,  2, 0 ),
    (  13,  2, 0 ),
    (  42,  9, 0 ),
    (  42, 13, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_sub
#-------------------------------------------------------------------------

def test_case_sub( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 1 ),
    (   1,  1, 1 ),
    (   2,  1, 1 ),
    (   1,  2, 1 ),
    (  13,  2, 1 ),
    (  42,  9, 1 ),
    (  42, 13, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_srl
#-------------------------------------------------------------------------

def test_case_srl( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 2 ),
    (   1,  1, 2 ),
    (   2,  1, 2 ),
    (   1,  2, 2 ),
    (  13,  2, 2 ),
    (  42,  9, 2 ),
    (  42, 13, 2 ),
  ])

#-------------------------------------------------------------------------
# test_case_sll
#-------------------------------------------------------------------------

def test_case_sll( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 3 ),
    (   1,  1, 3 ),
    (   2,  1, 3 ),
    (   1,  2, 3 ),
    (  13,  2, 3 ),
    (  42,  9, 3 ),
    (  42, 13, 3 ),
])

#-------------------------------------------------------------------------
# test_case_lt
#-------------------------------------------------------------------------

def test_case_lt( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 4 ),
    (   1,  1, 4 ),
    (   2,  1, 4 ),
    (   1,  2, 4 ),
    (  13,  2, 4 ),
    (  42,  9, 4 ),
    (  42, 13, 4 ),
  ])

#-------------------------------------------------------------------------
# test_case_eq
#-------------------------------------------------------------------------

def test_case_eq( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 5 ),
    (   1,  1, 5 ),
    (   2,  1, 5 ),
    (   1,  2, 5 ),
    (  13,  2, 5 ),
    (  42,  9, 5 ),
    (  42, 13, 5 ),
  ])

#-------------------------------------------------------------------------
# test_case_gt
#-------------------------------------------------------------------------

def test_case_gt( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 6 ),
    (   1,  1, 6 ),
    (   2,  1, 6 ),
    (   1,  2, 6 ),
    (  13,  2, 6 ),
    (  42,  9, 6 ),
    (  42, 13, 6 ),
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0, 7 ),
    (   1,  1, 7 ),
    (   2,  1, 7 ),
    (   1,  2, 7 ),
    (  13,  2, 7 ),
    (  42,  9, 7 ),
    (  42, 13, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(3) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

