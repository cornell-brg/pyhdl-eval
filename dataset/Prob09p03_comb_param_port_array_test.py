#=========================================================================
# Prob09p03_comb_param_port_array_test
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
    s.in_ = [ InPort (nbits) for _ in range(nports) ]
    s.out = [ OutPort(nbits) for _ in range(nports) ]

    @update
    def up():
      for i in range(0,nports):
        s.out[i] @= s.in_[i]

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s, nports, nbits ):
    s.in_ = [ InPort (nbits) for _ in range(nports) ]
    s.out = [ OutPort(nbits) for _ in range(nports) ]

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors, nports, nbits ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule,
                       nports=nports, nbits=nbits )

  for test_vector in test_vectors:

    in_ = test_vector

    for i in range(nports):
      ref.in_[i] @= in_[i]
      dut.in_[i] @= in_[i]

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    # Line Tracing
    print(f"{dut.sim_cycle_count()-1:3}:",end=" ")
    for i in range(nports):
      print(f"{dut.in_[i]}",end=" ")
    print(">",end=" ")
    for i in range(nports):
      print(f"{dut.out[i]}",end=" ")
    print("")

    for i in range(nports):
      assert ref.out[i] == dut.out[i]

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_nports2_nbits8_directed
#-------------------------------------------------------------------------

def test_case_nports2_nbits8_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x00, 0x00 ),
    ( 0x00, 0x01 ),
    ( 0x01, 0x00 ),
    ( 0x01, 0x23 ),
    ( 0x45, 0x67 ),
    ( 0x89, 0xab ),
    ( 0xcd, 0xef ),
  ],
  nports=2, nbits=8 )

#-------------------------------------------------------------------------
# test_case_nports2_nbits8_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(8), pst.bits(8)
    )
  ))
def test_case_nports2_nbits8_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nports=2, nbits=8 )

#-------------------------------------------------------------------------
# test_case_nports3_nbits13_directed
#-------------------------------------------------------------------------

def test_case_nports3_nbits13_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0x0000, 0x0000, 0x0000 ),
    ( 0x0000, 0x0000, 0x0001 ),
    ( 0x0000, 0x0001, 0x0000 ),
    ( 0x0001, 0x0000, 0x0000 ),
    ( 0x0123, 0x1567, 0x19ab ),
    ( 0x1def, 0x0123, 0x1567 ),
  ],
  nports=3, nbits=13 )

#-------------------------------------------------------------------------
# test_case_nports3_nbits13_random
#-------------------------------------------------------------------------

@settings(deadline=1000,max_examples=20)
@given(
  st.lists(
    st.tuples(
      pst.bits(13), pst.bits(13), pst.bits(13)
    )
  ))
def test_case_nports3_nbits13_random( pytestconfig, test_vectors ):
  run_sim( pytestconfig, test_vectors, nports=3, nbits=13 )

