#=========================================================================
# pyhdl_eval.verilog
#=========================================================================
# PyHDL-Eval support for Verilog. Uses PyMTL3 for Verilog importing.
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

import pathlib
import pymtl3
import pymtl3.passes.backends.verilog as pymtl3v

from pyhdl_eval.cfg  import InputPort, OutputPort
from pyhdl_eval.bits import Bits

class TopModuleVerilog():

  def __init__( s, file_name, config, ref=False ):

    # Create a VerilogPlaceholder class

    class TopModule( pymtl3v.VerilogPlaceholder, pymtl3.Component ):

      def construct( s ):

        # Handle parameters

        s.set_metadata( pymtl3v.VerilogPlaceholderPass.params, config.parameters )

        # Create ports

        for port in config.ports:
          name,type_ = port

          if isinstance( type_, InputPort ):
            if name != "clk" and name != "reset":
              setattr( s, name, pymtl3.InPort( type_.nbits() ) )

          elif isinstance( type_, OutputPort ):
            setattr( s, name, pymtl3.OutPort( type_.nbits() ) )

    # Append parameters as string to ensure filename is unique

    s.top = TopModule()

    vout_prob_name = pathlib.Path(file_name).stem
    for key,value in config.parameters.items():
      vout_prob_name += "_" + key + "_" + str(value)

    vout_file_name = vout_prob_name + "_translated.v"

    if ref:
      s.top.set_metadata( pymtl3v.VerilogPlaceholderPass.top_module, "RefModule" )

    s.top.set_metadata( pymtl3v.VerilogPlaceholderPass.src_file, file_name )
    s.top.set_metadata( pymtl3v.VerilogTranslationImportPass.enable, True )
    s.top.set_metadata( pymtl3v.VerilogTranslationPass.explicit_file_name, vout_file_name )
    s.top.set_metadata( pymtl3v.VerilogTranslationPass.explicit_module_name, vout_prob_name )
    s.top.apply( pymtl3v.VerilogPlaceholderPass() )
    s.top = pymtl3v.VerilogTranslationImportPass()( s.top )
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

