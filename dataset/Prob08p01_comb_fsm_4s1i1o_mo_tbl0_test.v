//========================================================================
// Prob08p01_comb_fsm_4s1i1o_mo_tbl0_test
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

  logic [3:0] ref_module_state;
  logic       ref_module_in_;
  logic [3:0] ref_module_state_next;
  logic       ref_module_out;

  RefModule ref_module
  (
    .state      (ref_module_state),
    .in_        (ref_module_in_),
    .state_next (ref_module_state_next),
    .out        (ref_module_out)
  );

  logic [3:0] top_module_state;
  logic       top_module_in_;
  logic [3:0] top_module_state_next;
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
    input logic [3:0] state,
    input logic       in_
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
  // test_case_1_valid
  //----------------------------------------------------------------------

  task test_case_1_valid();
    $display( "\ntest_case_1_valid" );
    t.reset_sequence();

    compare( 4'b0001, 0 );
    compare( 4'b0001, 1 );
    compare( 4'b0010, 0 );
    compare( 4'b0010, 1 );
    compare( 4'b0100, 0 );
    compare( 4'b0100, 1 );
    compare( 4'b1000, 0 );
    compare( 4'b1000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_invalid
  //----------------------------------------------------------------------

  task test_case_2_invalid();
    $display( "\ntest_case_2_invalid" );
    t.reset_sequence();

    compare( 4'b0000, 0 );
    compare( 4'b0000, 1 );
    // compare( 4'b0001, 0 ); valid
    // compare( 4'b0001, 1 ); valid

    // compare( 4'b0010, 0 ); valid
    // compare( 4'b0010, 1 ); valid
    compare( 4'b0011, 0 );
    compare( 4'b0011, 1 );

    // compare( 4'b0100, 0 ); valid
    // compare( 4'b0100, 1 ); valid
    compare( 4'b0101, 0 );
    compare( 4'b0101, 1 );

    compare( 4'b0110, 0 );
    compare( 4'b0110, 1 );
    compare( 4'b0111, 0 );
    compare( 4'b0111, 1 );

    // compare( 4'b1000, 0 ); valid
    // compare( 4'b1000, 1 ); valid
    compare( 4'b1001, 0 );
    compare( 4'b1001, 1 );

    compare( 4'b1010, 0 );
    compare( 4'b1010, 1 );
    compare( 4'b1011, 0 );
    compare( 4'b1011, 1 );

    compare( 4'b1100, 0 );
    compare( 4'b1100, 1 );
    compare( 4'b1101, 0 );
    compare( 4'b1101, 1 );

    compare( 4'b1110, 0 );
    compare( 4'b1110, 1 );
    compare( 4'b1111, 0 );
    compare( 4'b1111, 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_valid();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_invalid();

    $write("\n");
    $finish;
  end

endmodule

