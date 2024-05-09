#=========================================================================
# Prob08p09_comb_fsm_6s2i2o_mo_dia_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct, print_line_trace

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.state      = InPort (3)
    s.in_        = InPort (2)
    s.state_next = OutPort(3)
    s.out        = OutPort(2)

    # State Encoding

    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5

    # State Transition Logic

    @update
    def transition():
      s.state_next @= 0
      if s.state == A :
        if   s.in_ == 0b00 : s.state_next @= A;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= E;
      elif s.state == B :
        if   s.in_ == 0b00 : s.state_next @= C;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= E;
      elif s.state == C :
        if   s.in_ == 0b00 : s.state_next @= A;
        elif s.in_ == 0b01 : s.state_next @= D;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= E;
      elif s.state == D :
        if   s.in_ == 0b00 : s.state_next @= C;
        elif s.in_ == 0b01 : s.state_next @= B;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= E;
      elif s.state == E :
        if   s.in_ == 0b00 : s.state_next @= F;
        elif s.in_ == 0b01 : s.state_next @= F;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= E;
      elif s.state == F :
        if   s.in_ == 0b00 : s.state_next @= A;
        elif s.in_ == 0b01 : s.state_next @= A;
        elif s.in_ == 0b10 : s.state_next @= A;
        else               : s.state_next @= A;

    # State Output Logic

    @update
    def output():
      if   s.state == A : s.out @= 0b00
      elif s.state == B : s.out @= 0b00
      elif s.state == C : s.out @= 0b00
      elif s.state == D : s.out @= 0b01
      elif s.state == E : s.out @= 0b10
      elif s.state == F : s.out @= 0b10
      else              : s.out @= 0b00

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.state      = InPort (3)
    s.in_        = InPort (2)
    s.state_next = OutPort(3)
    s.out        = OutPort(2)

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
# test_case_valid
#-------------------------------------------------------------------------

def test_case_valid( pytestconfig ):
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

    ( 4, 0b00 ),
    ( 4, 0b01 ),
    ( 4, 0b10 ),
    ( 4, 0b11 ),

    ( 5, 0b00 ),
    ( 5, 0b01 ),
    ( 5, 0b10 ),
    ( 5, 0b11 ),
  ])

#-------------------------------------------------------------------------
# test_case_invalid
#-------------------------------------------------------------------------

def test_case_invalid( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 6, 0b00 ),
    ( 6, 0b01 ),
    ( 6, 0b10 ),
    ( 6, 0b11 ),

    ( 7, 0b00 ),
    ( 7, 0b01 ),
    ( 7, 0b10 ),
    ( 7, 0b11 ),
  ])

