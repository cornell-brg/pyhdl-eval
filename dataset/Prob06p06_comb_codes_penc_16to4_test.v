//========================================================================
// Prob06p06_comb_codes_penc_16to4_test
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

  logic [15:0] ref_module_in_;
  logic [ 3:0] ref_module_out;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .out (ref_module_out)
  );

  logic [15:0] top_module_in_;
  logic [ 3:0] top_module_out;

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
    input logic [15:0] in_
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
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 16'b0000_0000_0000_0000 );
    compare( 16'b0000_0000_0000_0001 );
    compare( 16'b0000_0000_0000_0010 );
    compare( 16'b0000_0000_0000_0011 );

    compare( 16'b0000_0000_0000_0100 );
    compare( 16'b0000_0000_0000_0101 );
    compare( 16'b0000_0000_0000_0110 );
    compare( 16'b0000_0000_0000_0111 );

    compare( 16'b0000_0000_0000_1000 );
    compare( 16'b0000_0000_0000_1001 );
    compare( 16'b0000_0000_0000_1010 );
    compare( 16'b0000_0000_0000_1011 );

    compare( 16'b0000_0000_0000_1100 );
    compare( 16'b0000_0000_0000_1101 );
    compare( 16'b0000_0000_0000_1110 );
    compare( 16'b0000_0000_0000_1111 );

    compare( 16'b0000_0000_0000_0000 );
    compare( 16'b0001_0000_0000_0000 );
    compare( 16'b0010_0000_0000_0000 );
    compare( 16'b0011_0000_0000_0000 );

    compare( 16'b0100_0000_0000_0000 );
    compare( 16'b0101_0000_0000_0000 );
    compare( 16'b0110_0000_0000_0000 );
    compare( 16'b0111_0000_0000_0000 );

    compare( 16'b1000_0000_0000_0000 );
    compare( 16'b1001_0000_0000_0000 );
    compare( 16'b1010_0000_0000_0000 );
    compare( 16'b1011_0000_0000_0000 );

    compare( 16'b1100_0000_0000_0000 );
    compare( 16'b1101_0000_0000_0000 );
    compare( 16'b1110_0000_0000_0000 );
    compare( 16'b1111_0000_0000_0000 );

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
      compare( $urandom(t.seed) );

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

