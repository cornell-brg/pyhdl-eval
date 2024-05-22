#=========================================================================
# reg_incr_pyrtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyrtl import *

def TopModule( in_ ):

  # Declare outputs

  out = WireVector(8)

  # Sequential logic

  reg_out = Register( 8, reset_value=0 )
  reg_out.next <<= in_

  # Combinational logic

  temp_wire = WireVector(8)
  temp_wire <<= reg_out + 1

  # Structural connections

  out <<= temp_wire

  # Return outputs

  return out

