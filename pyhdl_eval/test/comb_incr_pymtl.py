#=========================================================================
# comb_incr_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s ):

    # Port-based interface

    s.in_ = InPort ( Bits8 )
    s.out = OutPort( Bits8 )

    # Combinational logic

    @update
    def comb():
      s.out @= s.in_ + 1

