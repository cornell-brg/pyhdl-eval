//========================================================================
// Prob07p11_comb_arith_8b_fxp_umul_test
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
  logic [7:0] ref_module_out;
  logic       ref_module_overflow;

  RefModule ref_module
  (
    .in0      (ref_module_in0),
    .in1      (ref_module_in1),
    .out      (ref_module_out),
    .overflow (ref_module_overflow)
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic [7:0] top_module_out;
  logic       top_module_overflow;

  TopModule top_module
  (
    .in0      (top_module_in0),
    .in1      (top_module_in1),
    .out      (top_module_out),
    .overflow (top_module_overflow)
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
      $display( "%3d: %x %x > %x %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_out, top_module_overflow );

    `TEST_UTILS_CHECK_EQ( top_module_out,      ref_module_out      );
    `TEST_UTILS_CHECK_EQ( top_module_overflow, ref_module_overflow );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_whole
  //----------------------------------------------------------------------

  task test_case_1_whole();
    $display( "\ntest_case_1_whole" );
    t.reset_sequence();

    compare( 8'h10, 8'h00 );
    compare( 8'h10, 8'h10 );
    compare( 8'h10, 8'h00 );
    compare( 8'h20, 8'h20 );
    compare( 8'h20, 8'h30 );
    compare( 8'h30, 8'h20 );
    compare( 8'h30, 8'h30 );
    compare( 8'h40, 8'h30 );
    compare( 8'h30, 8'h40 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_frac_exact
  //----------------------------------------------------------------------

  task test_case_2_frac_exact();
    $display( "\ntest_case_2_frac_exact" );
    t.reset_sequence();

    compare( 8'h08, 8'h08 );
    compare( 8'h08, 8'h04 );
    compare( 8'h04, 8'h08 );
    compare( 8'h02, 8'h08 );
    compare( 8'h08, 8'h02 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_frac_nonexact
  //----------------------------------------------------------------------

  task test_case_3_frac_nonexact();
    $display( "\ntest_case_3_frac_nonexact" );
    t.reset_sequence();

    compare( 8'h08, 8'h08 );
    compare( 8'h08, 8'h04 );
    compare( 8'h04, 8'h08 );
    compare( 8'h02, 8'h08 );
    compare( 8'h08, 8'h02 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_overflow
  //----------------------------------------------------------------------

  task test_case_4_overflow();
    $display( "\ntest_case_4_overflow" );
    t.reset_sequence();

    compare( 8'h80, 8'h80 );
    compare( 8'h80, 8'h70 );
    compare( 8'h80, 8'h60 );
    compare( 8'h80, 8'h50 );
    compare( 8'h80, 8'h40 );
    compare( 8'h08, 8'h01 );
    compare( 8'h07, 8'h01 );
    compare( 8'h06, 8'h01 );
    compare( 8'h05, 8'h01 );
    compare( 8'h04, 8'h01 );

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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_whole();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_frac_exact();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_frac_nonexact();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_overflow();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

