#=========================================================================
# Prob09p05_comb_param_2to1_mux_test
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
  def construct( s, nbits ):
    s.in0 = InPort(nbits)
    s.in1 = InPort(nbits)
    s.sel = InPort()
    s.out = OutPort(nbits)

    @update
    def up():
      if s.sel == 0:
        s.out @= s.in0
      else:
        s.out @= s.in1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nbits ):
    s.in0 = InPort(nbits)
    s.in1 = InPort(nbits)
    s.sel = InPort()
    s.out = OutPort(nbits)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors, nbits ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nbits=nbits )

  for test_vector in test_vectors:

    in0,in1,sel = test_vector

    ref.in0 @= in0
    ref.in1 @= in1
    ref.sel @= sel

    dut.in0 @= in0
    dut.in1 @= in1
    dut.sel @= sel

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.in0, dut.in1, dut.sel, ">", dut.out )

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_nbits4_directed
#-------------------------------------------------------------------------

def test_case_nbits4_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0),
    (0,1,1),
    (0,0,0),
    (0,1,1),
    (1,0,0),
    (1,1,1),
    (1,0,0),
    (1,1,1),

    (0,0,0),
    (0,2,1),
    (0,0,0),
    (0,2,1),
    (2,0,0),
    (2,2,1),
    (2,0,0),
    (2,2,1),
  ],
  nbits=4 )

#-------------------------------------------------------------------------
# test_case_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0),
    (0,1,1),
    (0,0,0),
    (0,1,1),
    (1,0,0),
    (1,1,1),
    (1,0,0),
    (1,1,1),

    (0,0,0),
    (0,2,1),
    (0,0,0),
    (0,2,1),
    (2,0,0),
    (2,2,1),
    (2,0,0),
    (2,2,1),
  ],
  nbits=13 )

#-------------------------------------------------------------------------
# test_case_nbits13_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given( st.lists( st.tuples( pst.bits(13), pst.bits(13), pst.bits(1) )))
def test_case_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nbits=13 )

