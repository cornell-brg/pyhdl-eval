#=========================================================================
# incr_amaranth
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from amaranth import *

class TopModule( Elaboratable ):

  def __init__( s ):

    # Port-based interface

    s.in_ = Signal(8)
    s.out = Signal(8)

  def elaborate( s, platform ):

    # Create module

    m = Module()

    # Combinational logic

    m.d.comb += s.out.eq( s.in_ + 1 )

    # Return module

    return m

