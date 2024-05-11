#=========================================================================
# Prob07p12_comb_arith_8b_fxp_umul_test
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
    s.in0      = InPort (8)
    s.in1      = InPort (8)
    s.out      = OutPort(8)
    s.overflow = OutPort()

    s.temp     = Wire(16)

    @update
    def up():

      s.temp     @= zext( s.in0, 16 ) * zext( s.in1, 16 )
      s.overflow @= s.temp[12:16] != 0

      if s.overflow:
        s.out @= 0
      else:
        s.out @= trunc( s.temp >> 4, 8 )

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0      = InPort (8)
    s.in1      = InPort (8)
    s.out      = OutPort(8)
    s.overflow = OutPort()

#-------------------------------------------------------------------------
# fxp2str
#-------------------------------------------------------------------------

def fxp2str( fxp ):

  i = fxp[4:8] # integer part
  f = fxp[0:4] # fractional part

  f3 = f[3].uint() * 2.0**-1
  f2 = f[2].uint() * 2.0**-2
  f1 = f[1].uint() * 2.0**-3
  f0 = f[0].uint() * 2.0**-4

  # convert to a float

  x = i.uint() + f0 + f1 + f2 + f3

  # convert to a string

  return f"({x:7.4f})"

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1

    dut.in0 @= in0
    dut.in1 @= in1

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.in0, fxp2str(dut.in0),
                           dut.in1, fxp2str(dut.in1),
                      ">", dut.out, fxp2str(dut.out),
                           dut.overflow )

    assert ref.out      == dut.out
    assert ref.overflow == dut.overflow

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_whole
#-------------------------------------------------------------------------

def test_case_whole( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x10, 0x00 ),
    ( 0x10, 0x10 ),
    ( 0x10, 0x00 ),
    ( 0x20, 0x20 ),
    ( 0x20, 0x30 ),
    ( 0x30, 0x20 ),
    ( 0x30, 0x30 ),
    ( 0x40, 0x30 ),
    ( 0x30, 0x40 ),
  ])

#-------------------------------------------------------------------------
# test_case_frac_exact
#-------------------------------------------------------------------------

def test_case_frac_exact( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x08, 0x08 ),
    ( 0x08, 0x04 ),
    ( 0x04, 0x08 ),
    ( 0x02, 0x08 ),
    ( 0x08, 0x02 ),
  ])

#-------------------------------------------------------------------------
# test_case_frac_nonexact
#-------------------------------------------------------------------------

def test_case_frac_nonexact( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x01, 0x01 ),
    ( 0x01, 0x11 ),
    ( 0x01, 0x21 ),
    ( 0x01, 0x31 ),
    ( 0x01, 0x41 ),
    ( 0x01, 0x51 ),
    ( 0x01, 0x61 ),
    ( 0x01, 0x71 ),
    ( 0x01, 0x81 ),
    ( 0x01, 0x91 ),
    ( 0x01, 0xa1 ),
    ( 0x01, 0xb1 ),
    ( 0x01, 0xc1 ),
    ( 0x01, 0xd1 ),
    ( 0x01, 0xe1 ),
    ( 0x01, 0xf1 ),
  ])

#-------------------------------------------------------------------------
# test_case_overflow
#-------------------------------------------------------------------------

def test_case_overflow( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x11, 0xf1 ),
    ( 0x12, 0xef ),
    ( 0x80, 0x80 ),
    ( 0x80, 0x70 ),
    ( 0x80, 0x60 ),
    ( 0x80, 0x50 ),
    ( 0x80, 0x40 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(8), pst.bits(8) ) ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

