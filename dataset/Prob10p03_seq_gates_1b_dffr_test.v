//========================================================================
// Prob10p03_seq_gates_1b_dffr_test
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
  logic ref_module_d;
  logic ref_module_q;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .d     (ref_module_d),
    .q     (ref_module_q),
    .*
  );

  logic top_module_reset;
  logic top_module_d;
  logic top_module_q;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .d     (top_module_d),
    .q     (top_module_q),
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
    input logic reset_,
    input logic d
  );

    ref_module_reset = reset_;
    ref_module_d     = d;

    top_module_reset = reset_;
    top_module_d     = d;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_reset, top_module_d, top_module_q );

    `TEST_UTILS_CHECK_EQ( top_module_q, ref_module_q );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    //       rs d
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 0 );
    compare( 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_directed_reset
  //----------------------------------------------------------------------

  task test_case_2_directed_reset();
    $display( "\ntest_case_2_directed_reset" );
    t.reset_sequence();

    //       rs d
    compare( 0, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 0, 0 );
    compare( 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random_reset
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_random_reset();
    $display( "\ntest_case_3_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_directed_reset();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random_reset();

    $write("\n");
    $finish;
  end

endmodule

