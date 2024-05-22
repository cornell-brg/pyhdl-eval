#=========================================================================
# Prob05p04_comb_mux_4b_8to1_test
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
    ( "in0", InputPort (4) ),
    ( "in1", InputPort (4) ),
    ( "in2", InputPort (4) ),
    ( "in3", InputPort (4) ),
    ( "in4", InputPort (4) ),
    ( "in5", InputPort (4) ),
    ( "in6", InputPort (4) ),
    ( "in7", InputPort (4) ),
    ( "sel", InputPort (3) ),
    ( "out", OutputPort(4) ),
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

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples( pst.bits(4), pst.bits(4), pst.bits(4), pst.bits(4),
               pst.bits(4), pst.bits(4), pst.bits(4), pst.bits(4),
               pst.bits(3) )
    ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

