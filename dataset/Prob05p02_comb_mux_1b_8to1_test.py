#=========================================================================
# Prob05p02_comb_mux_1b_8to1_test
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
    ( "in0", InputPort (1) ),
    ( "in1", InputPort (1) ),
    ( "in2", InputPort (1) ),
    ( "in3", InputPort (1) ),
    ( "in4", InputPort (1) ),
    ( "in5", InputPort (1) ),
    ( "in6", InputPort (1) ),
    ( "in7", InputPort (1) ),
    ( "sel", InputPort (3) ),
    ( "out", OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (0,0,0,0,0,0,0,0,0),
    (1,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,1),
    (0,1,0,0,0,0,0,0,1),
    (0,0,0,0,0,0,0,0,2),
    (0,0,1,0,0,0,0,0,2),
    (0,0,0,0,0,0,0,0,3),
    (0,0,0,1,0,0,0,0,3),

    (0,0,0,0,0,0,0,0,4),
    (0,0,0,0,1,0,0,0,4),
    (0,0,0,0,0,0,0,0,5),
    (0,0,0,0,0,1,0,0,5),
    (0,0,0,0,0,0,0,0,6),
    (0,0,0,0,0,0,1,0,6),
    (0,0,0,0,0,0,0,0,7),
    (0,0,0,0,0,0,0,1,7),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples( pst.bits(1), pst.bits(1), pst.bits(1), pst.bits(1),
               pst.bits(1), pst.bits(1), pst.bits(1), pst.bits(1),
               pst.bits(3) )
    ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

