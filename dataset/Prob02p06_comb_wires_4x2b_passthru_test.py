#=========================================================================
# Prob02p06_comb_wires_4x2b_passthru_test
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
    ( "in0",  InputPort (2) ),
    ( "in1",  InputPort (2) ),
    ( "in2",  InputPort (2) ),
    ( "in3",  InputPort (2) ),
    ( "out0", OutputPort(2) ),
    ( "out1", OutputPort(2) ),
    ( "out2", OutputPort(2) ),
    ( "out3", OutputPort(2) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0, 0, 0, 0 ),
    ( 0, 1, 2, 3 ),
    ( 3, 0, 1, 2 ),
    ( 2, 3, 0, 1 ),
    ( 1, 2, 3, 0 ),
    ( 0, 0, 1, 1 ),
    ( 0, 1, 1, 0 ),
    ( 1, 1, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(2), pst.bits(2), pst.bits(2), pst.bits(2)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

