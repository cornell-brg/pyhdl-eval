#=========================================================================
# Prob02p07_comb_wires_5x3b_to_4x4b_test
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
    ( "in0",  InputPort (3) ),
    ( "in1",  InputPort (3) ),
    ( "in2",  InputPort (3) ),
    ( "in3",  InputPort (3) ),
    ( "in4",  InputPort (3) ),
    ( "out0", OutputPort(4) ),
    ( "out1", OutputPort(4) ),
    ( "out2", OutputPort(4) ),
    ( "out3", OutputPort(4) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0, 0, 0, 0 ),
    ( 1, 1, 1, 1, 1 ),
    ( 0, 0, 0, 0, 1 ),
    ( 0, 0, 0, 1, 0 ),
    ( 0, 0, 1, 0, 0 ),
    ( 0, 1, 0, 0, 0 ),
    ( 1, 0, 0, 0, 0 ),
    ( 1, 2, 3, 4, 5 ),
    ( 3, 4, 5, 6, 7 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(3), pst.bits(3), pst.bits(3), pst.bits(3), pst.bits(3)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

