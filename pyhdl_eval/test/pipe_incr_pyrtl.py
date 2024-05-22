#=========================================================================
# pipe_incr_pyrtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyrtl import *

def TopModule( in0, in1 ):

  # Declare outputs

  out = WireVector(8)

  # Stage 0

  in0_X0 = Register( 8 )
  in1_X0 = Register( 8 )

  in0_X0.next <<= in0
  in1_X0.next <<= in1

  incr0_X0 = WireVector(8)
  incr1_X0 = WireVector(8)

  incr0_X0 <<= in0_X0 + 1
  incr1_X0 <<= in1_X0 + 1

  # Stage 1

  incr0_X1 = Register( 8 )
  incr1_X1 = Register( 8 )

  incr0_X1.next <<= incr0_X0
  incr1_X1.next <<= incr1_X0

  out <<= incr0_X1 + incr1_X1

  # Return outputs

  return out

