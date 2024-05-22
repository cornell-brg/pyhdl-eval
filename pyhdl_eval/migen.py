#=========================================================================
# pyhdl_eval.migen
#=========================================================================
# DSL support for Migen (https://github.com/m-labs/migen).
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import importlib
import types
import migen
import greenlet

from pyhdl_eval.cfg import InputPort, OutputPort
from pyhdl_eval.bits import Bits

class TopModuleMigen():

  def __init__( s, file_name, config ):

    # Dynamically load the source file

    loader = importlib.machinery.SourceFileLoader("TopModule",file_name)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    # Instantiate the top module

    s.top = mod.TopModule( **config.parameters )

    # Setup some members for use later on

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

    # Create a greenlet to enable stepping the simulator one cycle

    def step_inner():

      def step_testbench():

        while True:

          # Write input values to input ports

          for name in s.input_names:
            actual_port = getattr( s.top, name )
            yield actual_port.eq( s.input_values[name] )

          # Tick simulator one cycle

          yield

          # Read output ports and save values

          for name in s.output_names:
            s.output_values[name] = yield getattr( s.top, name )

          # Switch back to the function that switched to this greenlet

          greenlet.getcurrent().parent.switch()

      migen.run_simulation( s.top, step_testbench() )

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

