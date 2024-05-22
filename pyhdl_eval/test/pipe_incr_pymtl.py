#=========================================================================
# pipe_incr_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s ):

    # Port-based interface

    s.in0 = InPort ( Bits8 )
    s.in1 = InPort ( Bits8 )
    s.out = OutPort( Bits8 )

    # Stage 0

    s.in0_X0 = Wire( Bits8 )
    s.in1_X0 = Wire( Bits8 )

    @update_ff
    def stage0_pipe():
      s.in0_X0 <<= s.in0
      s.in1_X0 <<= s.in1

    s.incr0_X0 = Wire( Bits8 )
    s.incr1_X0 = Wire( Bits8 )

    @update
    def stage0_comb():
      s.incr0_X0 @= s.in0_X0 + 1
      s.incr1_X0 @= s.in1_X0 + 1

    # Stage 1

    s.incr0_X1 = Wire( Bits8 )
    s.incr1_X1 = Wire( Bits8 )

    @update_ff
    def stage1_pipe():
      s.incr0_X1 <<= s.incr0_X0
      s.incr1_X1 <<= s.incr1_X0

    @update
    def stage1_comb():
      s.out @= s.incr0_X1 + s.incr1_X1

