#=========================================================================
# param_incr_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s, nbits ):

    # Port-based interface

    s.in_ = InPort ( nbits )
    s.out = OutPort( nbits )

    # Sequential logic

    s.reg_out = Wire( nbits )

    @update_ff
    def block1():
      if s.reset:
        s.reg_out <<= 0
      else:
        s.reg_out <<= s.in_

    # Combinational logic

    s.temp_wire = Wire( nbits )

    @update
    def block2():
      s.temp_wire @= s.reg_out + 1

    # Structural connections

    s.out //= s.temp_wire

