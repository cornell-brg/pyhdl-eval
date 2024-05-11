#=========================================================================
# Prob08p04_comb_fsm_4s1i2o_mo_tbl_test
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
    s.in_        = InPort ()
    s.state_next = OutPort(2)
    s.out0       = OutPort()
    s.out1       = OutPort()

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
      if   s.state == A : s.out0 @= 0; s.out1 @= 0;
      elif s.state == B : s.out0 @= 0; s.out1 @= 1;
      elif s.state == C : s.out0 @= 0; s.out1 @= 1;
      elif s.state == D : s.out0 @= 1; s.out1 @= 0;
      else              : s.out0 @= 0; s.out1 @= 0;

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.state      = InPort (2)
    s.in_        = InPort ()
    s.state_next = OutPort(2)
    s.out0       = OutPort()
    s.out1       = OutPort()

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
                      ">", dut.state_next, dut.out0, dut.out1 )

    assert ref.state_next == dut.state_next
    assert ref.out0       == dut.out0
    assert ref.out1       == dut.out1

    ref.sim_tick()
    dut.sim_tick()

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    ( 0, 0 ),
    ( 0, 1 ),
    ( 1, 0 ),
    ( 1, 1 ),
    ( 2, 0 ),
    ( 2, 1 ),
    ( 3, 0 ),
    ( 3, 1 ),
  ])

