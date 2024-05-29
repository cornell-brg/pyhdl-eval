#=========================================================================
# pyhdl_eval.core
#=========================================================================
# Core of PyHDL-Eval framework including a common TestHarness and run_sim
# function. The run_sim function always uses a Verilog implementation as
# the reference; the dut can be implemented in Verilog or any of several
# Python-based DSLs. The run_sim function includes the following
# simulation loop:
#
#   reset simulator
#   for test_vector in test_vectors:
#     write input ports with test vector data
#     tick phase0
#     output trace string
#     check output ports match between ref and dut
#     tick phase1
#
# The run_sim function is designed to work with any DSL that implements a
# class with the following Python API:
#
#   __inst__( s, file_name, config )
#
#     Constructor which should import the source file with the given
#     file_name and then create any wrappers or simulators necessary to
#     implement the remaining six methods. The config argument is an
#     instance of the Config dataclass in pyhd_eval.cfg and includes a
#     specification of the module's ports, parameters, and other
#     configuration information.
#
#   reset(s)
#
#     Reset the simulation.
#
#   write( s, port_name, value )
#
#     Write the input port with the given port_name. The given value can
#     either bit a Bits object or a regular Python int.
#
#   read( s, port_name )
#
#     Read the input or output port with the given port_name and return a
#     Bits object.
#
#   tick_phase0( s )
#
#     Tick the simulator. Phase 0 occurs after we write the inputs but
#     before we read and check the outputs. Since all problems in the
#     benchmark use positive edge triggered logic, phase0 can be viewed
#     as the negative edge of the clock.
#
#   tick_phase1( s )
#
#     Tick the simulator. Phase 1 occurs after we output a trace string
#     and check all output ports. Phase 1 can be viewed as the positive
#     edge of the clock.
#
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024
#

from pyhdl_eval.cfg      import InputPort, OutputPort, TraceFormat
from pyhdl_eval.verilog  import TopModuleVerilog
from pyhdl_eval.pymtl    import TopModulePyMTL
from pyhdl_eval.pyrtl    import TopModulePyRTL
from pyhdl_eval.myhdl    import TopModuleMyHDL
from pyhdl_eval.migen    import TopModuleMigen
from pyhdl_eval.amaranth import TopModuleAmaranth

#-------------------------------------------------------------------------
# Python-Embedded DSLs
#-------------------------------------------------------------------------

dsls = {
  "verilog"  : TopModuleVerilog,
  "pymtl"    : TopModulePyMTL,
  "pyrtl"    : TopModulePyRTL,
  "myhdl"    : TopModuleMyHDL,
  "migen"    : TopModuleMigen,
  "amaranth" : TopModuleAmaranth,
}

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

class TestHarness():

  def __init__( s, ref, dut ):
    s.ref = ref
    s.dut = dut
    s.cycle_count = 0

  def write( s, port_name, value ):
    s.ref.write( port_name, value )
    s.dut.write( port_name, value )

  def tick_phase0( s ):
    s.ref.tick_phase0()
    s.dut.tick_phase0()

  def tick_phase1( s ):
    s.ref.tick_phase1()
    s.dut.tick_phase1()
    s.cycle_count += 1

  def check( s, port_name ):
    assert s.ref.read( port_name ) == s.dut.read( port_name ), \
      f"Port named '{port_name}' does not match between ref and dut"

  def reset( s ):
    print("")
    s.cycle_count = 0
    s.ref.reset()
    s.dut.reset()

  def cleanup( s ):
    s.ref.cleanup()
    s.dut.cleanup()

  def get_cycle_count( s) :
    return s.cycle_count

  def __enter__( s ):
    return s

  def __exit__( s, type, value, traceback ):
    s.ref.cleanup()
    s.dut.cleanup()

#-------------------------------------------------------------------------
# print_with_trace_format
#-------------------------------------------------------------------------

