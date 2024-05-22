#=========================================================================
# reg_incr_myhdl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from myhdl import *

@block
def TopModule( clk, reset, in_, out ):

  # Sequential logic

  reg_out = Signal( modbv(0)[8:] )

  @always( clk.posedge )
  def seq():
    if reset:
      reg_out.next = 0
    else:
      reg_out.next = in_

  # Combinational logic

  temp_wire = Signal( modbv(0)[8:] )

  @always_comb
  def comb0():
    temp_wire.next = reg_out + 1

  # Structural connections

  @always_comb
  def comb1():
    out.next = temp_wire

  # Return blocks

  return seq, comb0, comb1

