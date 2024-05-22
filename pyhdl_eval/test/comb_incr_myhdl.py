#=========================================================================
# comb_incr_myhdl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from myhdl import *

@block
def TopModule( in_, out ):

  # Combinational logic

  @always_comb
  def comb():
    out.next = in_ + 1

  return comb

