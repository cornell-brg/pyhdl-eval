#=========================================================================
# pipe_incr_migen
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from migen import *

class TopModule( Module ):

  def __init__( s ):

    # Port-based interface

    s.in0 = Signal(8)
    s.in1 = Signal(8)
    s.out = Signal(8)

    # Stage 0

    in0_X0 = Signal( 8 )
    in1_X0 = Signal( 8 )

    s.sync += [
      in0_X0.eq( s.in0 ),
      in1_X0.eq( s.in1 ),
    ]

    incr0_X0 = Signal( 8 )
    incr1_X0 = Signal( 8 )

    s.comb += [
      incr0_X0.eq( in0_X0 + 1 ),
      incr1_X0.eq( in1_X0 + 1 ),
    ]

    # Stage 1

    incr0_X1 = Signal( 8 )
    incr1_X1 = Signal( 8 )

    s.sync += [
      incr0_X1.eq( incr0_X0 ),
      incr1_X1.eq( incr1_X0 ),
    ]

    s.comb += [
      s.out.eq( incr0_X1 + incr1_X1 ),
    ]

