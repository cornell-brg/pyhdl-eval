#=========================================================================
# const_migen
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from migen import *

class TopModule( Module ):

  def __init__( s ):

    # Port-based interface

    s.out = Signal(8)

    # Combinational logic

    s.comb += s.out.eq( 1 )

