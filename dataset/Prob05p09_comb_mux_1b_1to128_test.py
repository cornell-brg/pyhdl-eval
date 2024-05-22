#=========================================================================
# Prob05p09_comb_mux_1b_1to128_test
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
    ( "in_", InputPort (  1) ),
    ( "sel", InputPort (  7) ),
    ( "out", OutputPort(128) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0,   0 ),
    ( 1,   0 ),
    ( 0,   1 ),
    ( 1,   1 ),
    ( 0,   2 ),
    ( 1,   2 ),
    ( 0,   3 ),
    ( 1,   3 ),

    ( 0,  15 ),
    ( 1,  15 ),
    ( 0, 100 ),
    ( 1, 100 ),
    ( 0, 127 ),
    ( 1, 127 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(7) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

