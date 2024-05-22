//========================================================================
// Prob03p10_comb_gates_4b_pairwise_test
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

  logic [3:0] ref_module_in_;
  logic [2:0] ref_module_out_and;
  logic [2:0] ref_module_out_or;
  logic [2:0] ref_module_out_xnor;

  RefModule ref_module
  (
    .in_      (ref_module_in_),
    .out_and  (ref_module_out_and),
    .out_or   (ref_module_out_or),
    .out_xnor (ref_module_out_xnor)
  );

  logic [3:0] top_module_in_;
  logic [2:0] top_module_out_and;
  logic [2:0] top_module_out_or;
  logic [2:0] top_module_out_xnor;

  TopModule top_module
  (
    .in_      (top_module_in_),
    .out_and  (top_module_out_and),
    .out_or   (top_module_out_or),
    .out_xnor (top_module_out_xnor)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [3:0] in_
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x %x %x", t.cycles,
                top_module_in_,
                top_module_out_and, top_module_out_or,
                top_module_out_xnor );

    `TEST_UTILS_CHECK_EQ( top_module_out_and,  ref_module_out_and  );
    `TEST_UTILS_CHECK_EQ( top_module_out_or,   ref_module_out_or   );
    `TEST_UTILS_CHECK_EQ( top_module_out_xnor, ref_module_out_xnor );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 4'b0000 );
    compare( 4'b0001 );
    compare( 4'b0010 );
    compare( 4'b0011 );
    compare( 4'b0100 );
    compare( 4'b0101 );
    compare( 4'b0110 );
    compare( 4'b0111 );

    compare( 4'b1000 );
    compare( 4'b1001 );
    compare( 4'b1010 );
    compare( 4'b1011 );
    compare( 4'b1100 );
    compare( 4'b1101 );
    compare( 4'b1110 );
    compare( 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();

    $write("\n");
    $finish;
  end

endmodule

