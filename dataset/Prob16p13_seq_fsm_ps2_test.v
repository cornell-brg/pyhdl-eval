//========================================================================
// Prob16p13_seq_fsm_ps2_test
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
  logic [7:0] ref_module_in_;
  logic       ref_module_done;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .in_   (ref_module_in_),
    .done  (ref_module_done),
    .*
  );

  logic       top_module_reset;
  logic [7:0] top_module_in_;
  logic       top_module_done;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .in_   (top_module_in_),
    .done  (top_module_done),
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
    input logic       reset,
    input logic [7:0] in_
  );

    ref_module_reset = reset;
    ref_module_in_   = in_;

    top_module_reset = reset;
    top_module_in_   = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_reset, top_module_in_, top_module_done );

    `TEST_UTILS_CHECK_EQ( top_module_done, ref_module_done );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_simple
  //----------------------------------------------------------------------

  task test_case_1_simple();
    $display( "\ntest_case_1_simple" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 0, 8'b0000_0000 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 0, 8'b0000_0000 ); // C -> A done=1
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 0, 8'b0000_0000 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A

  endtask

  //----------------------------------------------------------------------
  // test_case_2_consecutive_ones
  //----------------------------------------------------------------------

  task test_case_2_consecutive_ones();
    $display( "\ntest_case_2_consecutive_ones" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_1000 ); // B -> C
    compare( 0, 8'b0000_1000 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_1000 ); // B -> C
    compare( 0, 8'b0000_1000 ); // C -> A done=1
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_1000 ); // B -> C
    compare( 0, 8'b0000_1000 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A

  endtask

  //----------------------------------------------------------------------
  // test_case_3_example
  //----------------------------------------------------------------------

  task test_case_3_example();
    $display( "\ntest_case_3_example" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0010_0101 ); // A -> A
    compare( 0, 8'b0101_0010 ); // A -> A
    compare( 0, 8'b0011_1000 ); // A -> B
    compare( 0, 8'b1100_1000 ); // B -> C
    compare( 0, 8'b0011_0010 ); // C -> A done=1
    compare( 0, 8'b1010_0011 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0101_0100 ); // B -> C
    compare( 0, 8'b0000_0010 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A

  endtask

  //----------------------------------------------------------------------
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 1, 8'b0000_0000 ); // reset
    compare( 1, 8'b0000_0000 ); // reset
    compare( 1, 8'b0000_0000 ); // reset
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 0, 8'b0000_0000 ); // C -> A done=1
    compare( 0, 8'b0000_0000 ); // A -> A
    compare( 0, 8'b0000_1000 ); // A -> B
    compare( 0, 8'b0000_0000 ); // B -> C
    compare( 0, 8'b0000_0000 ); // C -> A done=1

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    for ( int i = 0; i < 40; i = i+1 )
      compare( 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random_reset
  //----------------------------------------------------------------------

  task test_case_6_random_reset();
    $display( "\ntest_case_6_random_reset" );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_simple();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_consecutive_ones();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_example();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random_reset();

    $write("\n");
    $finish;
  end

endmodule

