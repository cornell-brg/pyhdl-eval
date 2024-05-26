#=========================================================================
# count_incr_test
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
    ( "en",    InputPort (1) ),
    ( "ld",    InputPort (1) ),
    ( "in_",   InputPort (8) ),
    ( "out",   OutputPort(8) ),
  ],
  dead_cycles=1,
  dead_cycle_inputs=(1,1,0),
)

#-------------------------------------------------------------------------
# test_case_ld_zero
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_ld_zero( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # en ld in_
    ( 1, 1, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_ld_small
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_ld_small( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # en ld in_
    ( 1, 1, 4 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_ld_large
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_ld_large( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # en ld in_
    ( 1, 1, 254 ),
    ( 1, 0,   0 ),
    ( 1, 0,   0 ),
    ( 1, 0,   0 ),
    ( 1, 0,   0 ),
    ( 1, 0,   0 ),
    ( 0, 0,   0 ),
    ( 0, 0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_multi_ld
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_mult_ld( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # en ld in_
    ( 1, 1, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
    ( 1, 1, 9 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 1, 0, 0 ),
    ( 0, 0, 0 ),
    ( 0, 0, 0 ),
  ])

#-------------------------------------------------------------------------
# test_case_multi_en
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_mult_en( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # en ld in_
    ( 1, 1,  0 ),
    ( 1, 0,  1 ),
    ( 0, 0,  2 ),
    ( 0, 0,  3 ),
    ( 1, 0,  4 ),
    ( 1, 0,  5 ),
    ( 0, 0,  6 ),
    ( 0, 0,  7 ),
    ( 1, 0,  8 ),
    ( 1, 0,  9 ),
    ( 0, 0, 10 ),
    ( 0, 0, 11 ),
    ( 1, 0, 12 ),
    ( 1, 0, 13 ),
    ( 0, 0, 14 ),
    ( 0, 0, 15 ),
    ( 0, 0,  0 ),
    ( 0, 0,  0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(1), pst.bits(1), pst.bits(8) )))
def test_case_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, config, test_vectors )

