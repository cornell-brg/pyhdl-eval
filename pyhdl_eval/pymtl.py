#=========================================================================
# pyhdl_eval.pymtl
#=========================================================================
# DSL support for PyMTL3 (https://github.com/pymtl/pymtl3).
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import importlib
import types
import pymtl3

from pyhdl_eval.bits import Bits

class TopModulePyMTL():

  def __init__( s, file_name, config ):

    # Dynamically load the source file

    loader = importlib.machinery.SourceFileLoader("TopModule",file_name)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)

    # Instantiate the top module

    s.top = mod.TopModule( **config.parameters )
    s.top.apply( pymtl3.DefaultPassGroup() )

    # Save the nbits for each port

    s.ports_nbits  = {}
    for port in config.ports:
      name,type_ = port
      s.ports_nbits[name] = type_.nbits()

  def reset( s ):
    s.top.sim_reset()

  def write( s, port_name, value ):
    if isinstance( value, Bits ):
      value = value.uint()
    port = getattr( s.top, port_name )
    port @= value

  def read( s, port_name ):
    nbits = s.ports_nbits[port_name]
    return Bits( nbits, getattr( s.top, port_name ).uint() )

  def tick_phase0( s ):
    s.top.sim_eval_combinational()

  def tick_phase1( s ):
    s.top.sim_tick()

  def cleanup( s ):
    pass

