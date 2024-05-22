#=========================================================================
# reg_incr_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s ):

    # Port-based interface

    s.in_ = InPort ( Bits8 )
    s.out = OutPort( Bits8 )

    # Sequential logic

    s.reg_out = Wire( Bits8 )

    @update_ff
    def seq():
      if s.reset:
        s.reg_out <<= 0
      else:
        s.reg_out <<= s.in_

    # Combinational logic

    s.temp_wire = Wire( Bits8 )

    @update
    def comb():
      s.temp_wire @= s.reg_out + 1

    # Structural connections

    s.out //= s.temp_wire

