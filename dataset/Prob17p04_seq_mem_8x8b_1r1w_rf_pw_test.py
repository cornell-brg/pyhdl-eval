#=========================================================================
# Prob17p04_seq_mem_8x8b_1r1w_rf_pw_test
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
    ( "clk",             InputPort (1) ),
    ( "read_addr",       InputPort (3) ),
    ( "read_data",       OutputPort(8) ),
    ( "write_nibble_en", InputPort (2) ),
    ( "write_addr",      InputPort (3) ),
    ( "write_data",      InputPort (8) ),
  ],
  dead_cycles=8,
  dead_cycle_inputs=[
    (0,0b11,0,0x00),
    (0,0b11,1,0x00),
    (0,0b11,2,0x00),
    (0,0b11,3,0x00),
    (0,0b11,4,0x00),
    (0,0b11,5,0x00),
    (0,0b11,6,0x00),
    (0,0b11,7,0x00),
  ]
)

#-------------------------------------------------------------------------
# test_case_simple
#-------------------------------------------------------------------------

def test_case_simple( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we    wa wd
    ( 0, 0b00, 0, 0x00 ),
    ( 0, 0b11, 0, 0xab ),
    ( 0, 0b00, 0, 0x00 ),
    ( 0, 0b11, 1, 0xcd ),
    ( 1, 0b00, 0, 0x00 ),
    ( 0, 0b11, 1, 0xef ),
    ( 1, 0b00, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_all_reg
#-------------------------------------------------------------------------

def test_case_all_reg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we    wa wd
    ( 0, 0b11, 0, 0x01 ),
    ( 0, 0b11, 1, 0x23 ),
    ( 0, 0b11, 2, 0x45 ),
    ( 0, 0b11, 3, 0x67 ),
    ( 0, 0b11, 4, 0x89 ),
    ( 0, 0b11, 5, 0xab ),
    ( 0, 0b11, 6, 0xcd ),
    ( 0, 0b11, 7, 0xef ),

    ( 0, 0b00, 0, 0xff ),
    ( 1, 0b00, 0, 0xff ),
    ( 2, 0b00, 0, 0xff ),
    ( 3, 0b00, 0, 0xff ),
    ( 4, 0b00, 0, 0xff ),
    ( 5, 0b00, 0, 0xff ),
    ( 6, 0b00, 0, 0xff ),
    ( 7, 0b00, 0, 0xff ),
  ])

#-------------------------------------------------------------------------
# test_case_partial_write
#-------------------------------------------------------------------------

def test_case_partial_write( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # ra we    wa wd
    ( 0, 0b11, 0, 0xff ),
    ( 0, 0b01, 0, 0xab ),
    ( 0, 0b00, 0, 0x00 ),
    ( 0, 0b10, 0, 0xab ),
    ( 0, 0b00, 0, 0x00 ),

    ( 1, 0b11, 1, 0xff ),
    ( 1, 0b01, 1, 0xab ),
    ( 1, 0b00, 1, 0x00 ),
    ( 1, 0b10, 1, 0xab ),
    ( 1, 0b00, 1, 0x00 ),

    ( 2, 0b11, 2, 0xff ),
    ( 2, 0b01, 2, 0xab ),
    ( 2, 0b00, 2, 0x00 ),
    ( 2, 0b10, 2, 0xab ),
    ( 2, 0b00, 2, 0x00 ),

    ( 3, 0b11, 3, 0xff ),
    ( 3, 0b01, 3, 0xab ),
    ( 3, 0b00, 3, 0x00 ),
    ( 3, 0b10, 3, 0xab ),
    ( 3, 0b00, 3, 0x00 ),

    ( 4, 0b11, 4, 0xff ),
    ( 4, 0b01, 4, 0xab ),
    ( 4, 0b00, 4, 0x00 ),
    ( 4, 0b10, 4, 0xab ),
    ( 4, 0b00, 4, 0x00 ),

    ( 5, 0b11, 5, 0xff ),
    ( 5, 0b01, 5, 0xab ),
    ( 5, 0b00, 5, 0x00 ),
    ( 5, 0b10, 5, 0xab ),
    ( 5, 0b00, 5, 0x00 ),

    ( 6, 0b11, 6, 0xff ),
    ( 6, 0b01, 6, 0xab ),
    ( 6, 0b00, 6, 0x00 ),
    ( 6, 0b10, 6, 0xab ),
    ( 6, 0b00, 6, 0x00 ),

    ( 7, 0b11, 7, 0xff ),
    ( 7, 0b01, 7, 0xab ),
    ( 7, 0b00, 7, 0x00 ),
    ( 7, 0b10, 7, 0xab ),
    ( 7, 0b00, 7, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(3), # read_addr
      pst.bits(2), # write_nibble_en
      pst.bits(3), # write_addr
      pst.bits(8), # write_data
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )
