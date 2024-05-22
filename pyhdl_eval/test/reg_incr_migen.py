#=========================================================================
# reg_incr_migen
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from migen import *

@ResetInserter()
class TopModule( Module ):

  def __init__( s ):

    # Port-based interface

    s.in_ = Signal(8)
    s.out = Signal(8)

    # Sequential logic

    reg_out = Signal( 8, reset=0 )

    s.sync += reg_out.eq( s.in_ )

    # Combinational logic

    temp_wire = Signal(8)

    s.comb += temp_wire.eq( reg_out + 1 )

    # Structural connections

    s.comb += s.out.eq( temp_wire )

