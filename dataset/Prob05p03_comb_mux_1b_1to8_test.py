#=========================================================================
# Prob05p03_comb_mux_1b_1to8_test
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import *

from test_utils import construct

#-------------------------------------------------------------------------
# PyMTL Reference
#-------------------------------------------------------------------------

class RefModule( Component ):
  def construct( s ):
    s.in_  = InPort()
    s.sel  = InPort(3)
    s.out0 = OutPort()
    s.out1 = OutPort()
    s.out2 = OutPort()
    s.out3 = OutPort()
    s.out4 = OutPort()
    s.out5 = OutPort()
    s.out6 = OutPort()
    s.out7 = OutPort()

    @update
    def up():

      s.out0 @= 0
      s.out1 @= 0
      s.out2 @= 0
      s.out3 @= 0
      s.out4 @= 0
      s.out5 @= 0
      s.out6 @= 0
      s.out7 @= 0

      if   s.sel == 0: s.out0 @= s.in_
      elif s.sel == 1: s.out1 @= s.in_
      elif s.sel == 2: s.out2 @= s.in_
      elif s.sel == 3: s.out3 @= s.in_
      elif s.sel == 4: s.out4 @= s.in_
      elif s.sel == 5: s.out5 @= s.in_
      elif s.sel == 6: s.out6 @= s.in_
      elif s.sel == 7: s.out7 @= s.in_

#-------------------------------------------------------------------------
# Verilog Wrapper
#-------------------------------------------------------------------------

class TopModule( VerilogPlaceholder, Component ):
  def construct( s ):
    s.in_  = InPort()
    s.sel  = InPort(3)
    s.out0 = OutPort()
    s.out1 = OutPort()
    s.out2 = OutPort()
    s.out3 = OutPort()
    s.out4 = OutPort()
    s.out5 = OutPort()
    s.out6 = OutPort()
    s.out7 = OutPort()

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------

def run_sim( pytestconfig, test_vectors ):

  ref,dut = construct( pytestconfig, __file__, RefModule, TopModule )

  for test_vector in test_vectors:

    in_,sel = test_vector

    ref.in_ @= in_
    ref.sel @= sel

    dut.in_ @= in_
    dut.sel @= sel

    ref.sim_tick()
    dut.sim_tick()

    assert ref.out0 == dut.out0
    assert ref.out1 == dut.out1
    assert ref.out2 == dut.out2
    assert ref.out3 == dut.out3
    assert ref.out4 == dut.out4
    assert ref.out5 == dut.out5
    assert ref.out6 == dut.out6
    assert ref.out7 == dut.out7

#-------------------------------------------------------------------------
# test_case_directed
#-------------------------------------------------------------------------

def test_case_directed( pytestconfig ):
  run_sim( pytestconfig,
  [
    (0,0),
    (1,0),
    (0,1),
    (1,1),
    (0,2),
    (1,2),
    (0,3),
    (1,3),

    (0,4),
    (1,4),
    (0,5),
    (1,5),
    (0,6),
    (1,6),
    (0,7),
    (1,7),
  ])

