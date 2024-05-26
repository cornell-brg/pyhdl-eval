#=========================================================================
# Prob09p05_comb_param_enc_test
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
# test_case_nbit8_valid
#-------------------------------------------------------------------------

def test_case_nbits8_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
  [
    0b0000_0001,
    0b0000_0010,
    0b0000_0100,
    0b0000_1000,
    0b0001_0000,
    0b0010_0000,
    0b0100_0000,
    0b1100_0000,
  ])

#-------------------------------------------------------------------------
# test_case_nbits8_invalid
#-------------------------------------------------------------------------

def test_case_nbits8_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8),
  [
    0b0000_0000,
    0b0001_0001,
    0b0010_0010,
    0b0100_0100,
    0b1000_1000,
    0b1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_nbits8_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_nbits6_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8), test_vectors )

#-------------------------------------------------------------------------
# test_case_nbits10_valid
#-------------------------------------------------------------------------

def test_case_nbits10_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10),
  [
    0b00_0000_0001,
    0b00_0000_0010,
    0b00_0000_0100,
    0b00_0000_1000,

    0b00_0001_0000,
    0b00_0010_0000,
    0b00_0100_0000,
    0b00_1000_0000,

    0b01_0000_0000,
    0b10_0000_0000,
  ])

#-------------------------------------------------------------------------
# test_case_nbits10_invalid
#-------------------------------------------------------------------------

def test_case_nbits10_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10),
  [
    0b00_0000_0000,
    0b00_0001_0001,
    0b00_0010_0010,
    0b00_0100_0100,

    0b00_1000_1000,
    0b01_0001_0000,
    0b10_0010_0000,
    0b11_1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_nbits10_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(10) ))
def test_case_nbits10_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=10), test_vectors )
