//========================================================================
// Prob04p14_comb_bool_nl_ringer_test
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

  logic ref_module_vibrate_mode;
  logic ref_module_ring;
  logic ref_module_turn_on_ringer;
  logic ref_module_turn_on_motor;

  RefModule ref_module
  (
    .vibrate_mode    (ref_module_vibrate_mode),
    .ring            (ref_module_ring),
    .turn_on_ringer  (ref_module_turn_on_ringer),
    .turn_on_motor   (ref_module_turn_on_motor)
  );

  logic top_module_vibrate_mode;
  logic top_module_ring;
  logic top_module_turn_on_ringer;
  logic top_module_turn_on_motor;

  TopModule top_module
  (
    .vibrate_mode    (top_module_vibrate_mode),
    .ring            (top_module_ring),
    .turn_on_ringer  (top_module_turn_on_ringer),
    .turn_on_motor   (top_module_turn_on_motor)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic vibrate_mode,
    input logic ring
  );

    ref_module_vibrate_mode = vibrate_mode;
    ref_module_ring         = ring;

    top_module_vibrate_mode = vibrate_mode;
    top_module_ring         = ring;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x", t.cycles,
                top_module_vibrate_mode,   top_module_ring,
                top_module_turn_on_ringer, top_module_turn_on_motor );

    `TEST_UTILS_CHECK_EQ( top_module_turn_on_ringer, ref_module_turn_on_ringer );
    `TEST_UTILS_CHECK_EQ( top_module_turn_on_motor,  ref_module_turn_on_motor  );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0);
    compare(0,1);
    compare(1,0);
    compare(1,1);

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
