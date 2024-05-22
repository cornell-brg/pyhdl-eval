//========================================================================
// Prob19p08_seq_pipe_minmax4_2stage_test
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

  logic [7:0] ref_module_in0;
  logic [7:0] ref_module_in1;
  logic [7:0] ref_module_in2;
  logic [7:0] ref_module_in3;
  logic [7:0] ref_module_min;
  logic [7:0] ref_module_max;

  RefModule ref_module
  (
    .in0 (ref_module_in0),
    .in1 (ref_module_in1),
    .in2 (ref_module_in2),
    .in3 (ref_module_in3),
    .min (ref_module_min),
    .max (ref_module_max),
    .*
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic [7:0] top_module_in2;
  logic [7:0] top_module_in3;
  logic [7:0] top_module_min;
  logic [7:0] top_module_max;

  TopModule top_module
  (
    .in0 (top_module_in0),
    .in1 (top_module_in1),
    .in2 (top_module_in2),
    .in3 (top_module_in3),
    .min (top_module_min),
    .max (top_module_max),
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
    input logic [7:0] in0,
    input logic [7:0] in1,
    input logic [7:0] in2,
    input logic [7:0] in3,
    input logic       check_output
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_in2 = in2;
    ref_module_in3 = in3;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_in2 = in2;
    top_module_in3 = in3;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_in2, top_module_in3,
                top_module_min, top_module_max );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_min, ref_module_min );
      `TEST_UTILS_CHECK_EQ( top_module_max, ref_module_max );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_small
  //----------------------------------------------------------------------

  task test_case_1_small();
    $display( "\ntest_case_1_small" );
    t.reset_sequence();

    compare(    0,    0,   0,    0, 0 ); // do not check output
    compare(    0,    0,   0,    0, 0 ); // do not check output

    compare( 1, 2, 3, 4, 1 );
    compare( 4, 3, 2, 1, 1 );
    compare( 3, 4, 1, 2, 1 );
    compare( 1, 4, 3, 2, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_dups
  //----------------------------------------------------------------------

  task test_case_2_dups();
    $display( "\ntest_case_2_dups" );
    t.reset_sequence();

    compare( 0, 0, 0, 0, 0 ); // do not check output
    compare( 0, 0, 0, 0, 0 ); // do not check output

    compare( 0, 0, 0, 0, 1 );
    compare( 9, 9, 9, 9, 1 );
    compare( 1, 1, 2, 2, 1 );
    compare( 2, 2, 1, 1, 1 );
    compare( 2, 1, 2, 1, 1 );
    compare( 1, 1, 2, 1, 1 );
    compare( 1, 2, 2, 2, 1 );
    compare( 2, 2, 1, 2, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_large
  //----------------------------------------------------------------------

  task test_case_3_large();
    $display( "\ntest_case_3_large" );
    t.reset_sequence();

    compare(    0,    0,    0,    0, 0 ); // do not check output
    compare(    0,    0,    0,    0, 0 ); // do not check output

    compare( 101, 102, 103, 104, 1 );
    compare( 104, 103, 102, 101, 1 );
    compare( 103, 104, 101, 102, 1 );
    compare( 101, 104, 103, 102, 1 );
    compare( 255, 254, 252, 253, 1 );
    compare( 252, 253, 254, 255, 1 );
    compare( 253, 252, 255, 254, 1 );
    compare( 255, 252, 253, 254, 1 );
    compare(   0,   0,   0,   0, 1 );
    compare(   0,   0,   0,   0, 1 );
    compare(   0,   0,   0,   0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_example
  //----------------------------------------------------------------------

  task test_case_4_example();
    $display( "\ntest_case_4_example" );
    t.reset_sequence();

    compare( 8'h00, 8'h00, 8'h00, 8'h00, 0 ); // do not check output
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 0 ); // do not check output

    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );
    compare( 8'h01, 8'h02, 8'h03, 8'h04, 1 );
    compare( 8'h04, 8'h05, 8'h03, 8'h02, 1 );
    compare( 8'h06, 8'h03, 8'h04, 8'h05, 1 );
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 8'h00, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    compare( 0, 0, 0, 0, 0 ); // do not check output
    compare( 0, 0, 0, 0, 0 ); // do not check output

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_small();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_dups();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_large();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_example();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

