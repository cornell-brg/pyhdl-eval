#=========================================================================
# Prob09p06_comb_param_dec_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim
from pyhdl_eval.bits import clog2

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

def mk_config( nbits ):
  config = Config(
    parameters = {
      "nbits" : nbits,
    },
    ports = [
      ( "in_", InputPort (clog2(nbits)) ),
      ( "out", OutputPort(nbits)        ),
    ],
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
  [
    0b000,
    0b001,
    0b010,
    0b011,
    0b100,
    0b101,
    0b110,
    0b111,
  ])

#-------------------------------------------------------------------------
# test_case_nbits10_valid
#-------------------------------------------------------------------------

def test_case_nbits10_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10),
  [
    0b0000,
    0b0001,
    0b0010,
    0b0011,
    0b0100,
    0b0101,
    0b0110,
    0b0111,
    0b1000,
    0b1001,
  ])

#-------------------------------------------------------------------------
# test_case_nbits10_invalid
#-------------------------------------------------------------------------

def test_case_nbits10_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10),
  [
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

