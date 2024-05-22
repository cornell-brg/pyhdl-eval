#=========================================================================
# count_incr_amaranth
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from amaranth import *

class TopModule( Elaboratable ):

  def __init__( s ):

    # Port-based interface

    s.ld  = Signal()
    s.en  = Signal()
    s.in_ = Signal(8)
    s.out = Signal(8)

  def elaborate( s, platform ):

    # Create module

    m = Module()

    # Sequential logic

    reg_next = Signal( 8 )
    reg_out  = Signal( 8 )

    with m.If( s.ld ):
      m.d.sync += reg_out.eq( s.in_ )
    with m.Elif( s.en ):
      m.d.sync += reg_out.eq( reg_next )

    # Combinational logic

    m.d.comb += reg_next.eq( reg_out + 1 )

    # Structural connections

    m.d.comb += s.out.eq( reg_out )

    # Return module

    return m

