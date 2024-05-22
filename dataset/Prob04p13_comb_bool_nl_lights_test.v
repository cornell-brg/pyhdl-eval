//========================================================================
// Prob04p13_comb_bool_nl_lights_test
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

  logic ref_module_dark;
  logic ref_module_movement;
  logic ref_module_force_on;
  logic ref_module_turn_on_lights;

  RefModule ref_module
  (
    .dark           (ref_module_dark),
    .movement       (ref_module_movement),
    .force_on       (ref_module_force_on),
    .turn_on_lights (ref_module_turn_on_lights)
  );

  logic top_module_dark;
  logic top_module_movement;
  logic top_module_force_on;
  logic top_module_turn_on_lights;

  TopModule top_module
  (
    .dark           (top_module_dark),
    .movement       (top_module_movement),
    .force_on       (top_module_force_on),
    .turn_on_lights (top_module_turn_on_lights)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic dark,
    input logic movement,
    input logic force_on
  );

    ref_module_dark     = dark;
    ref_module_movement = movement;
    ref_module_force_on = force_on;

    top_module_dark     = dark;
    top_module_movement = movement;
    top_module_force_on = force_on;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_dark, top_module_movement,
                top_module_force_on,
                top_module_turn_on_lights );

    `TEST_UTILS_CHECK_EQ( top_module_turn_on_lights,
                          ref_module_turn_on_lights );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0,0);
    compare(0,0,1);
    compare(0,1,0);
    compare(0,1,1);
    compare(1,0,0);
    compare(1,0,1);
    compare(1,1,0);
    compare(1,1,1);

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

