#=========================================================================
# Prob17p06_seq_mem_8x8b_1s1w_cam_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim
from pyhdl_eval      import strategies as pst

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------
# Notice how we use the dead cycles to initialize all of the values in
# the register file to zero.

config = Config(
  ports = [
    ( "clk",          InputPort (1) ),
    ( "write_en",     InputPort (1) ),
    ( "write_addr",   InputPort (3) ),
    ( "write_data",   InputPort (8) ),
    ( "search_en",    InputPort (1) ),
    ( "search_data",  InputPort (8) ),
    ( "search_match", OutputPort(8) ),
  ],
  dead_cycles=8,
  dead_cycle_inputs=[
    (1,0,0x00,0,0x00),
    (1,1,0x00,0,0x00),
    (1,2,0x00,0,0x00),
    (1,3,0x00,0,0x00),
    (1,4,0x00,0,0x00),
    (1,5,0x00,0,0x00),
    (1,6,0x00,0,0x00),
    (1,7,0x00,0,0x00),
  ]
)

#-------------------------------------------------------------------------
# test_case_simple
#-------------------------------------------------------------------------

def test_case_simple( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # we wa wd    se sd
    ( 0, 0, 0x00, 0, 0x00 ),
    ( 1, 0, 0xab, 0, 0x00 ),
    ( 0, 0, 0x00, 1, 0xab ),
    ( 1, 1, 0xcd, 0, 0x00 ),
    ( 0, 0, 0x00, 1, 0xcd ),
    ( 1, 1, 0xef, 0, 0x00 ),
    ( 0, 0, 0x00, 1, 0xef ),
    ( 0, 0, 0x00, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_all_reg
#-------------------------------------------------------------------------

def test_case_all_reg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # we wa wd    se sd
    ( 1, 0, 0x01, 0, 0x00 ),
    ( 1, 1, 0x23, 0, 0x00 ),
    ( 1, 2, 0x45, 0, 0x00 ),
    ( 1, 3, 0x67, 0, 0x00 ),
    ( 1, 4, 0x89, 0, 0x00 ),
    ( 1, 5, 0xab, 0, 0x00 ),
    ( 1, 6, 0xcd, 0, 0x00 ),
    ( 1, 7, 0xef, 0, 0x00 ),

    ( 0, 0, 0x00, 1, 0x01 ),
    ( 0, 0, 0x00, 1, 0x23 ),
    ( 0, 0, 0x00, 1, 0x45 ),
    ( 0, 0, 0x00, 1, 0x67 ),
    ( 0, 0, 0x00, 1, 0x89 ),
    ( 0, 0, 0x00, 1, 0xab ),
    ( 0, 0, 0x00, 1, 0xcd ),
    ( 0, 0, 0x00, 1, 0xef ),
  ])

#-------------------------------------------------------------------------
# test_case_multi_match
#-------------------------------------------------------------------------

def test_case_multi_match( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # we wa wd    se sd
    ( 1, 0, 0x01, 0, 0x00 ),
    ( 1, 1, 0x23, 0, 0x00 ),
    ( 1, 2, 0xab, 0, 0x00 ),
    ( 1, 3, 0x23, 0, 0x00 ),
    ( 1, 4, 0x89, 0, 0x00 ),
    ( 1, 5, 0xab, 0, 0x00 ),
    ( 1, 6, 0x23, 0, 0x00 ),
    ( 1, 7, 0xef, 0, 0x00 ),

    ( 0, 0, 0x00, 1, 0x01 ),
    ( 0, 0, 0x00, 1, 0x23 ),
    ( 0, 0, 0x00, 1, 0x89 ),
    ( 0, 0, 0x00, 1, 0xab ),
    ( 0, 0, 0x00, 1, 0xef ),
  ])

#-------------------------------------------------------------------------
# test_case_no_forward
#-------------------------------------------------------------------------

def test_case_no_forward( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # we wa wd    se sd
    ( 1, 0, 0x01, 1, 0x01 ),
    ( 1, 1, 0x23, 1, 0x23 ),
    ( 1, 2, 0x45, 1, 0x45 ),
    ( 1, 3, 0x67, 1, 0x67 ),
    ( 1, 4, 0x89, 1, 0x89 ),
    ( 1, 5, 0xab, 1, 0xab ),
    ( 1, 6, 0xcd, 1, 0xcd ),
    ( 1, 7, 0xef, 1, 0xef ),
  ])

#-------------------------------------------------------------------------
# test_case_random_constrained
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(1),                                 # write_en
      pst.bits(3),                                 # write_addr
      st.sampled_from([ 0x01, 0x23, 0x45, 0x67 ]), # write_data
      pst.bits(1),                                 # search_en
      st.sampled_from([ 0x01, 0x23, 0x45, 0x67 ]), # search_data
    ),
    min_size=30
  ))
def test_case_random_constrained( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(1), # write_en
      pst.bits(3), # write_addr
      pst.bits(8), # write_data
      pst.bits(1), # search_en
      pst.bits(8), # search_data
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

