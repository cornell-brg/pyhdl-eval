#=========================================================================
# Prob19p06_seq_pipe_add3_2stage_test
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
    ( "clk",   InputPort (1) ),
    ( "in0",   InputPort (8) ),
    ( "in1",   InputPort (8) ),
    ( "in2",   InputPort (8) ),
    ( "out01", OutputPort(8) ),
    ( "out",   OutputPort(8) ),
  ],
  dead_cycles=2,
  trace_format=TraceFormat.INT,
)

#-------------------------------------------------------------------------
# test_case_input2
#-------------------------------------------------------------------------

def test_case_input2( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (    0,    0,   0 ),

    (    0,    1,   0 ),
    (    1,    0,   0 ),
    (   42,   13,   0 ),
    (   13,   42,   0 ),
    (  100,   27,   0 ),

    (    0,   -1,   0 ),
    (   -1,    0,   0 ),
    (   -1,    0,   0 ),
    (   42,  -13,   0 ),
    (  -42,   13,   0 ),
    (  -42,  -13,   0 ),
    ( -128,  127,   0 ),

    (    0,    0,   1 ),
    (    0,    1,   0 ),
    (    0,   42,  13 ),
    (    0,   13,  42 ),
    (    0,  100,  27 ),

    (    0,    0,  -1 ),
    (    0,   -1,   0 ),
    (    0,   -1,   0 ),
    (    0,   42, -13 ),
    (    0,  -42,  13 ),
    (    0,  -42, -13 ),
    (    0, -128, 127 ),

    (    0,    0,   1 ),
    (    1,    0,   0 ),
    (   42,    0,  13 ),
    (   13,    0,  42 ),
    (  100,    0,  27 ),

    (    0,    0,  -1 ),
    (   -1,    0,   0 ),
    (   -1,    0,   0 ),
    (   42,    0, -13 ),
    (  -42,    0,  13 ),
    (  -42,    0, -13 ),
    ( -128,    0, 127 ),

    (    0,    0,   0 ),
    (    0,    0,   0 ),
    (    0,    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_input3
#-------------------------------------------------------------------------

def test_case_input3( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0, 0 ),
    ( 1, 1, 1 ),
    ( 1, 2, 3 ),
    ( 3, 1, 2 ),
    ( 2, 3, 1 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  127,    1,    0 ),
    (    0,  127,    1 ),
    (    1,    0,  127 ),
    ( -128,   -1,    0 ),
    (    0, -128,   -1 ),
    (   -1,    0, -128 ),
    (   64,   64,   64 ),
    (  -64,  -64,  -64 ),
    (  128,  128,  128 ),
    (    0,    0,    0 ),
    (    0,    0,    0 ),
    (    0,    0,    0 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x01, 0x02, 0x04 ),
    ( 0x02, 0x03, 0x04 ),
    ( 0x03, 0x04, 0x05 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
    ( 0x00, 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

