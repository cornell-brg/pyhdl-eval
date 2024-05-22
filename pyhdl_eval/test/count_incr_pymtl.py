#=========================================================================
# count_incr_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s ):

    # Port-based interface

    s.ld  = InPort ()
    s.en  = InPort ()
    s.in_ = InPort ( Bits8 )
    s.out = OutPort( Bits8 )

    # Sequential logic

    s.reg_next = Wire( Bits8 )
    s.reg_out  = Wire( Bits8 )

    @update_ff
    def seq():
      if s.ld:
        s.reg_out <<= s.in_
      elif s.en:
        s.reg_out <<= s.reg_next

    # Combinational logic

    @update
    def comb():
      s.reg_next @= s.reg_out + 1

    # Structural connections

    s.out //= s.reg_out

