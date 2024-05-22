#=========================================================================
# param_incr_pyrtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyrtl import *

def TopModule( in_, nbits ):

  # Declare outputs

  out = WireVector( nbits )

  # Sequential logic

  reg_out = Register( nbits, reset_value=0 )
  reg_out.next <<= in_

  # Combinational logic

  temp_wire = WireVector( nbits )
  temp_wire <<= reg_out + 1

  # Structural connections

  out <<= temp_wire

  # Return outputs

  return out

