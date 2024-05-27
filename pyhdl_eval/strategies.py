#=========================================================================
# pyhdl_eval.stragegies
#=========================================================================
# Hypothesis strategies for random testing.
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from hypothesis import strategies as st
from pyhdl_eval.bits import Bits

#-------------------------------------------------------------------------
# bits
#-------------------------------------------------------------------------
# Return a Hypothesis search stategy for Bits

@st.composite
def bits( draw, nbits, min_value=None, max_value=None ):

  if min_value == None:
    min_value = 0
  if max_value == None:
    max_value = 2**nbits-1

  if nbits == 1:
    return Bits( nbits, draw( st.booleans() ) )
  else:
    return Bits( nbits, draw( st.integers(min_value,max_value) ) )

