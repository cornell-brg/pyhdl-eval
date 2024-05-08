#=========================================================================
# Prob07p18_comb_arith_4x8b_sorter_test
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
    s.in0  = InPort (8)
    s.in1  = InPort (8)
    s.in2  = InPort (8)
    s.in3  = InPort (8)
    s.out0 = OutPort(8)
    s.out1 = OutPort(8)
    s.out2 = OutPort(8)
    s.out3 = OutPort(8)

    @update
    def up():
      ins  = [ s.in0,  s.in1,  s.in2,  s.in3  ]
      outs = [ s.out0, s.out1, s.out2, s.out3 ]
      for in_,out in zip(sorted(ins),outs):
        out @= in_

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in0  = InPort (8)
    s.in1  = InPort (8)
    s.in2  = InPort (8)
    s.in3  = InPort (8)
    s.out0 = OutPort(8)
    s.out1 = OutPort(8)
    s.out2 = OutPort(8)
    s.out3 = OutPort(8)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in0,in1,in2,in3 = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.in2 @= in2
    ref.in3 @= in3

    dut.in0 @= in0
    dut.in1 @= in1
    dut.in2 @= in2
    dut.in3 @= in3

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in0,  dut.in1,  dut.in2,  dut.in3,
                      ">", dut.out0, dut.out1, dut.out2, dut.out3 )

    assert ref.out0 == dut.out0
    assert ref.out1 == dut.out1
    assert ref.out2 == dut.out2
    assert ref.out3 == dut.out3

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

def test_case_small( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 1, 2, 3, 4 ),
    ( 4, 3, 2, 1 ),
    ( 3, 4, 1, 2 ),
    ( 1, 4, 3, 2 ),
  ])

#-------------------------------------------------------------------------
# test_case_dups
#-------------------------------------------------------------------------

def test_case_dups( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0, 0, 0 ),
    ( 9, 9, 9, 9 ),
    ( 1, 1, 2, 2 ),
    ( 2, 2, 1, 1 ),
    ( 2, 1, 2, 1 ),
    ( 1, 1, 2, 1 ),
    ( 1, 2, 2, 2 ),
    ( 2, 2, 1, 2 ),
  ])

#-------------------------------------------------------------------------
# test_case_large
#-------------------------------------------------------------------------

def test_case_large( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 101, 102, 103, 104 ),
    ( 104, 103, 102, 101 ),
    ( 103, 104, 101, 102 ),
    ( 101, 104, 103, 102 ),
    ( 255, 254, 252, 253 ),
    ( 252, 253, 254, 255 ),
    ( 253, 252, 255, 254 ),
    ( 255, 252, 253, 254 ),
  ])

#-------------------------------------------------------------------------
# test_case_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(8), pst.bits(8), pst.bits(8), pst.bits(8)
    )
  ))
def test_case_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors )

