#=========================================================================
# Prob06p02_comb_codes_enc_16to4_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.datatypes import strategies as pst

from test_utils import construct, print_line_trace

from hypothesis import settings, given
from hypothesis import strategies as st

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in_ = InPort (16)
    s.out = OutPort(4)

    @update
    def up():

      if   s.in_ == 0b0000_0000_0000_0001: s.out @= 0
      elif s.in_ == 0b0000_0000_0000_0010: s.out @= 1
      elif s.in_ == 0b0000_0000_0000_0100: s.out @= 2
      elif s.in_ == 0b0000_0000_0000_1000: s.out @= 3

      elif s.in_ == 0b0000_0000_0001_0000: s.out @= 4
      elif s.in_ == 0b0000_0000_0010_0000: s.out @= 5
      elif s.in_ == 0b0000_0000_0100_0000: s.out @= 6
      elif s.in_ == 0b0000_0000_1000_0000: s.out @= 7

      elif s.in_ == 0b0000_0001_0000_0000: s.out @= 8
      elif s.in_ == 0b0000_0010_0000_0000: s.out @= 9
      elif s.in_ == 0b0000_0100_0000_0000: s.out @= 10
      elif s.in_ == 0b0000_1000_0000_0000: s.out @= 11

      elif s.in_ == 0b0001_0000_0000_0000: s.out @= 12
      elif s.in_ == 0b0010_0000_0000_0000: s.out @= 13
      elif s.in_ == 0b0100_0000_0000_0000: s.out @= 14
      elif s.in_ == 0b1000_0000_0000_0000: s.out @= 15

      else:
        s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_ = InPort (16)
    s.out = OutPort(4)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_ = test_vector

    ref.in_ @= in_
    dut.in_ @= in_

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in_, ">", dut.out )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000_0000_0001,
    0b0000_0000_0000_0010,
    0b0000_0000_0000_0100,
    0b0000_0000_0000_1000,

    0b0000_0000_0001_0000,
    0b0000_0000_0010_0000,
    0b0000_0000_0100_0000,
    0b0000_0000_1000_0000,

    0b0000_0001_0000_0000,
    0b0000_0010_0000_0000,
    0b0000_0100_0000_0000,
    0b0000_1000_0000_0000,

    0b0001_0000_0000_0000,
    0b0010_0000_0000_0000,
    0b0100_0000_0000_0000,
    0b1000_0000_0000_0000,
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000_0000_0000_0000,
    0b0000_0000_0001_0010,
    0b0000_0000_0010_0100,
    0b0000_0000_0100_1000,

    0b0000_0001_0001_0000,
    0b0000_0010_0010_0000,
    0b0000_0100_0100_0000,
    0b0000_1000_1000_0000,

    0b0001_0001_0000_0000,
    0b0010_0010_0000_0000,
    0b0100_0100_0000_0000,
    0b1000_1000_0000_0000,

    0b0001_0001_0001_0001,
    0b0010_0010_0010_0010,
    0b0100_0100_0100_0100,
    0b1111_1111_1111_1111,
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( pst.bits(16) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

