#=========================================================================
# comb_incr_test
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
    ( "in_", InputPort (8) ),
    ( "out", OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_small( dslstr ):
  run_sim( dslstr, __file__, config, [ 0, 1, 3, 5, 7, 9 ] )

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_large( dslstr ):
  run_sim( dslstr, __file__, config, [ 100, 150, 200, 254 ] )

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_overflow( dslstr ):
  run_sim( dslstr, __file__, config, [ 255 ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(8) ) )
def test_case_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, config, test_vectors )

