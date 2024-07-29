#=========================================================================
# Prob09p02_comb_param_bit_rev_test
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

def mk_config( nbits ):
  config = Config(
    parameters = {
      "nbits" : nbits,
    },
    ports = [
      ( "in_", InputPort (nbits) ),
      ( "out", OutputPort(nbits) ),
    ],
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
  [
    0b0000_0000,
    0b0000_0001,
    0b0000_0010,
    0b0000_0100,
    0b0000_0100,
    0b0001_0001,
    0b0010_0010,
    0b0100_0100,
    0b1000_1000,
    0b1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists(pst.bits(8)) )
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8), test_vectors )

#-------------------------------------------------------------------------
# test_case_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=13),
  [
    0b0_0000_0000_0000,
    0b0_0000_0000_0001,
    0b0_0000_0000_0010,
    0b0_0000_0000_0100,
    0b0_0000_0000_1000,
    0b0_0000_0001_0001,
    0b0_0000_0010_0010,
    0b0_0000_0100_0100,
    0b0_0000_1000_1000,
    0b0_0001_0001_0001,
    0b0_0010_0010_0010,
    0b0_0100_0100_0100,
    0b0_1000_1000_1000,
    0b1_0001_0001_0001,
    0b1_0101_0101_0101,
    0b0_1010_1010_1010,
    0b1_1111_1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_nbits13_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists(pst.bits(13)) )
def test_case_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=13), test_vectors )

