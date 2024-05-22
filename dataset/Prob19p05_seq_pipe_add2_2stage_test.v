//========================================================================
// Prob19p05_seq_pipe_add2_2stage_test
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
  logic [3:0] ref_module_out_lsn;
  logic [7:0] ref_module_out;

  RefModule ref_module
  (
    .in0     (ref_module_in0),
    .in1     (ref_module_in1),
    .out_lsn (ref_module_out_lsn),
    .out     (ref_module_out),
    .*
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic [3:0] top_module_out_lsn;
  logic [7:0] top_module_out;

  TopModule top_module
  (
    .in0     (top_module_in0),
    .in1     (top_module_in1),
    .out_lsn (top_module_out_lsn),
    .out     (top_module_out),
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
    input logic       check_output
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;

    top_module_in0 = in0;
    top_module_in1 = in1;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_out_lsn, top_module_out );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_out_lsn, ref_module_out_lsn );
      `TEST_UTILS_CHECK_EQ( top_module_out,     ref_module_out     );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_positive
  //----------------------------------------------------------------------

  task test_case_1_positive();
    $display( "\ntest_case_1_positive" );
    t.reset_sequence();

    compare(   0,  0, 0 ); // do not check output
    compare(   0,  0, 0 ); // do not check output
    compare(   0,  0, 1 );
    compare(   0,  1, 1 );
    compare(   1,  0, 1 );
    compare(  42, 13, 1 );
    compare(  13, 42, 1 );
    compare( 100, 27, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_negative
  //----------------------------------------------------------------------

  task test_case_2_negative();
    $display( "\ntest_case_2_negative" );
    t.reset_sequence();

    compare(    0,   0, 0 ); // do not check output
    compare(    0,   0, 0 ); // do not check output
    compare(    0,  -1, 1 );
    compare(   -1,   0, 1 );
    compare(   42, -13, 1 );
    compare(  -42,  13, 1 );
    compare(  -42, -13, 1 );
    compare( -128, 127, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_overflow
  //----------------------------------------------------------------------

  task test_case_3_overflow();
    $display( "\ntest_case_3_overflow" );
    t.reset_sequence();

    compare(    0,   0, 0 ); // do not check output
    compare(    0,   0, 0 ); // do not check output
    compare(  127,   1, 1 );
    compare(  126,   2, 1 );
    compare(  120,  13, 1 );
    compare( -128,  -1, 1 );
    compare( -127,  -2, 1 );
    compare( -120, -13, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_mid_carry
  //----------------------------------------------------------------------

  task test_case_4_mid_carry();
    $display( "\ntest_case_4_mid_carry" );
    t.reset_sequence();

    compare( 8'h00, 8'h00, 0 ); // do not check output
    compare( 8'h00, 8'h00, 0 ); // do not check output
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h08, 8'h08, 1 );
    compare( 8'h0c, 8'h0c, 1 );
    compare( 8'h0d, 8'h0d, 1 );
    compare( 8'h18, 8'h18, 1 );
    compare( 8'h1c, 8'h1c, 1 );
    compare( 8'h1d, 8'h1d, 1 );
    compare( 8'h38, 8'h38, 1 );
    compare( 8'h3c, 8'h3c, 1 );
    compare( 8'h3d, 8'h3d, 1 );
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_example
  //----------------------------------------------------------------------

  task test_case_5_example();
    $display( "\ntest_case_5_example" );
    t.reset_sequence();

    compare( 8'h00, 8'h00, 0 ); // do not check output
    compare( 8'h00, 8'h00, 0 ); // do not check output
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h01, 8'h01, 1 );
    compare( 8'h02, 8'h03, 1 );
    compare( 8'h03, 8'h04, 1 );
    compare( 8'h11, 8'h11, 1 );
    compare( 8'h12, 8'h13, 1 );
    compare( 8'h13, 8'h14, 1 );
    compare( 8'h09, 8'h09, 1 );
    compare( 8'h19, 8'h19, 1 );
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 1 );
    compare( 8'h00, 8'h00, 1 );

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

    compare( 0, 0, 0 ); // do not check output
    compare( 0, 0, 0 ); // do not check output

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_positive();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_negative();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_overflow();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_mid_carry();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_example();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();

    $write("\n");
    $finish;
  end

endmodule
