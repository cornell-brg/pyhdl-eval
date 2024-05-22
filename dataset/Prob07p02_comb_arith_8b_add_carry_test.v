//========================================================================
// Prob07p02_comb_arith_8b_add_carry_test
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
  logic       ref_module_cin;
  logic [7:0] ref_module_out;
  logic       ref_module_cout;

  RefModule ref_module
  (
    .in0  (ref_module_in0),
    .in1  (ref_module_in1),
    .cin  (ref_module_cin),
    .out  (ref_module_out),
    .cout (ref_module_cout)
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic       top_module_cin;
  logic [7:0] top_module_out;
  logic       top_module_cout;

  TopModule top_module
  (
    .in0  (top_module_in0),
    .in1  (top_module_in1),
    .cin  (top_module_cin),
    .out  (top_module_out),
    .cout (top_module_cout)
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
    input logic       cin
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_cin = cin;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_cin = cin;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_in0, top_module_in1, top_module_cin,
                top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out,  ref_module_out  );
    `TEST_UTILS_CHECK_EQ( top_module_cout, ref_module_cout );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_positive
  //----------------------------------------------------------------------

  task test_case_1_positive();
    $display( "\ntest_case_1_positive" );
    t.reset_sequence();

    compare(   0,  0, 0 );
    compare(   0,  1, 0 );
    compare(   1,  0, 0 );
    compare(  42, 13, 0 );
    compare(  13, 42, 0 );
    compare( 100, 27, 0 );
                         ;
    compare(   0,  0, 1 );
    compare(   0,  1, 1 );
    compare(   1,  0, 1 );
    compare(  42, 13, 1 );
    compare(  13, 42, 1 );
    compare( 100, 26, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_negative
  //----------------------------------------------------------------------

  task test_case_2_negative();
    $display( "\ntest_case_2_negative" );
    t.reset_sequence();

    compare(    0,  -1, 0 );
    compare(   -1,   0, 0 );
    compare(   42, -13, 0 );
    compare(  -42,  13, 0 );
    compare(  -42, -13, 0 );
    compare( -128, 127, 0 );

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

    compare(  127,   1, 0 );
    compare(  126,   2, 0 );
    compare(  120,  13, 0 );
    compare( -128,  -1, 0 );
    compare( -127,  -2, 0 );
    compare( -120, -13, 0 );

    compare(  127,   0, 1 );
    compare(  126,   1, 1 );
    compare(  120,  12, 1 );
    compare( -128,  -2, 1 );
    compare( -127,  -3, 1 );
    compare( -120, -14, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_4_random();
    $display( "\ntest_case_4_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

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
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random();

    $write("\n");
    $finish;
  end

endmodule

