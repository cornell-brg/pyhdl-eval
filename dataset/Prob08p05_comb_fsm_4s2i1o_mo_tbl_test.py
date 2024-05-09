#=========================================================================
# Prob08p05_comb_fsm_4s2i1o_mo_tbl_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.state      = InPort (2)
    s.in_        = InPort (2)
    s.state_next = OutPort(2)
    s.out        = OutPort()

    # State Encoding

    A = 0
    B = 1
    C = 2
    D = 3

    # State Transition Logic

    @update
    def transition():
      s.state_next @= 0
      if s.state == A :
        if   s.in_ == 0b00 : s.state_next @= A;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= D;
      elif s.state == B :
        if   s.in_ == 0b00 : s.state_next @= C;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= D;
      elif s.state == C :
        if   s.in_ == 0b00 : s.state_next @= A;
        elif s.in_ == 0b01 : s.state_next @= D;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= D;
      elif s.state == D :
        if   s.in_ == 0b00 : s.state_next @= C;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= D;

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
    s.state      = InPort (2)
    s.in_        = InPort (2)
    s.state_next = OutPort(2)
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

    ref.sim_tick()
    dut.sim_tick()

    print_line_trace( dut, dut.state, dut.in_,
                      ">", dut.state_next, dut.out )

    assert ref.state_next == dut.state_next
    assert ref.out        == dut.out

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0b00 ),
    ( 0, 0b01 ),
    ( 0, 0b10 ),
    ( 0, 0b11 ),

    ( 1, 0b00 ),
    ( 1, 0b01 ),
    ( 1, 0b10 ),
    ( 1, 0b11 ),

    ( 2, 0b00 ),
    ( 2, 0b01 ),
    ( 2, 0b10 ),
    ( 2, 0b11 ),

    ( 3, 0b00 ),
    ( 3, 0b01 ),
    ( 3, 0b10 ),
    ( 3, 0b11 ),
  ])

