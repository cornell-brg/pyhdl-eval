//========================================================================
// Prob05p09_comb_mux_1b_1to128_test
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

  logic         ref_module_in_;
  logic   [6:0] ref_module_sel;
  logic [127:0] ref_module_out;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .sel (ref_module_sel),
    .out (ref_module_out)
  );

  logic         top_module_in_;
  logic   [6:0] top_module_sel;
  logic [127:0] top_module_out;

  TopModule top_module
  (
    .in_ (top_module_in_),
    .sel (top_module_sel),
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
    input logic       in_,
    input logic [6:0] sel
  );

    ref_module_in_ = in_;
    ref_module_sel = sel;

    top_module_in_ = in_;
    top_module_sel = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_in_, top_module_sel, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 0,   0 );
    compare( 1,   0 );
    compare( 0,   1 );
    compare( 1,   1 );
    compare( 0,   2 );
    compare( 1,   2 );
    compare( 0,   3 );
    compare( 1,   3 );

    compare( 0,  15 );
    compare( 1,  15 );
    compare( 0, 100 );
    compare( 1, 100 );
    compare( 0, 127 );
    compare( 1, 127 );

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
      compare( $urandom(t.seed), $urandom(t.seed) );

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

