#=========================================================================
# count_incr_pyrtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyrtl import *

def TopModule( en, ld, in_ ):

  # Declare outputs

  out = WireVector(8)

  # Sequential logic

  reg_next = WireVector(8)
  reg_out  = Register(8)

  with conditional_assignment:
    with ld:
      reg_out.next |= in_
    with en:
      reg_out.next |= reg_next

  # Combinational logic

  reg_next <<= reg_out + 1

  # Structural connections

  out <<= reg_out

  # Return outputs

  return out

