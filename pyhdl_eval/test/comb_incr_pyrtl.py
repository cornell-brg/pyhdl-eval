#=========================================================================
# comb_incr_pyrtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyrtl import *

def TopModule( in_ ):

  # Declare outputs

  out = WireVector(8)

  # Combinational logic

  out <<= in_ + 1

  # Return outputs

  return out

