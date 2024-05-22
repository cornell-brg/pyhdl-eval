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

def bits( nbits ):

  @st.composite
  def strategy_bits( draw ):
    if nbits == 1:
      return Bits( nbits, draw( st.booleans() ) )
    else:
      return Bits( nbits, draw( st.integers(0,2**nbits-1) ) )

  return strategy_bits()

