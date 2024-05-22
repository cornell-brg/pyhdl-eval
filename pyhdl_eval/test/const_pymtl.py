#=========================================================================
# const_pymtl
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pymtl3 import *

class TopModule( Component ):

  def construct( s ):

    # Port-based interface

    s.out = OutPort( Bits8 )

    # Connect to constant

    connect( s.out, 1 )

