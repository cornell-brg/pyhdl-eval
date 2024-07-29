#=========================================================================
# Prob07p11_comb_arith_8b_fxp_umul_test
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
    ( "in0",      InputPort (8) ),
    ( "in1",      InputPort (8) ),
    ( "out",      OutputPort(8) ),
    ( "overflow", OutputPort(1) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_whole
#-------------------------------------------------------------------------

def test_case_whole( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x10, 0x00 ),
    ( 0x10, 0x10 ),
    ( 0x10, 0x00 ),
    ( 0x20, 0x20 ),
    ( 0x20, 0x30 ),
    ( 0x30, 0x20 ),
    ( 0x30, 0x30 ),
    ( 0x40, 0x30 ),
    ( 0x30, 0x40 ),
  ])

#-------------------------------------------------------------------------
# test_case_frac_exact
#-------------------------------------------------------------------------

def test_case_frac_exact( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x08, 0x08 ),
    ( 0x08, 0x04 ),
    ( 0x04, 0x08 ),
    ( 0x02, 0x08 ),
    ( 0x08, 0x02 ),
  ])

#-------------------------------------------------------------------------
# test_case_frac_nonexact
#-------------------------------------------------------------------------

def test_case_frac_nonexact( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x01, 0x01 ),
    ( 0x01, 0x11 ),
    ( 0x01, 0x21 ),
    ( 0x01, 0x31 ),
    ( 0x01, 0x41 ),
    ( 0x01, 0x51 ),
    ( 0x01, 0x61 ),
    ( 0x01, 0x71 ),
    ( 0x01, 0x81 ),
    ( 0x01, 0x91 ),
    ( 0x01, 0xa1 ),
    ( 0x01, 0xb1 ),
    ( 0x01, 0xc1 ),
    ( 0x01, 0xd1 ),
    ( 0x01, 0xe1 ),
    ( 0x01, 0xf1 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig, __file__, config,
  [
    ( 0x11, 0xf1 ),
    ( 0x12, 0xef ),
    ( 0x80, 0x80 ),
    ( 0x80, 0x70 ),
    ( 0x80, 0x60 ),
    ( 0x80, 0x50 ),
    ( 0x80, 0x40 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(derandomize=True,deadline=None,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, __file__, config, test_vectors )

