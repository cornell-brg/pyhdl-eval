#=========================================================================
# const_myhdl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from myhdl import *

@block
def TopModule( out ):

  # Combinational logic

  const_value = Signal(1)

  @always_comb
  def logic():
    out.next = const_value

  return logic

