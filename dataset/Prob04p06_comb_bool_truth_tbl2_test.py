#=========================================================================
# Prob04p06_comb_bool_truth_tbl2_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.c = InPort()
    s.d = InPort()
    s.f = OutPort()

    @update
    def up():
      temp = concat(s.a,s.b,s.c,s.d)
      if   temp == 0b0000: s.f @= 1
      elif temp == 0b0001: s.f @= 1
      elif temp == 0b0010: s.f @= 0
      elif temp == 0b0011: s.f @= 0
      elif temp == 0b0100: s.f @= 1
      elif temp == 0b0101: s.f @= 1
      elif temp == 0b0110: s.f @= 0
      elif temp == 0b0111: s.f @= 0
      elif temp == 0b1000: s.f @= 1
      elif temp == 0b1001: s.f @= 0
      elif temp == 0b1010: s.f @= 1
      elif temp == 0b1011: s.f @= 0
      elif temp == 0b1100: s.f @= 0
      elif temp == 0b1101: s.f @= 1
      elif temp == 0b1110: s.f @= 0
      elif temp == 0b1111: s.f @= 1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.c = InPort()
    s.d = InPort()
    s.f = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    a,b,c,d = test_vector

    ref.a @= a
    ref.b @= b
    ref.c @= c
    ref.d @= d

    dut.a @= a
    dut.b @= b
    dut.c @= c
    dut.d @= d

    ref.sim_tick()
    dut.sim_tick()

    assert ref.f == dut.f

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig, [

    (0,0,0,0),
    (0,0,0,1),
    (0,0,1,0),
    (0,0,1,1),
    (0,1,0,0),
    (0,1,0,1),
    (0,1,1,0),
    (0,1,1,1),

    (1,0,0,0),
    (1,0,0,1),
    (1,0,1,0),
    (1,0,1,1),
    (1,1,0,0),
    (1,1,0,1),
    (1,1,1,0),
    (1,1,1,1),

  ] )

