//========================================================================
// Prob04p15_comb_bool_nl_thermostat_test
//========================================================================
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024

`include "test_utils.v"

module Top();

  //----------------------------------------------------------------------
  // Setup
  //----------------------------------------------------------------------

  logic clk;
  logic reset;

  TestUtils t( .* );

  //----------------------------------------------------------------------
  // Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic ref_module_mode;
  logic ref_module_too_cold;
  logic ref_module_too_hot;
  logic ref_module_fan_on;
  logic ref_module_heater;
  logic ref_module_aircon;
  logic ref_module_fan;

  RefModule ref_module
  (
    .mode     (ref_module_mode),
    .too_cold (ref_module_too_cold),
    .too_hot  (ref_module_too_hot),
    .fan_on   (ref_module_fan_on),
    .heater   (ref_module_heater),
    .aircon   (ref_module_aircon),
    .fan      (ref_module_fan)
  );

  logic top_module_mode;
  logic top_module_too_cold;
  logic top_module_too_hot;
  logic top_module_fan_on;
  logic top_module_heater;
  logic top_module_aircon;
  logic top_module_fan;

  TopModule top_module
  (
    .mode     (top_module_mode),
    .too_cold (top_module_too_cold),
    .too_hot  (top_module_too_hot),
    .fan_on   (top_module_fan_on),
    .heater   (top_module_heater),
    .aircon   (top_module_aircon),
    .fan      (top_module_fan)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic mode,
    input logic too_cold,
    input logic too_hot,
    input logic fan_on
  );

    ref_module_mode     = mode;
    ref_module_too_cold = too_cold;
    ref_module_too_hot  = too_hot;
    ref_module_fan_on   = fan_on;

    top_module_mode     = mode;
    top_module_too_cold = too_cold;
    top_module_too_hot  = too_hot;
    top_module_fan_on   = fan_on;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x %x %x", t.cycles,
                top_module_mode,    top_module_too_cold,
                top_module_too_hot, top_module_fan_on,
                top_module_heater,  top_module_aircon,
                top_module_fan );

    `TEST_UTILS_CHECK_EQ( top_module_heater, ref_module_heater );
    `TEST_UTILS_CHECK_EQ( top_module_aircon, ref_module_aircon );
    `TEST_UTILS_CHECK_EQ( top_module_fan,    ref_module_fan    );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0,0,0);
    compare(0,0,0,1);
    compare(0,0,1,0);
    compare(0,0,1,1);
    compare(0,1,0,0);
    compare(0,1,0,1);
    compare(0,1,1,0);
    compare(0,1,1,1);

    compare(1,0,0,0);
    compare(1,0,0,1);
    compare(1,0,1,0);
    compare(1,0,1,1);
    compare(1,1,0,0);
    compare(1,1,0,1);
    compare(1,1,1,0);
    compare(1,1,1,1);

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();

    $write("\n");
    $finish;
  end

endmodule

