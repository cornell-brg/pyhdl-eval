//========================================================================
// Prob07p14_comb_arith_8b_scmp_test
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

  logic [ 7:0] ref_module_in0;
  logic [ 7:0] ref_module_in1;
  logic        ref_module_lt;
  logic        ref_module_eq;
  logic        ref_module_gt;

  RefModule ref_module
  (
    .in0 (ref_module_in0),
    .in1 (ref_module_in1),
    .lt  (ref_module_lt),
    .eq  (ref_module_eq),
    .gt  (ref_module_gt)
  );

  logic [ 7:0] top_module_in0;
  logic [ 7:0] top_module_in1;
  logic        top_module_lt;
  logic        top_module_eq;
  logic        top_module_gt;

  TopModule top_module
  (
    .in0 (top_module_in0),
    .in1 (top_module_in1),
    .lt  (top_module_lt),
    .eq  (top_module_eq),
    .gt  (top_module_gt)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [7:0] in0,
    input logic [7:0] in1
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;

    top_module_in0 = in0;
    top_module_in1 = in1;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_lt, top_module_eq, top_module_gt );

    `TEST_UTILS_CHECK_EQ( top_module_lt, ref_module_lt );
    `TEST_UTILS_CHECK_EQ( top_module_eq, ref_module_eq );
    `TEST_UTILS_CHECK_EQ( top_module_gt, ref_module_gt );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_lt_pos
  //----------------------------------------------------------------------

  task test_case_1_lt_pos();
    $display( "\ntest_case_1_lt_pos" );
    t.reset_sequence();

    compare(   0,   1 );
    compare(   1,   2 );
    compare(   3,   9 );
    compare(  13,  42 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_lt_neg
  //----------------------------------------------------------------------

  task test_case_2_lt_neg();
    $display( "\ntest_case_2_lt_neg" );
    t.reset_sequence();

    compare(    0,    1 );
    compare(    1,    2 );
    compare(    3,    9 );
    compare(   13,   42 );

    compare(   -1,    0 );
    compare(   -1,    1 );
    compare(   -1,    2 );
    compare( -128,    0 );
    compare( -128,    1 );
    compare( -128,    2 );

    compare(   -5,    0 );
    compare(   -5,   -1 );
    compare(   -5,   -2 );
    compare( -128, -100 );
    compare( -128, -127 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_eq
  //----------------------------------------------------------------------

  task test_case_3_eq();
    $display( "\ntest_case_3_eq" );
    t.reset_sequence();

    compare(   0,   0 );
    compare(  16,  16 );
    compare(  32,  32 );
    compare( 100, 100 );
    compare( 128, 128 );
    compare( 255, 255 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_gt_pos
  //----------------------------------------------------------------------

  task test_case_4_gt_pos();
    $display( "\ntest_case_4_gt_pos" );
    t.reset_sequence();

    compare(   1,   0 );
    compare(   2,   1 );
    compare(   9,   3 );
    compare(  42,  13 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_gt_neg
  //----------------------------------------------------------------------

  task test_case_5_gt_neg();
    $display( "\ntest_case_5_gt_neg" );
    t.reset_sequence();

    compare(    0,   -1 );
    compare(    1,   -1 );
    compare(    2,   -1 );
    compare(    0, -128 );
    compare(    1, -128 );
    compare(    2, -128 );

    compare(    0,   -5 );
    compare(   -1,   -5 );
    compare(   -2,   -5 );
    compare( -100, -128 );
    compare( -127, -128 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_6_random();
    $display( "\ntest_case_6_random" );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_lt_pos();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_lt_neg();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_eq();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_gt_pos();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_gt_neg();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();

    $write("\n");
    $finish;
  end

endmodule

