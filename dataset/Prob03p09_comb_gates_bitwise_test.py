#=========================================================================
# Prob03p09_comb_gates_bitwise_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort, TraceFormat
from pyhdl_eval.core import run_sim
from pyhdl_eval      import strategies as pst

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "in0",      InputPort (4) ),
    ( "in1",      InputPort (4) ),
    ( "out_and",  OutputPort(4) ),
    ( "out_nand", OutputPort(4) ),
    ( "out_or",   OutputPort(4) ),
    ( "out_nor",  OutputPort(4) ),
  ],
  trace_format=TraceFormat.BIN,
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0b0000, 0b0000 ),
    ( 0b0000, 0b1111 ),
    ( 0b1111, 0b0000 ),
    ( 0b1111, 0b1111 ),
    ( 0b1100, 0b1010 ),
    ( 0b0011, 0b0101 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(4), pst.bits(4)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

