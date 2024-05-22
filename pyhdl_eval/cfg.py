#=========================================================================
# pyhdl_eval.cfg
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

from dataclasses import dataclass, field
from enum import Enum

# Interface Configuration

class Port():
  pass

class InputPort(Port):
  def __init__( s, nbits ):
    s._nbits = nbits
  def nbits( s ):
    return s._nbits

class OutputPort(Port):
  def __init__( s, nbits ):
    s._nbits = nbits
  def nbits( s ):
    return s._nbits

# Trace Configuration

class TraceFormat(Enum):
  HEX  = 1
  BIN  = 2
  INT  = 3
  UINT = 4

# Config Dataclass

@dataclass
class Config:
  parameters        : list[ tuple[str,int]  ] = field(default_factory=dict)
  ports             : list[ tuple[str,Port] ] = field(default_factory=list)
  trace_format      : TraceFormat             = TraceFormat.HEX
  dead_cycles       : int                     = 0
  dead_cycle_inputs : int                     = None

