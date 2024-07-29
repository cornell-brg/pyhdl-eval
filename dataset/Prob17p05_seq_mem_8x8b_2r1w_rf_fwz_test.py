#=========================================================================
# Prob17p05_seq_mem_8x8b_2r1w_rf_fwz_test
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
# the register file to zero ... except we do not initialize register zero
# since we want to test that it always returns zero.

config = Config(
  ports = [
    ( "clk",         InputPort (1) ),
    ( "read_addr0",  InputPort (3) ),
    ( "read_data0",  OutputPort(8) ),
    ( "read_addr1",  InputPort (3) ),
    ( "read_data1",  OutputPort(8) ),
    ( "write_en",    InputPort (1) ),
    ( "write_addr",  InputPort (3) ),
    ( "write_data",  InputPort (8) ),
  ],
  dead_cycles=7,
  dead_cycle_inputs=[
    (0,0,1,1,0x00),
    (0,0,1,2,0x00),
    (0,0,1,3,0x00),
    (0,0,1,4,0x00),
    (0,0,1,5,0x00),
    (0,0,1,6,0x00),
    (0,0,1,7,0x00),
  ]
)

#-------------------------------------------------------------------------
# test_case_simple
#-------------------------------------------------------------------------

def test_case_simple( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # r0 r1 we wa wd
    ( 1, 1, 1, 1, 0xab ),
    ( 1, 1, 0, 0, 0x00 ),
    ( 1, 1, 1, 2, 0xcd ),
    ( 2, 2, 0, 0, 0x00 ),
    ( 1, 1, 1, 2, 0xef ),
    ( 2, 2, 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_all_reg
#-------------------------------------------------------------------------

def test_case_all_reg( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # r0 r1 we wa wd
    ( 1, 1, 1, 1, 0x23 ),
    ( 1, 1, 1, 2, 0x45 ),
    ( 1, 1, 1, 3, 0x67 ),
    ( 1, 1, 1, 4, 0x89 ),
    ( 1, 1, 1, 5, 0xab ),
    ( 1, 1, 1, 6, 0xcd ),
    ( 1, 1, 1, 7, 0xef ),

    ( 1, 1, 1, 0, 0xff ),
    ( 2, 2, 1, 0, 0xff ),
    ( 3, 3, 1, 0, 0xff ),
    ( 4, 4, 1, 0, 0xff ),
    ( 5, 5, 1, 0, 0xff ),
    ( 6, 6, 1, 0, 0xff ),
    ( 7, 7, 1, 0, 0xff ),
  ])

#-------------------------------------------------------------------------
# test_case_read_ports
#-------------------------------------------------------------------------

def test_case_read_ports( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # r0 r1 we wa wd
    ( 1, 1, 1, 1, 0x23 ),
    ( 1, 1, 1, 2, 0x45 ),
    ( 1, 2, 0, 1, 0x00 ),
    ( 2, 1, 0, 1, 0x00 ),
    ( 1, 1, 1, 3, 0x67 ),
    ( 1, 3, 0, 1, 0x00 ),
    ( 3, 1, 0, 1, 0x00 ),
    ( 1, 1, 1, 4, 0x89 ),
    ( 1, 4, 0, 1, 0x00 ),
    ( 4, 1, 0, 1, 0x00 ),
    ( 1, 1, 1, 5, 0xab ),
    ( 1, 5, 0, 1, 0x00 ),
    ( 5, 1, 0, 1, 0x00 ),
    ( 1, 1, 1, 6, 0xcd ),
    ( 1, 6, 0, 1, 0x00 ),
    ( 6, 1, 0, 1, 0x00 ),
    ( 1, 1, 1, 7, 0xef ),
    ( 1, 7, 0, 1, 0x00 ),
    ( 7, 1, 0, 1, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_forward
#-------------------------------------------------------------------------

def test_case_forward( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # r0 r1 we wa wd
    ( 1, 1, 1, 1, 0x23 ),
    ( 1, 1, 1, 2, 0x45 ),
    ( 1, 1, 1, 3, 0x67 ),
    ( 1, 1, 1, 4, 0x89 ),
    ( 1, 1, 1, 5, 0xab ),
    ( 1, 1, 1, 6, 0xcd ),
    ( 1, 1, 1, 7, 0xef ),

    ( 1, 1, 1, 1, 0x45 ),
    ( 2, 1, 1, 2, 0x67 ),
    ( 3, 1, 1, 3, 0x89 ),
    ( 4, 1, 1, 4, 0xab ),
    ( 5, 1, 1, 5, 0xcd ),
    ( 6, 1, 1, 6, 0xef ),
    ( 7, 1, 1, 7, 0x01 ),

    ( 1, 1, 1, 1, 0x67 ),
    ( 1, 2, 1, 2, 0x89 ),
    ( 1, 3, 1, 3, 0xab ),
    ( 1, 4, 1, 4, 0xcd ),
    ( 1, 5, 1, 5, 0xef ),
    ( 1, 6, 1, 6, 0x01 ),
    ( 1, 7, 1, 7, 0x23 ),

    ( 1, 1, 1, 1, 0x89 ),
    ( 2, 2, 1, 2, 0xab ),
    ( 3, 3, 1, 3, 0xcd ),
    ( 4, 4, 1, 4, 0xef ),
    ( 5, 5, 1, 5, 0x01 ),
    ( 6, 6, 1, 6, 0x23 ),
    ( 7, 7, 1, 7, 0x45 ),
  ])

#-------------------------------------------------------------------------
# test_case_zero
#-------------------------------------------------------------------------

def test_case_zero( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [ # r0 r1 we wa wd
    ( 0, 0, 1, 0, 0x01 ),
    ( 0, 0, 0, 0, 0x00 ),
    ( 0, 0, 1, 0, 0x23 ),
    ( 0, 0, 0, 0, 0x00 ),
    ( 0, 1, 1, 0, 0x45 ),
    ( 0, 1, 0, 0, 0x00 ),
    ( 0, 1, 1, 0, 0x67 ),
    ( 0, 1, 0, 0, 0x00 ),
    ( 1, 0, 1, 0, 0x89 ),
    ( 1, 0, 0, 0, 0x00 ),
    ( 1, 0, 1, 0, 0xab ),
    ( 1, 0, 0, 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(3), # read_addr0
      pst.bits(3), # read_addr1
      pst.bits(1), # write_en
      pst.bits(3), # write_addr
      pst.bits(8), # write_data
    ),
    min_size=30
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

