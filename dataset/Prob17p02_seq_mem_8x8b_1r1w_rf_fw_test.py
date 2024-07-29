#=========================================================================
# Prob17p02_seq_mem_8x8b_1r1w_rf_fw_test
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
    ( "clk",         InputPort (1) ),
    ( "read_addr",   InputPort (3) ),
    ( "read_data",   OutputPort(8) ),
    ( "write_en",    InputPort (1) ),
    ( "write_addr",  InputPort (3) ),
    ( "write_data",  InputPort (8) ),
  ],
  dead_cycles=8,
  dead_cycle_inputs=[
    (0,1,0,0x00),
    (0,1,1,0x00),
    (0,1,2,0x00),
    (0,1,3,0x00),
    (0,1,4,0x00),
    (0,1,5,0x00),
    (0,1,6,0x00),
    (0,1,7,0x00),
  ]
)

#-------------------------------------------------------------------------
# test_case_simple
#-------------------------------------------------------------------------

def test_case_simple( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we wa wd
    ( 0, 0, 0, 0x00 ),
    ( 0, 1, 0, 0xab ),
    ( 0, 0, 0, 0x00 ),
    ( 0, 1, 1, 0xcd ),
    ( 1, 0, 0, 0x00 ),
    ( 0, 1, 1, 0xef ),
    ( 1, 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_all_reg
#-------------------------------------------------------------------------

def test_case_all_reg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we wa wd
    ( 0, 1, 0, 0x01 ),
    ( 0, 1, 1, 0x23 ),
    ( 0, 1, 2, 0x45 ),
    ( 0, 1, 3, 0x67 ),
    ( 0, 1, 4, 0x89 ),
    ( 0, 1, 5, 0xab ),
    ( 0, 1, 6, 0xcd ),
    ( 0, 1, 7, 0xef ),

    ( 0, 1, 0, 0xff ),
    ( 1, 1, 0, 0xff ),
    ( 2, 1, 0, 0xff ),
    ( 3, 1, 0, 0xff ),
    ( 4, 1, 0, 0xff ),
    ( 5, 1, 0, 0xff ),
    ( 6, 1, 0, 0xff ),
    ( 7, 1, 0, 0xff ),
  ])

#-------------------------------------------------------------------------
# test_case_forward
#-------------------------------------------------------------------------

def test_case_forward( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we wa wd
    ( 0, 1, 0, 0x01 ),
    ( 0, 1, 1, 0x23 ),
    ( 0, 1, 2, 0x45 ),
    ( 0, 1, 3, 0x67 ),
    ( 0, 1, 4, 0x89 ),
    ( 0, 1, 5, 0xab ),
    ( 0, 1, 6, 0xcd ),
    ( 0, 1, 7, 0xef ),

    ( 0, 0, 0, 0x23 ),
    ( 1, 0, 1, 0x45 ),
    ( 2, 0, 2, 0x67 ),
    ( 3, 0, 3, 0x89 ),
    ( 4, 0, 4, 0xab ),
    ( 5, 0, 5, 0xcd ),
    ( 6, 0, 6, 0xef ),
    ( 7, 0, 7, 0x01 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(3), # read_addr
      pst.bits(1), # write_en
      pst.bits(3), # write_addr
      pst.bits(8), # write_data
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

