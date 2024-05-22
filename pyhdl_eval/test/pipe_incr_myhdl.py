#=========================================================================
# pipe_incr_myhdl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from myhdl import *

@block
def TopModule( clk, in0, in1, out ):

  # Stage 0

  in0_X0 = Signal( modbv(0)[8:] )
  in1_X0 = Signal( modbv(0)[8:] )

  @always( clk.posedge )
  def stage0_seq():
    in0_X0.next = in0
    in1_X0.next = in1

  incr0_X0 = Signal( modbv(0)[8:] )
  incr1_X0 = Signal( modbv(0)[8:] )

  @always_comb
  def stage0_comb():
    incr0_X0.next = in0_X0 + 1
    incr1_X0.next = in1_X0 + 1

  # Stage 0

  incr0_X1 = Signal( modbv(0)[8:] )
  incr1_X1 = Signal( modbv(0)[8:] )

  @always( clk.posedge )
  def stage1_seq():
    incr0_X1.next = incr0_X0
    incr1_X1.next = incr1_X0

  @always_comb
  def stage1_comb():
    out.next = incr0_X1 + incr1_X1

  return stage0_seq, stage0_comb, stage1_seq, stage1_comb

