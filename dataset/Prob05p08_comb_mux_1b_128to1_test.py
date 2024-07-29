#=========================================================================
# Prob05p08_comb_mux_1b_128to1_test
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
    ( "in_", InputPort (128) ),
    ( "sel", InputPort (  7) ),
    ( "out", OutputPort(  1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0,         0 ),
    ( 0b0001,    0 ),
    ( 0,         1 ),
    ( 0b0010,    1 ),
    ( 0,         2 ),
    ( 0b0100,    2 ),
    ( 0,         3 ),
    ( 0b1000,    3 ),

    ( 0,        15 ),
    ( 1 << 15,  15 ),
    ( 0,       100 ),
    ( 1 << 100,100 ),
    ( 0,       127 ),
    ( 1 << 127,127 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(128), pst.bits(7) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

