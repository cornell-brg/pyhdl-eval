#=========================================================================
# Prob05p05_comb_mux_4b_1to8_test
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
    ( "in_",  InputPort (4) ),
    ( "sel",  InputPort (3) ),
    ( "out0", OutputPort(4) ),
    ( "out1", OutputPort(4) ),
    ( "out2", OutputPort(4) ),
    ( "out3", OutputPort(4) ),
    ( "out4", OutputPort(4) ),
    ( "out5", OutputPort(4) ),
    ( "out6", OutputPort(4) ),
    ( "out7", OutputPort(4) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    (0,0),
    (1,0),
    (2,0),
    (3,0),
    (4,0),
    (5,0),
    (6,0),
    (7,0),
    (8,0),

    (0,1),
    (1,1),
    (0,2),
    (1,2),
    (0,3),
    (1,3),

    (0,4),
    (1,4),
    (0,5),
    (1,5),
    (0,6),
    (1,6),
    (0,7),
    (1,7),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(4), pst.bits(3) )))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

