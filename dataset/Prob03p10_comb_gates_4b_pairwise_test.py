#=========================================================================
# Prob03p10_comb_gates_4b_pairwise_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in_      = InPort(4)
    s.out_and  = OutPort(3)
    s.out_or   = OutPort(3)
    s.out_xnor = OutPort(3)

    @update
    def up():

      # AND operation on consecutive pairs

      s.out_and[0]  @= s.in_[0] & s.in_[1];
      s.out_and[1]  @= s.in_[1] & s.in_[2];
      s.out_and[2]  @= s.in_[2] & s.in_[3];

      # OR operation on consecutive pairs

      s.out_or[0]   @= s.in_[0] | s.in_[1];
      s.out_or[1]   @= s.in_[1] | s.in_[2];
      s.out_or[2]   @= s.in_[2] | s.in_[3];

      # XNOR operation on consecutive pairs

      s.out_xnor[0] @= ~(s.in_[0] ^ s.in_[1]);
      s.out_xnor[1] @= ~(s.in_[1] ^ s.in_[2]);
      s.out_xnor[2] @= ~(s.in_[2] ^ s.in_[3]);

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_      = InPort(4)
    s.out_and  = OutPort(3)
    s.out_or   = OutPort(3)
    s.out_xnor = OutPort(3)

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

    print_line_trace( dut, dut.in_, ">",
                      dut.out_and, dut.out_or, dut.out_xnor )

    assert ref.out_and  == dut.out_and
    assert ref.out_or   == dut.out_or
    assert ref.out_xnor == dut.out_xnor

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    0b0000,
    0b0001,
    0b0010,
    0b0011,
    0b0100,
    0b0101,
    0b0110,
    0b0111,

    0b1000,
    0b1001,
    0b1010,
    0b1011,
    0b1100,
    0b1101,
    0b1110,
    0b1111,
  ])

