#=========================================================================
# pyhdl_eval.pyrtl
#=========================================================================
# DSL support for PyRTL (https://github.com/UCSBarchlab/PyRTL).
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import importlib
import types
import pyrtl

from pyhdl_eval.cfg import InputPort, OutputPort
from pyhdl_eval.bits import Bits

# We want to make sure all of the signals are in their own namespace and
# are not members of TopModulePyRTL, so we will add all of these signals
# to an instance of this special Signals class.

class Signals():
  pass

class TopModulePyRTL():

  def __init__( s, file_name, config ):

    loader = importlib.machinery.SourceFileLoader("TopModule",file_name)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    # Create pins to use as ports

    s.signals = Signals()
    for port in config.ports:
      name,type_ = port

      if isinstance( type_, InputPort ):
        if name != "clk":
          setattr( s.signals, name, pyrtl.Input( type_.nbits(), name ) )

      elif isinstance( type_, OutputPort ):
        setattr( s.signals, name, pyrtl.Output( type_.nbits(), name ) )

    # Collect input and output signals in lists

    input_signals  = []
    output_signals = []

    for port in config.ports:
      name,type_ = port

      if isinstance( type_, InputPort ):
        if name != "clk" and name != "reset":
          input_signals.append( getattr( s.signals, name ) )

      elif isinstance( type_, OutputPort ):
        output_signals.append( getattr( s.signals, name ) )

    # Instantiate the top module

    output_tmps = mod.TopModule( *input_signals, **config.parameters )

    # Connect up the output ports

    if not isinstance( output_tmps, tuple ):
      output_tmps = ( output_tmps, )

    for output_signal,output_tmp in zip(output_signals,output_tmps):
      output_signal <<= output_tmp

    # Create a simulator

    s.sim = pyrtl.Simulation()

    # Setup some members for use later on

    s.input_values = {}
    s.ports_nbits  = {}
    for port in config.ports:
      name,type_ = port
      s.ports_nbits[name] = type_.nbits()

  def reset( s ):
    pass

  def write( s, port_name, value ):
    if isinstance( value, Bits ):
      s.input_values[port_name] = value.uint()
    else:
      nbits = s.ports_nbits[port_name]
      s.input_values[port_name] = Bits(nbits,value).uint()

  def read( s, port_name ):
    nbits = len(getattr( s.signals, port_name ))
    return Bits(nbits,s.sim.inspect(port_name))

  def tick_phase0( s ):
    s.sim.step(s.input_values)

  def tick_phase1( s ):
    pass

  def cleanup( s ):
    pyrtl.reset_working_block()

