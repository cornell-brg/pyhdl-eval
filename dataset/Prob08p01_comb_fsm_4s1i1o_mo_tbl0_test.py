#=========================================================================
# Prob08p01_comb_fsm_4s1i1o_mo_tbl0_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.state      = InPort (4)
    s.in_        = InPort ()
    s.state_next = OutPort(4)
    s.out        = OutPort()

    # State Encoding

    A = 0b0001
    B = 0b0010
    C = 0b0100
    D = 0b1000

    # State Transition Logic

    @update
    def transition():
      s.state_next @= 0
      if s.state == A :
        if   s.in_ == 0 : s.state_next @= A;
        else            : s.state_next @= B;
      elif s.state == B :
        if   s.in_ == 0 : s.state_next @= C;
        else            : s.state_next @= B;
      elif s.state == C :
        if   s.in_ == 0 : s.state_next @= A;
        else            : s.state_next @= D;
      elif s.state == D :
        if   s.in_ == 0 : s.state_next @= C;
        else            : s.state_next @= B;

    # State Output Logic

    @update
    def output():
      if   s.state == A : s.out @= 0
      elif s.state == B : s.out @= 0
      elif s.state == C : s.out @= 0
      elif s.state == D : s.out @= 1
      else              : s.out @= 0

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.state      = InPort (4)
    s.in_        = InPort ()
    s.state_next = OutPort(4)
    s.out        = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    state,in_ = test_vector

    ref.state @= state
    ref.in_   @= in_

    dut.state @= state
    dut.in_   @= in_

    ref.sim_eval_combinational()
    dut.sim_eval_combinational()

    print_line_trace( dut, dut.state, dut.in_,
                      ">", dut.state_next, dut.out )

    assert ref.state_next == dut.state_next
    assert ref.out        == dut.out

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b0001, 0 ),
    ( 0b0001, 1 ),
    ( 0b0010, 0 ),
    ( 0b0010, 1 ),
    ( 0b0100, 0 ),
    ( 0b0100, 1 ),
    ( 0b1000, 0 ),
    ( 0b1000, 1 ),
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0b0000, 0 ),
    ( 0b0000, 1 ),
    # ( 0b0001, 0 ), valid
    # ( 0b0001, 1 ), valid

    # ( 0b0010, 0 ), valid
    # ( 0b0010, 1 ), valid
    ( 0b0011, 0 ),
    ( 0b0011, 1 ),

    # ( 0b0100, 0 ), valid
    # ( 0b0100, 1 ), valid
    ( 0b0101, 0 ),
    ( 0b0101, 1 ),

    ( 0b0110, 0 ),
    ( 0b0110, 1 ),
    ( 0b0111, 0 ),
    ( 0b0111, 1 ),

    # ( 0b1000, 0 ), valid
    # ( 0b1000, 1 ), valid
    ( 0b1001, 0 ),
    ( 0b1001, 1 ),

    ( 0b1010, 0 ),
    ( 0b1010, 1 ),
    ( 0b1011, 0 ),
    ( 0b1011, 1 ),

    ( 0b1100, 0 ),
    ( 0b1100, 1 ),
    ( 0b1101, 0 ),
    ( 0b1101, 1 ),

    ( 0b1110, 0 ),
    ( 0b1110, 1 ),
    ( 0b1111, 0 ),
    ( 0b1111, 1 ),
  ])

