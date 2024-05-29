//========================================================================
// Prob16p12_seq_fsm_stop_light_test
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

  logic ref_module_reset;
  logic ref_module_starting_yellow;
  logic ref_module_change;
  logic ref_module_green_on;
  logic ref_module_yellow_on;
  logic ref_module_red_on;

  RefModule ref_module
  (
    .reset           (reset || ref_module_reset),
    .starting_yellow (ref_module_starting_yellow),
    .change          (ref_module_change),
    .green_on        (ref_module_green_on),
    .yellow_on       (ref_module_yellow_on),
    .red_on          (ref_module_red_on),
    .*
  );

  logic top_module_reset;
  logic top_module_starting_yellow;
  logic top_module_change;
  logic top_module_green_on;
  logic top_module_yellow_on;
  logic top_module_red_on;

  TopModule top_module
  (
    .reset           (reset || top_module_reset),
    .starting_yellow (top_module_starting_yellow),
    .change          (top_module_change),
    .green_on        (top_module_green_on),
    .yellow_on       (top_module_yellow_on),
    .red_on          (top_module_red_on),
    .*
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic reset,
    input logic starting_yellow,
    input logic change
  );

    ref_module_reset           = reset;
    ref_module_starting_yellow = starting_yellow;
    ref_module_change          = change;

    top_module_reset           = reset;
    top_module_starting_yellow = starting_yellow;
    top_module_change          = change;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x %x %x", t.cycles,
                top_module_reset,     top_module_starting_yellow,
                top_module_change,    top_module_green_on,
                top_module_yellow_on, top_module_red_on );

    `TEST_UTILS_CHECK_EQ( top_module_green_on,  ref_module_green_on  );
    `TEST_UTILS_CHECK_EQ( top_module_yellow_on, ref_module_yellow_on );
    `TEST_UTILS_CHECK_EQ( top_module_red_on,    ref_module_red_on    );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_startyellow0
  //----------------------------------------------------------------------

  task test_case_1_startyellow0();
    $display( "\ntest_case_1_startyellow0" );
    t.reset_sequence();

    //       rs sy ch
    compare( 0, 0, 0 ); // G  -> G
    compare( 0, 0, 1 ); // G  -> Y1
    compare( 0, 0, 0 ); // Y1 -> Y1
    compare( 0, 0, 1 ); // Y1 -> R
    compare( 0, 0, 0 ); // R  -> R
    compare( 0, 0, 1 ); // R  -> G
    compare( 0, 0, 0 ); // G  -> G

  endtask

  //----------------------------------------------------------------------
  // test_case_2_startyellow1
  //----------------------------------------------------------------------

  task test_case_2_startyellow1();
    $display( "\ntest_case_2_startyellow1" );
    t.reset_sequence();

    //       rs sy ch
    compare( 0, 1, 0 ); // G  -> G
    compare( 0, 1, 1 ); // G  -> Y1
    compare( 0, 1, 0 ); // Y1 -> Y1
    compare( 0, 1, 1 ); // Y1 -> R
    compare( 0, 1, 0 ); // R  -> R
    compare( 0, 1, 1 ); // R  -> Y2
    compare( 0, 1, 0 ); // Y2 -> Y2
    compare( 0, 1, 1 ); // Y2 -> G
    compare( 0, 1, 0 ); // G  -> G

  endtask

  //----------------------------------------------------------------------
  // test_case_3_startyellow_switch
  //----------------------------------------------------------------------

  task test_case_3_startyellow_switch();
    $display( "\ntest_case_3_startyellow_switch" );
    t.reset_sequence();

    //       rs sy ch
    compare( 0, 0, 0 ); // G  -> G
    compare( 0, 0, 1 ); // G  -> Y1
    compare( 0, 0, 0 ); // Y1 -> Y1
    compare( 0, 0, 1 ); // Y1 -> R
    compare( 0, 0, 0 ); // R  -> R
    compare( 0, 0, 1 ); // R  -> G
    compare( 0, 0, 0 ); // G  -> G

    compare( 0, 1, 0 ); // G  -> G

    compare( 0, 1, 0 ); // G  -> G
    compare( 0, 1, 1 ); // G  -> Y1
    compare( 0, 1, 0 ); // Y1 -> Y1
    compare( 0, 1, 1 ); // Y1 -> R
    compare( 0, 1, 0 ); // R  -> R
    compare( 0, 1, 1 ); // R  -> Y2
    compare( 0, 1, 0 ); // Y2 -> Y2
    compare( 0, 1, 1 ); // Y2 -> G
    compare( 0, 1, 0 ); // G  -> G

  endtask

  //----------------------------------------------------------------------
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs sy ch
    compare( 0, 0, 0 ); // G  -> G
    compare( 0, 0, 1 ); // G  -> Y1
    compare( 0, 0, 1 ); // Y1 -> R
    compare( 0, 0, 1 ); // R  -> G
    compare( 0, 0, 1 ); // G  -> Y1

    compare( 1, 1, 0 );
    compare( 1, 1, 0 );
    compare( 1, 1, 0 );

    compare( 0, 1, 0 ); // G  -> G
    compare( 0, 1, 1 ); // G  -> Y1
    compare( 0, 1, 1 ); // Y1 -> R
    compare( 0, 1, 1 ); // R  -> Y2
    compare( 0, 1, 1 ); // Y2 -> G
    compare( 0, 1, 1 ); // G  -> Y1

    compare( 1, 0, 0 );
    compare( 1, 0, 0 );
    compare( 1, 0, 0 );

    compare( 0, 0, 0 ); // G  -> G
    compare( 0, 0, 1 ); // G  -> Y1
    compare( 0, 0, 1 ); // Y1 -> R
    compare( 0, 0, 1 ); // R  -> G
    compare( 0, 0, 1 ); // G  -> Y1

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_startyellow0();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_startyellow1();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_startyellow_switch();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();

    $write("\n");
    $finish;
  end

endmodule

