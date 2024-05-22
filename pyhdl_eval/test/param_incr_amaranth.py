#=========================================================================
# param_incr_amaranth
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from amaranth import *

class TopModule( Elaboratable ):

  def __init__( s, nbits ):

    # Port-based interface

    s.in_ = Signal( nbits )
    s.out = Signal( nbits )

    # Save parameters

    s.nbits = nbits

  def elaborate( s, platform ):

    # Create module

    m = Module()

    # Sequential logic

    reg_out = Signal( s.nbits, reset=0 )

    m.d.sync += reg_out.eq( s.in_ )

    # Combinational logic

    temp_wire = Signal( s.nbits )

    m.d.comb += temp_wire.eq( reg_out + 1 )

    # Structural connections

    m.d.comb += s.out.eq( temp_wire )

    # Return module

    return m

