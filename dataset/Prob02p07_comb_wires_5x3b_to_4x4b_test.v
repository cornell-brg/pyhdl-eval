//========================================================================
// Prob02p07_comb_wires_5x3b_to_4x4b_test
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

  logic [2:0] ref_module_in0;
  logic [2:0] ref_module_in1;
  logic [2:0] ref_module_in2;
  logic [2:0] ref_module_in3;
  logic [2:0] ref_module_in4;
  logic [3:0] ref_module_out0;
  logic [3:0] ref_module_out1;
  logic [3:0] ref_module_out2;
  logic [3:0] ref_module_out3;

  RefModule ref_module
  (
    .in0  (ref_module_in0),
    .in1  (ref_module_in1),
    .in2  (ref_module_in2),
    .in3  (ref_module_in3),
    .in4  (ref_module_in4),
    .out0 (ref_module_out0),
    .out1 (ref_module_out1),
    .out2 (ref_module_out2),
    .out3 (ref_module_out3)
  );

  logic [2:0] top_module_in0;
  logic [2:0] top_module_in1;
  logic [2:0] top_module_in2;
  logic [2:0] top_module_in3;
  logic [2:0] top_module_in4;
  logic [3:0] top_module_out0;
  logic [3:0] top_module_out1;
  logic [3:0] top_module_out2;
  logic [3:0] top_module_out3;

  TopModule top_module
  (
    .in0  (top_module_in0),
    .in1  (top_module_in1),
    .in2  (top_module_in2),
    .in3  (top_module_in3),
    .in4  (top_module_in4),
    .out0 (top_module_out0),
    .out1 (top_module_out1),
    .out2 (top_module_out2),
    .out3 (top_module_out3)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [2:0] in0,
    input logic [2:0] in1,
    input logic [2:0] in2,
    input logic [2:0] in3,
    input logic [2:0] in4
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_in2 = in2;
    ref_module_in3 = in3;
    ref_module_in4 = in4;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_in2 = in2;
    top_module_in3 = in3;
    top_module_in4 = in4;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x %x %x %x", t.cycles,
                top_module_in0,  top_module_in1,
                top_module_in2,  top_module_in3, top_module_in4,
                top_module_out0, top_module_out1,
                top_module_out2, top_module_out3 );

    `TEST_UTILS_CHECK_EQ( top_module_out0, ref_module_out0 );
    `TEST_UTILS_CHECK_EQ( top_module_out1, ref_module_out1 );
    `TEST_UTILS_CHECK_EQ( top_module_out2, ref_module_out2 );
    `TEST_UTILS_CHECK_EQ( top_module_out3, ref_module_out3 );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 0, 0, 0, 0, 0 );
    compare( 1, 1, 1, 1, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 1, 0 );
    compare( 0, 0, 1, 0, 0 );
    compare( 0, 1, 0, 0, 0 );
    compare( 1, 0, 0, 0, 0 );
    compare( 1, 2, 3, 4, 5 );
    compare( 3, 4, 5, 6, 7 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_2_random();
    $display( "\ntest_case_2_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_random();

    $write("\n");
    $finish;
  end

endmodule

