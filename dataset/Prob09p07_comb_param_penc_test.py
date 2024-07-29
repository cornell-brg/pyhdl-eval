#=========================================================================
# Prob09p07_comb_param_penc_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
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
      ( "out", OutputPort(clog2(nbits)) ),
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
    0b0000_0011,

    0b0000_0100,
    0b0000_0101,
    0b0000_0110,
    0b0000_0111,

    0b0000_1000,
    0b0000_1001,
    0b0000_1010,
    0b0000_1011,

    0b0000_1100,
    0b0000_1101,
    0b0000_1110,
    0b0000_1111,

    0b0000_0000,
    0b0001_0000,
    0b0010_0000,
    0b0011_0000,

    0b0100_0000,
    0b0101_0000,
    0b0110_0000,
    0b0111_0000,

    0b1000_0000,
    0b1001_0000,
    0b1010_0000,
    0b1011_0000,

    0b1100_0000,
    0b1101_0000,
    0b1110_0000,
    0b1111_0000,
  ])

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8), test_vectors )

#-------------------------------------------------------------------------
# test_case_nbits10_directed
#-------------------------------------------------------------------------

def test_case_nbits10_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10),
  [
    0b00_0000_0000,
    0b00_0000_0001,
    0b00_0000_0010,
    0b00_0000_0011,

    0b00_0000_0100,
    0b00_0000_0101,
    0b00_0000_0110,
    0b00_0000_0111,

    0b00_0000_1000,
    0b00_0000_1001,
    0b00_0000_1010,
    0b00_0000_1011,

    0b00_0000_1100,
    0b00_0000_1101,
    0b00_0000_1110,
    0b00_0000_1111,

    0b00_0000_0000,
    0b00_0001_0000,
    0b00_0010_0000,
    0b00_0011_0000,

    0b00_0100_0000,
    0b00_0101_0000,
    0b00_0110_0000,
    0b00_0111_0000,

    0b00_1000_0000,
    0b00_1001_0000,
    0b00_1010_0000,
    0b00_1011_0000,

    0b00_1100_0000,
    0b00_1101_0000,
    0b00_1110_0000,
    0b00_1111_0000,

    0b00_0000_0000,
    0b01_0000_0000,
    0b10_0000_0000,
    0b11_0000_0000,
  ])

#-------------------------------------------------------------------------
# test_case_nbits10_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(10) ))
def test_case_nbits10_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10), test_vectors )