def print_with_trace_format( value, trace_format ):

  if trace_format == TraceFormat.HEX:
    print( value.hex(), end=" " )

  elif trace_format == TraceFormat.BIN:
    print( value.bin(), end=" " )

  elif trace_format == TraceFormat.INT:
    print( value.int_str(), end=" " )

  elif trace_format == TraceFormat.UINT:
    print( value.uint_str(), end=" " )

#-------------------------------------------------------------------------
# run_sim
#-------------------------------------------------------------------------
# First argument is either a string indicating which dsl to use for the
# dut, or a pytestconfig object.

def run_sim( dslstr_or_pytestconfig, script_file_name, config,
             test_vectors=None ):

  # Reference is always the Verilog file next to the test script

  assert script_file_name.endswith("_test.py")
  script_base_name = script_file_name[:-8]
  ref_file_name = script_base_name + "_ref.v"

  ref = TopModuleVerilog( ref_file_name, config, ref=True )

  # If the first argument is a string, then the dsl source file is next
  # to the test script with the dsl as a suffix ...

  if isinstance( dslstr_or_pytestconfig, str ):

    dslstr = dslstr_or_pytestconfig
    suffix = ".py" if dslstr != "verilog" else ".v"
    dut_file_name = f"{script_base_name}_{dslstr}{suffix}"
    TopModuleDSL = dsls[dslstr]

    dut = TopModuleDSL( dut_file_name, config )

  # ... else the first argument is a pytestconfig object. Iterate through
  # all dsls to see if the corresponding command line option is set. By
  # default just use the reference verilog as the dut.

  else:

    dsl_found = False
    pytestconfig = dslstr_or_pytestconfig
    for dsl in dsls:
      if pytestconfig.getoption(dsl):

        dsl_found = True
        dut_file_name = pytestconfig.getoption(dsl)
        TopModuleDSL = dsls[dsl]

        dut = TopModuleDSL( dut_file_name, config )

    if not dsl_found:
      dut = TopModuleVerilog( ref_file_name, config, ref=True )

  # If test_vectors is empty that means we are testing a module with no
  # inputs. We still need to tick the module for a few cycles, so we
  # create a test_vectors with None entries and then handle this
  # specially in the simulation loop.

  if test_vectors == None:
    test_vectors = [ None, None, None ]

  # Create list of input and output port names

  input_port_names  = []
  output_port_names = []
  for port in config.ports:
    name,type_ = port
    if isinstance( type_, InputPort ):
      if name != "clk":
        input_port_names.append( name )
    elif isinstance( type_, OutputPort ):
      output_port_names.append( name )

  # Simulation loop

  with TestHarness( ref, dut ) as th:

    # Add "dead cycles" (i.e., cycles where outputs are not checked) at
    # the beginning of the simulation.

    ninputs = len(input_port_names)
    if not config.dead_cycle_inputs:
      test_vectors = [ (0,)*ninputs ]*config.dead_cycles + test_vectors
    elif not isinstance( config.dead_cycle_inputs, list ):
      inputs = config.dead_cycle_inputs
      test_vectors = [ inputs ]*config.dead_cycles + test_vectors
    else:
      test_vectors = config.dead_cycle_inputs + test_vectors

    # Reset the test harness

    th.reset()

    # Iterate through the test vectors

    for i,test_vector in enumerate(test_vectors):

      # Write input ports

      if test_vector != None:

        if not isinstance( test_vector, tuple ):
          test_vector = ( test_vector, )

        for name,value in zip( input_port_names, test_vector ):
          th.write( name, value )

      # Tick phase 0

      th.tick_phase0()

      # Tracing

      print(f"{th.get_cycle_count():3}:",end=" ")

      for name in input_port_names:
        value = th.dut.read( name )
        print_with_trace_format( value, config.trace_format )

      print( ">", end=" " )

      for name in output_port_names:
        value = th.dut.read( name )
        print_with_trace_format( value, config.trace_format )

      if i < config.dead_cycles:
        print( "*", end="" )

      print( "" )

      # Check outputs

      if i >= config.dead_cycles:
        for name in output_port_names:
          th.check( name )

      th.tick_phase1()

