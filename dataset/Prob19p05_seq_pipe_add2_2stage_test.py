#=========================================================================
# Prob19p05_seq_pipe_add2_2stage_test
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
    ( "clk",     InputPort (1) ),
    ( "in0",     InputPort (8) ),
    ( "in1",     InputPort (8) ),
    ( "out_lsn", OutputPort(4) ),
    ( "out",     OutputPort(8) ),
  ],
  dead_cycles=1,
  trace_format=TraceFormat.INT,
)

#-------------------------------------------------------------------------
# test_case_positive
#-------------------------------------------------------------------------

def test_case_positive( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (   0,  0 ),
    (   0,  1 ),
    (   1,  0 ),
    (  42, 13 ),
    (  13, 42 ),
    ( 100, 27 ),
    (   0,  0 ),
    (   0,  0 ),
    (   0,  0 ),
  ])

#-------------------------------------------------------------------------
# test_case_negative
#-------------------------------------------------------------------------

def test_case_negative( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (    0,  -1 ),
    (   -1,   0 ),
    (   42, -13 ),
    (  -42,  13 ),
    (  -42, -13 ),
    ( -128, 127 ),
    (    0,   0 ),
    (    0,   0 ),
    (    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (  127,   1 ),
    (  126,   2 ),
    (  120,  13 ),
    ( -128,  -1 ),
    ( -127,  -2 ),
    ( -120, -13 ),
    (    0,   0 ),
    (    0,   0 ),
    (    0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_mid_carry
#-------------------------------------------------------------------------

def test_case_mid_carry( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x00, 0x00 ),
    ( 0x08, 0x08 ),
    ( 0x0c, 0x0c ),
    ( 0x0d, 0x0d ),
    ( 0x18, 0x18 ),
    ( 0x1c, 0x1c ),
    ( 0x1d, 0x1d ),
    ( 0x38, 0x38 ),
    ( 0x3c, 0x3c ),
    ( 0x3d, 0x3d ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_example
#-------------------------------------------------------------------------

def test_case_example( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x00, 0x00 ),
    ( 0x01, 0x01 ),
    ( 0x02, 0x03 ),
    ( 0x03, 0x04 ),
    ( 0x11, 0x11 ),
    ( 0x12, 0x13 ),
    ( 0x13, 0x14 ),
    ( 0x09, 0x09 ),
    ( 0x19, 0x19 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
    ( 0x00, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

