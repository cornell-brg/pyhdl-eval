//========================================================================
// Prob19p07_seq_pipe_add4_2stage_test
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
  logic [7:0] ref_module_out01;
  logic [7:0] ref_module_out23;
  logic [7:0] ref_module_out;

  RefModule ref_module
  (
    .in0   (ref_module_in0),
    .in1   (ref_module_in1),
    .in2   (ref_module_in2),
    .in3   (ref_module_in3),
    .out01 (ref_module_out01),
    .out23 (ref_module_out23),
    .out   (ref_module_out),
    .*
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic [7:0] top_module_in2;
  logic [7:0] top_module_in3;
  logic [7:0] top_module_out01;
  logic [7:0] top_module_out23;
  logic [7:0] top_module_out;

  TopModule top_module
  (
    .in0   (top_module_in0),
    .in1   (top_module_in1),
    .in2   (top_module_in2),
    .in3   (top_module_in3),
    .out01 (top_module_out01),
    .out23 (top_module_out23),
    .out   (top_module_out),
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
      $display( "%3d: %x %x %x %x > %x %x %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_in2, top_module_in3,
                top_module_out01, top_module_out23, top_module_out );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_out01, ref_module_out01 );
      `TEST_UTILS_CHECK_EQ( top_module_out23, ref_module_out23 );
      `TEST_UTILS_CHECK_EQ( top_module_out,   ref_module_out   );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_input2
  //----------------------------------------------------------------------

  task test_case_1_input2();
    $display( "\ntest_case_1_input2" );
    t.reset_sequence();

    compare(    0,    0,   0,    0, 0 ); // do not check output
    compare(    0,    0,   0,    0, 0 ); // do not check output

    compare(    0,    0,   0,    0, 1 );

    compare(    0,    1,   0,    0, 1 );
    compare(    1,    0,   0,    0, 1 );
    compare(   42,   13,   0,    0, 1 );
    compare(   13,   42,   0,    0, 1 );
    compare(  100,   27,   0,    0, 1 );

    compare(    0,   -1,   0,    0, 1 );
    compare(   -1,    0,   0,    0, 1 );
    compare(   -1,    0,   0,    0, 1 );
    compare(   42,  -13,   0,    0, 1 );
    compare(  -42,   13,   0,    0, 1 );
    compare(  -42,  -13,   0,    0, 1 );
    compare( -128,  127,   0,    0, 1 );

    compare(    0,    0,   1,    0, 1 );
    compare(    0,    1,   0,    0, 1 );
    compare(    0,   42,  13,    0, 1 );
    compare(    0,   13,  42,    0, 1 );
    compare(    0,  100,  27,    0, 1 );

    compare(    0,    0,  -1,    0, 1 );
    compare(    0,   -1,   0,    0, 1 );
    compare(    0,   -1,   0,    0, 1 );
    compare(    0,   42, -13,    0, 1 );
    compare(    0,  -42,  13,    0, 1 );
    compare(    0,  -42, -13,    0, 1 );
    compare(    0, -128, 127,    0, 1 );

    compare(    0,    0,    0,   1, 1 );
    compare(    0,    0,    1,   0, 1 );
    compare(    0,    0,   42,  13, 1 );
    compare(    0,    0,   13,  42, 1 );
    compare(    0,    0,  100,  27, 1 );

    compare(    0,    0,    0,  -1, 1 );
    compare(    0,    0,   -1,   0, 1 );
    compare(    0,    0,   -1,   0, 1 );
    compare(    0,    0,   42, -13, 1 );
    compare(    0,    0,  -42,  13, 1 );
    compare(    0,    0,  -42, -13, 1 );
    compare(    0,    0, -128, 127, 1 );

    compare(    0,    0,    0,   0, 1 );
    compare(    0,    0,    0,   0, 1 );
    compare(    0,    0,    0,   0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_input4
  //----------------------------------------------------------------------

  task test_case_2_input4();
    $display( "\ntest_case_2_input4" );
    t.reset_sequence();

    compare( 0, 0, 0, 0, 0 ); // do not check output
    compare( 0, 0, 0, 0, 0 ); // do not check output

    compare( 0, 0, 0, 0, 1 );
    compare( 1, 1, 1, 1, 1 );
    compare( 1, 2, 3, 4, 1 );
    compare( 4, 1, 2, 3, 1 );
    compare( 3, 4, 1, 2, 1 );
    compare( 2, 3, 4, 1, 1 );
    compare( 0, 0, 0, 0, 1 );
    compare( 0, 0, 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_overflow
  //----------------------------------------------------------------------

  task test_case_3_overflow();
    $display( "\ntest_case_3_overflow" );
    t.reset_sequence();

    compare(    0,    0,    0,    0, 0 ); // do not check output
    compare(    0,    0,    0,    0, 0 ); // do not check output

    compare(  127,    1,    0,    0, 1 );
    compare(    0,  127,    1,    0, 1 );
    compare(    0,    0,  127,    1, 1 );
    compare(    1,    0,    0,  127, 1 );
    compare( -128,   -1,    0,    0, 1 );
    compare(    0, -128,   -1,    0, 1 );
    compare(    0,    0, -128,   -1, 1 );
    compare(   -1,    0,    0, -128, 1 );
    compare(   64,   64,   64,   64, 1 );
    compare(  -64,  -64,  -64,  -64, 1 );
    compare(  128,  128,  128,  128, 1 );
    compare(    0,    0,    0,    0, 1 );
    compare(    0,    0,    0,    0, 1 );
    compare(    0,    0,    0,    0, 1 );

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
    compare( 8'h02, 8'h03, 8'h04, 8'h05, 1 );
    compare( 8'h03, 8'h04, 8'h05, 8'h06, 1 );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_input2();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_input4();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_overflow();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_example();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

