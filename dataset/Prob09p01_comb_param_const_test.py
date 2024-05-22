#=========================================================================
# Prob09p01_comb_param_const_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

def mk_config( nbits, value ):
  config = Config(
    parameters = {
      "nbits" : nbits,
      "value" : value,
    },
    ports = [
      ( "out", OutputPort(nbits) ),
    ],
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=8,value=0xef) )

#-------------------------------------------------------------------------
# test_case_nbits32_directed
#-------------------------------------------------------------------------

def test_case_nbits32_directed( pytestconfig ):
  run_sim( pytestconfig, __file__, mk_config(nbits=32,value=0xcafecafe) )

