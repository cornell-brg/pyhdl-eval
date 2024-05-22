#=========================================================================
# pyhdl_eval.bits
#=========================================================================
# Bits class for representing fixed-bitwidth data. Used to write/read
# ports when testing modules written in various DSLs.
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import math

def clog2( N ):
  assert N > 0
  return int( math.ceil( math.log( N, 2 ) ) )

class Bits:

  #-----------------------------------------------------------------------
  # __init__
  #-----------------------------------------------------------------------

  def __init__( s, nbits=1, value=0 ):

    if nbits < 1:
      raise ValueError(f"Only support 1 <= nbits not {nbits}")

    if isinstance( value, Bits ):
      if nbits != value.nbits:
        raise ValueError( f"nbits must match ({nbits} != {value.nbits})" )
      nbits = value.nbits
      value = value._unit

    if value >= 2**nbits:
      raise ValueError( f"Value {value} ({hex(value)}) is too large for nbits={nbits}" )
    if value < -2**(nbits-1):
      raise ValueError( f"Value {value} ({hex(value)}) is too small for nbits={nbits}" )

    s._nbits = nbits

    if value < 0:
      value = value % (1 << nbits)

    s._uint  = value

  #-----------------------------------------------------------------------
  # nbits
  #-----------------------------------------------------------------------

  def nbits( s ):
    return s._nbits

  #-----------------------------------------------------------------------
  # int/uint
  #-----------------------------------------------------------------------

  def int( s ) :
    sign_bit = s._uint >> (s._nbits - 1)
    if sign_bit:
      return -int( (~s._uint % (1 << s._nbits)) + 1 )
    return s._uint

  def uint( s ) :
    return int(s._uint)

  #-----------------------------------------------------------------------
  # equality
  #-----------------------------------------------------------------------

  def __eq__( s, other ):
    if not isinstance( other, Bits ):
      return False
    return ( s._nbits == other._nbits ) and ( s._uint == other._uint )

  #-----------------------------------------------------------------------
  # string formatting
  #-----------------------------------------------------------------------

  def __repr__( s ):
    return f"Bits({s._nbits},{hex(s._uint)})"

  def __str__( s ):
    return f"{s._uint:x}".zfill(((s._nbits-1)//4)+1)

  def int_str( s ):

    # find max number of decimal digits
    digits = math.ceil( math.log10(2**s._nbits) )

    # add one for the possible negative sign
    digits += 1

    return f"{s.int():{digits}}"

  def uint_str( s ):

    # find max number of decimal digits
    digits = math.ceil( math.log10(2**s._nbits) )

    return f"{s._uint:{digits}}"

  def bin( s ):
    return f"{int(s._uint):b}".zfill(s._nbits)

  def oct( s ):
    return f"{int(s._uint):o}".zfill(((s._nbits-1)//3)+1)

  def hex( s ):
    return f"{int(s._uint):x}".zfill(((s._nbits-1)//4)+1)

