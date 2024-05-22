#=========================================================================
# param_incr_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, InputPort, OutputPort
from pyhdl_eval.core import run_sim, dsls
from pyhdl_eval      import strategies as pst

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

def mk_config( nbits, value ):
  config = Config(
    parameters = {
      "nbits" : nbits,
    },
    ports = [
      ( "clk",   InputPort (1)     ),
      ( "reset", InputPort (1)     ),
      ( "in_",   InputPort (nbits) ),
      ( "out",   OutputPort(nbits) ),
    ],
  )
  return config

#-------------------------------------------------------------------------
# test_case_nbits4_value1_directed
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_nbits4_directed( dslstr ):
  run_sim( dslstr, __file__, mk_config(nbits=4,value=1),
  [
    # rs in_
    ( 0, 0x0 ),
    ( 0, 0x1 ),
    ( 0, 0x3 ),
    ( 0, 0x5 ),
    ( 0, 0x7 ),
    ( 0, 0x9 ),
    ( 0, 0x0 ),
    ( 0, 0x0 ),
  ])

#-------------------------------------------------------------------------
# test_case_nbits4_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(4) )))
def test_case_nbits4_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, mk_config(nbits=4,value=1), test_vectors )

#-------------------------------------------------------------------------
# test_case_nbits8_value2_directed
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_nbits8_value2_directed( dslstr ):
  run_sim( dslstr, __file__, mk_config(nbits=8,value=2),
  [
    # rs in_
    ( 0, 0x00 ),
    ( 0, 0x11 ),
    ( 0, 0x13 ),
    ( 0, 0x15 ),
    ( 0, 0x17 ),
    ( 0, 0x19 ),
    ( 0, 0x00 ),
    ( 0, 0x00 ),
  ])

#-------------------------------------------------------------------------
# test_case_nbits8_value2_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(8) )))
def test_case_nbits8_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, mk_config(nbits=8,value=2), test_vectors )

