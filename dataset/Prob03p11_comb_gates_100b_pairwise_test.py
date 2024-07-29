#=========================================================================
# Prob03p11_comb_gates_100b_pairwise_test
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
    ( "in_",      InputPort (100) ),
    ( "out_and",  OutputPort( 99) ),
    ( "out_or",   OutputPort( 99) ),
    ( "out_xnor", OutputPort( 99) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    0x0_0000_0000_0000_0000_0000_0000,
    0x0_1234_1234_1234_1234_1234_1234,
    0x1_89ab_cdef_89ab_cdef_89ab_cdef,
    0x2_4567_89ab_cdef_4567_89ab_cdef,
    0x4_0123_4567_89ab_cdef_0123_4567,
    0x8_dead_beef_dead_beef_dead_beef,
    0xf_ffff_ffff_ffff_ffff_ffff_ffff,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=1000,max_examples=20)
@given( st.lists(pst.bits(100)) )
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

