#=========================================================================
# Prob09p04_comb_param_2to1_mux_test
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

def mk_config( nbits ):
  config = Config(
    parameters = {
      "nbits" : nbits,
    },
    ports = [
      ( "in0", InputPort (nbits) ),
      ( "in1", InputPort (nbits) ),
      ( "sel", InputPort (1)     ),
      ( "out", OutputPort(nbits) ),
    ],
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits4_directed
#-------------------------------------------------------------------------

def test_case_nbits4_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=4),
  [
    (0,0,0),
    (0,1,1),
    (0,0,0),
    (0,1,1),
    (1,0,0),
    (1,1,1),
    (1,0,0),
    (1,1,1),

    (0,0,0),
    (0,2,1),
    (0,0,0),
    (0,2,1),
    (2,0,0),
    (2,2,1),
    (2,0,0),
    (2,2,1),
  ])

#-------------------------------------------------------------------------
# test_case_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=13),
  [
    (0,0,0),
    (0,1,1),
    (0,0,0),
    (0,1,1),
    (1,0,0),
    (1,1,1),
    (1,0,0),
    (1,1,1),

    (0,0,0),
    (0,2,1),
    (0,0,0),
    (0,2,1),
    (2,0,0),
    (2,2,1),
    (2,0,0),
    (2,2,1),
  ])

#-------------------------------------------------------------------------
# test_case_nbits13_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(13), pst.bits(13), pst.bits(1) )))
def test_case_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, mk_config(nbits=13), test_vectors )

