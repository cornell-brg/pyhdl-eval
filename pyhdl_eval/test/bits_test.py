#=========================================================================
# bits_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

from pyhdl_eval.bits import Bits

#-------------------------------------------------------------------------
# check_bits
#-------------------------------------------------------------------------

def check_bits( x, nbits, uint, int_=None ):
  print(f"checking {repr(x):2} == {uint:2}",end="")
  assert x.nbits() == nbits
  assert x.uint()  == uint
  if int_ != None:
    print(f" ({int_:2})",end="")
    assert x.int() == int_
  print("")

#-------------------------------------------------------------------------
# test_nbits3_unsigned
#-------------------------------------------------------------------------

def test_nbits3_unsigned():
  print("")

  check_bits( Bits(3,0b000), 3, 0x0 )
  check_bits( Bits(3,0b001), 3, 0x1 )
  check_bits( Bits(3,0b010), 3, 0x2 )
  check_bits( Bits(3,0b011), 3, 0x3 )

  check_bits( Bits(3,0b100), 3, 0x4 )
  check_bits( Bits(3,0b101), 3, 0x5 )
  check_bits( Bits(3,0b110), 3, 0x6 )
  check_bits( Bits(3,0b111), 3, 0x7 )

#-------------------------------------------------------------------------
# test_nbits3_signed
#-------------------------------------------------------------------------

def test_nbits3_signed():
  print("")

  check_bits( Bits(3,0),  3, 0x0, 0 )
  check_bits( Bits(3,1),  3, 0x1, 1 )
  check_bits( Bits(3,2),  3, 0x2, 2 )
  check_bits( Bits(3,3),  3, 0x3, 3 )

  check_bits( Bits(3,-4), 3, 0x4, -4 )
  check_bits( Bits(3,-3), 3, 0x5, -3 )
  check_bits( Bits(3,-2), 3, 0x6, -2 )
  check_bits( Bits(3,-1), 3, 0x7, -1 )

#-------------------------------------------------------------------------
# test_nbits4_unsigned
#-------------------------------------------------------------------------

def test_nbits4_unsigned():
  print("")

  check_bits( Bits(4,0b0000), 4, 0x0 )
  check_bits( Bits(4,0b0001), 4, 0x1 )
  check_bits( Bits(4,0b0010), 4, 0x2 )
  check_bits( Bits(4,0b0011), 4, 0x3 )

  check_bits( Bits(4,0b0100), 4, 0x4 )
  check_bits( Bits(4,0b0101), 4, 0x5 )
  check_bits( Bits(4,0b0110), 4, 0x6 )
  check_bits( Bits(4,0b0111), 4, 0x7 )

  check_bits( Bits(4,0b1000), 4, 0x8 )
  check_bits( Bits(4,0b1001), 4, 0x9 )
  check_bits( Bits(4,0b1010), 4, 0xa )
  check_bits( Bits(4,0b1011), 4, 0xb )

  check_bits( Bits(4,0b1100), 4, 0xc )
  check_bits( Bits(4,0b1101), 4, 0xd )
  check_bits( Bits(4,0b1110), 4, 0xe )
  check_bits( Bits(4,0b1111), 4, 0xf )

#-------------------------------------------------------------------------
# test_nbits4_signed
#-------------------------------------------------------------------------

def test_nbits4_signed():
  print("")

  check_bits( Bits(4,0),  4, 0x0, 0 )
  check_bits( Bits(4,1),  4, 0x1, 1 )
  check_bits( Bits(4,2),  4, 0x2, 2 )
  check_bits( Bits(4,3),  4, 0x3, 3 )

  check_bits( Bits(4,4),  4, 0x4, 4 )
  check_bits( Bits(4,5),  4, 0x5, 5 )
  check_bits( Bits(4,6),  4, 0x6, 6 )
  check_bits( Bits(4,7),  4, 0x7, 7 )

  check_bits( Bits(4,-8), 4, 0x8, -8 )
  check_bits( Bits(4,-7), 4, 0x9, -7 )
  check_bits( Bits(4,-6), 4, 0xa, -6 )
  check_bits( Bits(4,-5), 4, 0xb, -5 )

  check_bits( Bits(4,-4), 4, 0xc, -4 )
  check_bits( Bits(4,-3), 4, 0xd, -3 )
  check_bits( Bits(4,-2), 4, 0xe, -2 )
  check_bits( Bits(4,-1), 4, 0xf, -1 )

#-------------------------------------------------------------------------
# test_equals
#-------------------------------------------------------------------------

def test_equals():

  assert Bits(3,0) == Bits(3,0)
  assert Bits(3,1) == Bits(3,1)
  assert Bits(3,2) == Bits(3,2)
  assert Bits(3,3) == Bits(3,3)

  assert Bits(3,4) == Bits(3,-4)
  assert Bits(3,5) == Bits(3,-3)
  assert Bits(3,6) == Bits(3,-2)
  assert Bits(3,7) == Bits(3,-1)

#-------------------------------------------------------------------------
# test_not_equals
#-------------------------------------------------------------------------

def test_not_equals():

  assert Bits(3,0) != Bits(3,1)
  assert Bits(3,1) != Bits(3,2)
  assert Bits(3,2) != Bits(3,3)
  assert Bits(3,3) != Bits(3,-4)

  assert Bits(3,4) != Bits(3,-3)
  assert Bits(3,5) != Bits(3,-2)
  assert Bits(3,6) != Bits(3,-1)
  assert Bits(3,7) != Bits(3,0)

  assert Bits(3,0) != None

