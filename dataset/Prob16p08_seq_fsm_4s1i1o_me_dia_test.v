//========================================================================
// Prob16p08_seq_fsm_4s1i1o_me_dia_test
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

  logic       ref_module_reset;
  logic       ref_module_in_;
  logic [1:0] ref_module_state;
  logic       ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .in_   (ref_module_in_),
    .state (ref_module_state),
    .out   (ref_module_out),
    .*
  );

  logic       top_module_reset;
  logic       top_module_in_;
  logic [1:0] top_module_state;
  logic       top_module_out;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .in_   (top_module_in_),
    .state (top_module_state),
    .out   (top_module_out),
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
    input logic reset,
    input logic in_
  );

    ref_module_reset = reset;
    ref_module_in_   = in_;

    top_module_reset = reset;
    top_module_in_   = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x", t.cycles,
                top_module_reset, top_module_in_,
                top_module_state, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_state, ref_module_state );
    `TEST_UTILS_CHECK_EQ( top_module_out,   ref_module_out   );

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 0 ); // A -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 1 ); // B -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 0 ); // C -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 1 ); // C -> D
    compare( 0, 0 ); // D -> C
    compare( 0, 1 ); // C -> D
    compare( 0, 0 ); // D -> C
    compare( 0, 0 ); // C -> A
    compare( 0, 0 ); // A -> A

  endtask

  //----------------------------------------------------------------------
  // test_case_2_directed_reset
  //----------------------------------------------------------------------

  task test_case_2_directed_reset();
    $display( "\ntest_case_2_directed_reset" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 0 ); // A -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 1 ); // B -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 0 ); // C -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 1 ); // C -> D
    compare( 0, 0 ); // D -> C
    compare( 1, 0 ); // reset
    compare( 0, 0 ); // A -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 1 ); // B -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 0 ); // C -> A
    compare( 0, 1 ); // A -> B
    compare( 0, 0 ); // B -> C
    compare( 0, 1 ); // C -> D
    compare( 0, 0 ); // D -> C

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random
  //----------------------------------------------------------------------

  task test_case_3_random();
    $display( "\ntest_case_3_random" );
    t.reset_sequence();

    for ( int i = 0; i < 40; i = i+1 )
      compare( 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random_reset
  //----------------------------------------------------------------------

  task test_case_4_random_reset();
    $display( "\ntest_case_4_random_reset" );
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
    if ((t.n <= 0) || (t.n == 2)) test_case_2_directed_reset();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random_reset();

    $write("\n");
    $finish;
  end

endmodule

