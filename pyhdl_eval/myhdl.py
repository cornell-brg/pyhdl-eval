#=========================================================================
# pyhdl_eval.myhdl
#=========================================================================
# PyHDL-Eval support for MyHDL.
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import importlib
import types
import myhdl

from pyhdl_eval.bits import Bits

# We want to make sure all of the signals are in their own namespace and
# are not members of TopModulePyRTL, so we will add all of these signals
# to an instance of this special Signals class.

class Signals():
  pass

class TopModuleMyHDL():

  def __init__( s, file_name, config ):

    loader = importlib.machinery.SourceFileLoader("TopModule",file_name)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    # Create signals to use as ports

    s.has_clk   = False
    s.has_reset = False

    s.signals = Signals()
    for port in config.ports:
      name,type_ = port
      nbits = type_.nbits()

      if name == "reset":
        s.has_reset = True
        setattr( s.signals, name,
                 myhdl.ResetSignal(0,active=1,isasync=False) )
      else:
        setattr( s.signals, name,
                 myhdl.Signal( myhdl.modbv(0,min=0,max=2**nbits) ) )

      if name == "clk":
        s.has_clk = True

    # Collect signals into a list

    signal_list = []
    for port in config.ports:
      name,type_ = port
      signal_list.append( getattr( s.signals, name ) )

    # Create dummy clk and dummy reset if necessary

    if not s.has_clk:
      s.signals.clk = myhdl.Signal(bool(0))

    # Create a top level wrapper for hardware module

    @myhdl.block
    def test_top():

      top = mod.TopModule( *signal_list, **config.parameters )

      @myhdl.always(myhdl.delay(5))
      def clkgen():
        s.signals.clk.next = not s.signals.clk

      return top, clkgen

    s.sim = test_top()

    # We start with a 6 unit delay since it seems like MyHDL wants the
    # simulation to start with the second half of a clock cycle.

    s.sim.run_sim( 6, quiet=True )

  def reset( s ):
    if s.has_reset:
      s.signals.reset.next = 1
      s.sim.run_sim( 30, quiet=True )
      s.signals.reset.next = 0

  def write( s, port_name, value ):
    if isinstance( value, Bits ):
      value = value.uint()
    port = getattr( s.signals, port_name )
    port.next = value

  def read( s, port_name ):
    myhdl_modbv = getattr( s.signals, port_name )
    nbits = len(myhdl_modbv)
    return Bits(nbits,int(myhdl_modbv))

  def tick_phase0( s ):
    s.sim.run_sim( 8, quiet=True )

  def tick_phase1( s ):
    s.sim.run_sim( 2, quiet=True )

  def cleanup( s ):
    s.sim.quit_sim()

