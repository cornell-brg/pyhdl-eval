#=========================================================================
# pyhdl_eval.migen
#=========================================================================
# DSL support for Amaranth (https://github.com/amaranth-lang/amaranth).
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import importlib
import types
import amaranth
import amaranth.sim
import greenlet

from pyhdl_eval.cfg import InputPort, OutputPort
from pyhdl_eval.bits import Bits

class TopModuleAmaranth():

  def __init__( s, file_name, config ):

    # Dynamically load the source file

    loader = importlib.machinery.SourceFileLoader("TopModule",file_name)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    # Setup some members for use later on

    s.has_clk       = False
    s.has_reset     = False
    s.input_names   = []
    s.input_values  = {}
    s.output_names  = []
    s.output_values = {}
    s.ports_nbits   = {}
    for port in config.ports:
      name,type_ = port
      if isinstance( type_, InputPort ) and name != "clk":
        s.input_names.append( name )
        s.input_values[name] = 0
      elif isinstance( type_, OutputPort ):
        s.output_names.append( name )
        s.output_values[name] = 0
      s.ports_nbits[name] = type_.nbits()
      if name == "reset":
        s.has_reset = True
      if name == "clk":
        s.has_clk = True

    # Create a greenlet to enable stepping the simulator one cycle

    def step_inner():

      # Instantiate the top module (note that we instantiate the module
      # here to avoid UnusedElaboratable warnings when our random testing
      # runs tests with no test vectors)

      s.top = mod.TopModule( **config.parameters )

      if s.has_reset:
        s.reset_signal = amaranth.Signal()
        s.top = amaranth.ResetInserter( s.reset_signal )( s.top )

      # Infinite loop to drive the simulator

      def step_testbench():

        while True:

          # Write input values to input ports

          for name in s.input_names:
            if name == "reset":
              yield s.reset_signal.eq( s.input_values[name] )
            else:
              actual_port = getattr( s.top, name )
              yield actual_port.eq( s.input_values[name] )

          # Tick simulator one cycle (must tick simulator differently
          # depending if the dut is purely combinational or has a clock)

          if not s.has_clk:
            yield amaranth.sim.Settle()
          else:
            yield

          # Read output ports and save values

          for name in s.output_names:
            s.output_values[name] = yield getattr( s.top, name )

          # Switch back to the function that switched to this greenlet

          greenlet.getcurrent().parent.switch()

      sim = amaranth.sim.Simulator( s.top )

      if s.has_clk:
        sim.add_clock(1)
        sim.add_sync_process(step_testbench)
      else:
        sim.add_process(step_testbench)

      sim.run()

    s.step_greenlet = greenlet.greenlet( step_inner )

  def reset( s ):
    if s.has_reset:
      s.write( "reset", 1 )
      s.step_greenlet.switch()
      s.step_greenlet.switch()
      s.step_greenlet.switch()
      s.write( "reset", 0 )

  def write( s, port_name, value ):
    if isinstance( value, Bits ):
      s.input_values[port_name] = value.uint()
    else:
      nbits = s.ports_nbits[port_name]
      s.input_values[port_name] = Bits(nbits,value).uint()

  def read( s, port_name ):
    nbits = s.ports_nbits[port_name]
    if port_name in s.input_values:
      return Bits(nbits,s.input_values[port_name])
    else:
      return Bits(nbits,s.output_values[port_name])

  def tick_phase0( s ):
    s.step_greenlet.switch()

  def tick_phase1( s ):
    pass

  def cleanup( s ):
    pass

