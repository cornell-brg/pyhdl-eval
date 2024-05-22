#=========================================================================
# reg_incr_amaranth
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

    # Sequential logic

    reg_out = Signal( 8, reset=0 )

    m.d.sync += reg_out.eq( s.in_ )

    # Combinational logic

    temp_wire = Signal(8)

    m.d.comb += temp_wire.eq( reg_out + 1 )

    # Structural connections

    m.d.comb += s.out.eq( temp_wire )

    # Return module

    return m

