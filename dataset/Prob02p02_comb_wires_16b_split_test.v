//========================================================================
// Prob02p02_comb_wires_16b_split_test
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

  logic [7:0] ref_module_in_;
  logic [3:0] ref_module_lo;
  logic [3:0] ref_module_hi;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .lo  (ref_module_lo),
    .hi  (ref_module_hi)
  );

  logic [7:0] top_module_in_;
  logic [3:0] top_module_lo;
  logic [3:0] top_module_hi;

  TopModule top_module
  (
    .in_ (top_module_in_),
    .lo  (top_module_lo),
    .hi  (top_module_hi)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [7:0] in_
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x %x", t.cycles, top_module_in_,
                top_module_lo, top_module_hi );

    `TEST_UTILS_CHECK_EQ( top_module_lo, ref_module_lo );
    `TEST_UTILS_CHECK_EQ( top_module_hi, ref_module_hi );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 8'h00 );
    compare( 8'h01 );
    compare( 8'h10 );
    compare( 8'h23 );
    compare( 8'h45 );
    compare( 8'h67 );
    compare( 8'h89 );
    compare( 8'hab );
    compare( 8'hcd );
    compare( 8'hef );

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

