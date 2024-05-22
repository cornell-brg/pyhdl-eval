#=========================================================================
# Prob06p01_comb_codes_enc_4to2_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "in_", InputPort (4) ),
    ( "out", OutputPort(2) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0001,
    0b0010,
    0b0100,
    0b1000,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0000,
    # 0b0001, valid
    # 0b0010, valid
    0b0011,
    # 0b0100, valid
    0b0101,
    0b0110,
    0b0111,

    # 0b1000, valid
    0b1001,
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

