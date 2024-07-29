#=========================================================================
# Prob09p08_comb_param_rotator_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort, TraceFormat
from pyhdl_eval.core import run_sim
from pyhdl_eval.bits import clog2
from pyhdl_eval      import strategies as pst

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

def mk_config( nbits ):
  config = Config(
    parameters = {
      "nbits" : nbits,
    },
    ports = [
      ( "in_", InputPort (nbits)        ),
      ( "amt", InputPort (clog2(nbits)) ),
      ( "op",  InputPort (1)            ),
      ( "out", OutputPort(nbits)        ),
    ],
    trace_format=TraceFormat.BIN,
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits4_left_rotate
#-------------------------------------------------------------------------

def test_case_nbits4_left_rotate( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=4),
  [
    ( 0b1101, 0, 0 ),
    ( 0b1101, 1, 0 ),
    ( 0b1101, 2, 0 ),
    ( 0b1101, 3, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_nbits4_right_rotate
#-------------------------------------------------------------------------

def test_case_nbits4_right_rotate( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=4),
  [
    ( 0b1101, 0, 1 ),
    ( 0b1101, 1, 1 ),
    ( 0b1101, 2, 1 ),
    ( 0b1101, 3, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_nbits4_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(4), pst.bits(2), pst.bits(1) ) ))
def test_case_nbits4_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=4), test_vectors )

#-------------------------------------------------------------------------
# test_case_nbits8_left_rotate
#-------------------------------------------------------------------------

def test_case_nbits8_left_rotate( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
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
# test_case_nbits8_right_rotate
#-------------------------------------------------------------------------

def test_case_nbits8_right_rotate( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
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
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(3), pst.bits(1) ) ))
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8), test_vectors )

