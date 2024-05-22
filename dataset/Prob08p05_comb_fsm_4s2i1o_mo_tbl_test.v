//========================================================================
// Prob08p05_comb_fsm_4s2i1o_mo_tbl_test
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

  logic [1:0] ref_module_state;
  logic [1:0] ref_module_in_;
  logic [1:0] ref_module_state_next;
  logic       ref_module_out;

  RefModule ref_module
  (
    .state      (ref_module_state),
    .in_        (ref_module_in_),
    .state_next (ref_module_state_next),
    .out        (ref_module_out)
  );

  logic [1:0] top_module_state;
  logic [1:0] top_module_in_;
  logic [1:0] top_module_state_next;
  logic       top_module_out;

  TopModule top_module
  (
    .state      (top_module_state),
    .in_        (top_module_in_),
    .state_next (top_module_state_next),
    .out        (top_module_out)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [1:0] state,
    input logic [1:0] in_
  );

    ref_module_state = state;
    ref_module_in_   = in_;

    top_module_state = state;
    top_module_in_   = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x", t.cycles,
                top_module_state,      top_module_in_,
                top_module_state_next, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_state_next, ref_module_state_next );
    `TEST_UTILS_CHECK_EQ( top_module_out,        ref_module_out        );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 0, 2'b00 );
    compare( 0, 2'b01 );
    compare( 0, 2'b10 );
    compare( 0, 2'b11 );

    compare( 1, 2'b00 );
    compare( 1, 2'b01 );
    compare( 1, 2'b10 );
    compare( 1, 2'b11 );

    compare( 2, 2'b00 );
    compare( 2, 2'b01 );
    compare( 2, 2'b10 );
    compare( 2, 2'b11 );

    compare( 3, 2'b00 );
    compare( 3, 2'b01 );
    compare( 3, 2'b10 );
    compare( 3, 2'b11 );

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

