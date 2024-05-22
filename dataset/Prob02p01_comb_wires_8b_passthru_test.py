#=========================================================================
# Prob02p01_comb_wires_8b_passthru_test
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
    ( "out", OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
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
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists(pst.bits(8)) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

