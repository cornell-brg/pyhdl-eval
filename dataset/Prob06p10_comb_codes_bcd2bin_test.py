#=========================================================================
# Prob06p10_comb_codes_bcd2bin_test
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

config = Config(
  ports = [
    ( "in_", InputPort (8) ),
    ( "out", OutputPort(4) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
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
    0b0001_0000,
    0b0001_0001,

    0b0001_0010,
    0b0001_0011,
    0b0001_0100,
    0b0001_0101,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0b0000_1010,
    0b0000_1011,
    0b0000_1100,
    0b0000_1101,
    0b0000_1110,
    0b0000_1111,

    0b0001_0000,
    0b0001_0001,
    0b0001_0010,
    0b0001_0011,

    0b0001_0100,
    0b0001_0101,
    0b0001_0110,
    0b0001_0111,

    0b0001_1000,
    0b0001_1001,
    0b0001_1010,
    0b0001_1011,

    0b0001_1100,
    0b0001_1101,
    0b0001_1110,
    0b0001_1111,

    0b0010_0000,
    0b0010_0001,
    0b0010_0010,
    0b0010_0011,

    0b0010_0100,
    0b0010_0101,
    0b0010_0110,
    0b0010_0111,

    0b0010_1000,
    0b0010_1001,
    0b0010_1010,
    0b0010_1011,

    0b0010_1100,
    0b0010_1101,
    0b0010_1110,
    0b0010_1111,

    0b0100_1111,
    0b1000_1111,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(8) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

