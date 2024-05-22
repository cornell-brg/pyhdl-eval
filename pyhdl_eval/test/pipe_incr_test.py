#=========================================================================
# pipe_incr_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, InputPort, OutputPort, TraceFormat
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
    ( "in0",   InputPort (8) ),
    ( "in1",   InputPort (8) ),
    ( "out",   OutputPort(8) ),
  ],
  trace_format = TraceFormat.UINT,
  dead_cycles  = 2,
)

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_directed( dslstr ):
  run_sim( dslstr, __file__, config,
  [
    # in0 in1
    (  0,   0 ),
    (  1,   3 ),
    (  3,   5 ),
    (  5,   7 ),
    (  7,   9 ),
    (  9,  10 ),
    (  0,   0 ),
    (  0,   0 ),
    (  0,   0 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) )))
def test_case_random( dslstr, test_vectors ):
  run_sim( dslstr, __file__, config, test_vectors )

