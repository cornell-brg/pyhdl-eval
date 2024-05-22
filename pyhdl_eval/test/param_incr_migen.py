#=========================================================================
# param_incr_migen
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from migen import *

@ResetInserter()
class TopModule( Module ):

  def __init__( s, nbits ):

    # Port-based interface

    s.in_ = Signal( nbits )
    s.out = Signal( nbits )

    # Sequential logic

    reg_out = Signal( nbits, reset=0 )

    s.sync += reg_out.eq( s.in_ )

    # Combinational logic

    temp_wire = Signal( nbits )

    s.comb += temp_wire.eq( reg_out + 1 )

    # Structural connections

    s.comb += s.out.eq( temp_wire )

