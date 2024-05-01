#=========================================================================
# Prob04p11_comb_bool_waveform1_test
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
    s.f = OutPort()

    @update
    def up():
      temp = concat(s.a,s.b,s.c)
      if   temp == 0b000: s.f @= 1
      elif temp == 0b001: s.f @= 1
      elif temp == 0b010: s.f @= 1
      elif temp == 0b011: s.f @= 0
      elif temp == 0b100: s.f @= 1
      elif temp == 0b101: s.f @= 0
      elif temp == 0b110: s.f @= 0
      elif temp == 0b111: s.f @= 1

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.a = InPort()
    s.b = InPort()
    s.c = InPort()
    s.f = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    a,b,c = test_vector

    ref.a @= a
    ref.b @= b
    ref.c @= c

    dut.a @= a
    dut.b @= b
    dut.c @= c

    ref.sim_tick()
    dut.sim_tick()

    assert ref.f == dut.f

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0,0),
    (0,0,1),
    (0,1,0),
    (0,1,1),
    (1,0,0),
    (1,0,1),
    (1,1,0),
    (1,1,1),
  ])

