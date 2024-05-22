//========================================================================
// Prob07p05_comb_arith_100b_popcount_test
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

  logic [99:0] ref_module_in_;
  logic [ 6:0] ref_module_out;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .out (ref_module_out)
  );

  logic [99:0] top_module_in_;
  logic [ 6:0] top_module_out;

  TopModule top_module
  (
    .in_ (top_module_in_),
    .out (top_module_out)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [99:0] in_
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_in_, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_small
  //----------------------------------------------------------------------

  task test_case_1_small();
    $display( "\ntest_case_1_small" );
    t.reset_sequence();

    compare( 8'b0000_0000 );

    compare( 8'b0000_0001 );
    compare( 8'b0000_0010 );
    compare( 8'b0000_0100 );
    compare( 8'b0000_1000 );
    compare( 8'b0001_0000 );
    compare( 8'b0010_0000 );
    compare( 8'b0100_0000 );
    compare( 8'b1000_0000 );

    compare( 8'b0000_0011 );
    compare( 8'b0000_1110 );
    compare( 8'b0011_1100 );
    compare( 8'b1111_1000 );
    compare( 8'b1111_1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_large
  //----------------------------------------------------------------------

  task test_case_2_large();
    $display( "\ntest_case_2_large" );
    t.reset_sequence();

    compare( 100'h0_0000_0000_0000_0000_0000_0001 );
    compare( 100'h0_0000_0000_0000_0000_0000_0011 );
    compare( 100'h0_0000_0000_0000_0000_0000_0111 );
    compare( 100'h0_0000_0000_0000_0000_0000_1111 );

    compare( 100'h0_0000_0000_0000_0000_0001_1111 );
    compare( 100'h0_0000_0000_0000_0000_0011_1111 );
    compare( 100'h0_0000_0000_0000_0000_0111_1111 );
    compare( 100'h0_0000_0000_0000_0000_1111_1111 );

    compare( 100'h0_0000_0000_0000_0001_1111_1111 );
    compare( 100'h0_0000_0000_0000_0011_1111_1111 );
    compare( 100'h0_0000_0000_0000_0111_1111_1111 );
    compare( 100'h0_0000_0000_0000_1111_1111_1111 );

    compare( 100'h0_0000_0000_0001_1111_1111_1111 );
    compare( 100'h0_0000_0000_0011_1111_1111_1111 );
    compare( 100'h0_0000_0000_0111_1111_1111_1111 );
    compare( 100'h0_0000_0000_1111_1111_1111_1111 );

    compare( 100'h0_0000_0001_1111_1111_1111_1111 );
    compare( 100'h0_0000_0011_1111_1111_1111_1111 );
    compare( 100'h0_0000_0111_1111_1111_1111_1111 );
    compare( 100'h0_0000_1111_1111_1111_1111_1111 );

    compare( 100'h0_0001_1111_1111_1111_1111_1111 );
    compare( 100'h0_0011_1111_1111_1111_1111_1111 );
    compare( 100'h0_0111_1111_1111_1111_1111_1111 );
    compare( 100'h0_1111_1111_1111_1111_1111_1111 );

    compare( 100'h1_1111_1111_1111_1111_1111_1111 );
    compare( 100'h3_3333_3333_3333_3333_3333_3333 );
    compare( 100'h7_7777_7777_7777_7777_7777_7777 );
    compare( 100'hf_ffff_ffff_ffff_ffff_ffff_ffff );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_random();
    $display( "\ntest_case_3_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 ) begin
      compare( { $urandom(t.seed), $urandom(t.seed),
                 $urandom(t.seed), $urandom(t.seed) } );
    end

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_small();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_large();
    if ((t.n <= 0) || (t.n == 4)) test_case_3_random();

    $write("\n");
    $finish;
  end

endmodule

