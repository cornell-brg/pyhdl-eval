#=========================================================================
# reg_incr_test
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

config = Config(
  ports = [
    ( "clk",   InputPort (1) ),
    ( "reset", InputPort (1) ),
    ( "in_",   InputPort (8) ),
    ( "out",   OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_small( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # rs in_
    ( 0, 0 ),
    ( 0, 1 ),
    ( 0, 3 ),
    ( 0, 5 ),
    ( 0, 7 ),
    ( 0, 9 ),
    ( 0, 0 ),
    ( 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_large( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # rs in_
    ( 0, 100 ),
    ( 0, 150 ),
    ( 0, 200 ),
    ( 0, 254 ),
    ( 0, 0   ),
    ( 0, 0   ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_overflow( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # rs in_
    ( 0, 255 ),
    ( 0, 255 ),
    ( 0, 255 ),
    ( 0, 0   ),
    ( 0, 0   ),
  ])

#-------------------------------------------------------------------------
# test_case_reset
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_reset( dslstr ):
  if dslstr == "pyrtl":
    pytest.skip(reason="PyRTL cannot handle multiple resets in single simulation")
  run_sim( dslstr, __file__, config,
  [
    # rs in_
    ( 0, 42 ),
    ( 0, 42 ),
    ( 0, 42 ),
    ( 1, 42 ),
    ( 1, 42 ),
    ( 0,  0 ),
    ( 0,  0 ),
    ( 0,  0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( st.just(0), pst.bits(8) )))
def test_case_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, config, test_vectors )

#-------------------------------------------------------------------------
# test_case_random_reset
#-------------------------------------------------------------------------
# pyrtl does not support multiple resets in a single simulation.

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(8) )))
def test_case_random( dslstr, test_vectors ):
  if dslstr == "pyrtl":
    pytest.skip(reason="PyRTL cannot handle multiple resets in single simulation")
  run_sim( dslstr, __file__, config, test_vectors )

