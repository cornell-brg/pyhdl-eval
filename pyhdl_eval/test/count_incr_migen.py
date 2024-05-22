#=========================================================================
# count_incr_migen
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from migen import *

class TopModule( Module ):

  def __init__( s ):

    # Port-based interface

    s.ld  = Signal()
    s.en  = Signal()
    s.in_ = Signal(8)
    s.out = Signal(8)

    # Sequential logic

    reg_next = Signal( 8 )
    reg_out  = Signal( 8 )

    s.sync += \
      If  ( s.ld, reg_out.eq( s.in_    ) ). \
      Elif( s.en, reg_out.eq( reg_next ) )

    # Combinational logic

    s.comb += reg_next.eq( reg_out + 1 )

    # Structural connections

    s.comb += s.out.eq( reg_out )

