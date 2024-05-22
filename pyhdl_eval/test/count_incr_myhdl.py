#=========================================================================
# count_incr_myhdl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from myhdl import *

@block
def TopModule( clk, ld, en, in_, out ):

  # Sequential logic

  reg_next = Signal( modbv(0)[8:] )
  reg_out  = Signal( modbv(0)[8:] )

  @always( clk.posedge )
  def seq():
    if ld:
      reg_out.next = in_
    elif en:
      reg_out.next = reg_next

  # Combinational logic

  @always_comb
  def comb0():
    reg_next.next = reg_out + 1

  # Structural connections

  @always_comb
  def comb1():
    out.next = reg_out

  # Return blocks

  return seq, comb0, comb1

