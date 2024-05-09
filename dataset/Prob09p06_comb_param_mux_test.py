#=========================================================================
# Prob09p06_comb_param_mux_test
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
  def construct( s, nports, nbits ):
    s.in_ = [ InPort(nbits) for _ in range(nports) ]
    s.sel = InPort( clog2(nports) )
    s.out = OutPort(nbits)

    @update
    def up():
      s.out @= s.in_[s.sel]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nports, nbits ):
    s.in_ = [ InPort(nbits) for _ in range(nports) ]
    s.sel = InPort( clog2(nports) )
    s.out = OutPort(nbits)

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors, nports, nbits ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nports=nports, nbits=nbits )

  for test_vector in test_vectors:

    for i in range(nports):
      ref.in_[i] @= test_vector[i]
      dut.in_[i] @= test_vector[i]

    ref.sel @= test_vector[nports]
    dut.sel @= test_vector[nports]

    ref.sim_tick()
    dut.sim_tick()

    # Line Tracing
    print(f"{dut.sim_cycle_count()-1:3}:",end=" ")
    for i in range(nports):
      print(f"{dut.in_[i]}",end=" ")
    print(f"{dut.sel}")
    print(f"> {dut.out}")

    assert ref.out == dut.out

#-------------------------------------------------------------------------
# test_case_nbits4_directed
#-------------------------------------------------------------------------

def test_case_nports2_nbits4_directed( pytestconfig ):
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
  nports=2, nbits=4 )

#-------------------------------------------------------------------------
# test_case_nports4_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nports4_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0,0,0),
    (1,0,0,0,0),
    (0,0,0,0,1),
    (0,1,0,0,1),
    (0,0,0,0,2),
    (0,0,1,0,2),
    (0,0,0,0,3),
    (0,0,0,1,3),

    (0,0,0,0,0),
    (2,0,0,0,0),
    (0,0,0,0,1),
    (0,2,0,0,1),
    (0,0,0,0,2),
    (0,0,2,0,2),
    (0,0,0,0,3),
    (0,0,0,2,3),
  ],
  nports=4, nbits=13 )

#-------------------------------------------------------------------------
# test_case_nports4_nbits13_random
#-------------------------------------------------------------------------
 
@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(13), pst.bits(13), pst.bits(13), pst.bits(13),
      pst.bits(2)
    )
  ))
def test_case_nports4_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nports=4, nbits=13 )

