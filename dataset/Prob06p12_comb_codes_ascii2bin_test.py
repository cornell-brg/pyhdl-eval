#=========================================================================
# Prob06p12_comb_codes_ascii2bin_test
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
    ( "in_", InputPort (16) ),
    ( "out", OutputPort( 4) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0x3030,
    0x3031,
    0x3032,
    0x3033,

    0x3034,
    0x3035,
    0x3036,
    0x3037,

    0x3038,
    0x3039,
    0x3130,
    0x3131,

    0x3132,
    0x3133,
    0x3134,
    0x3135,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0x0000,
    0x0001,
    0x0002,
    0x0003,
    0x0004,
    0x0005,
    0x0006,
    0x0007,
    0x0008,
    0x0009,
    0x0010,

    0x1010,
    0x2020,
    0x4040,
    0x5050,
    0x6060,
    0x7070,
    0x8080,
    0x9090,
    0xa0a0,
    0xb0b0,
    0xc0c0,
    0xd0d0,
    0xe0e0,
    0xf0f0,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( pst.bits(16) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

