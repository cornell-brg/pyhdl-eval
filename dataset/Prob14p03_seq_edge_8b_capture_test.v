//========================================================================
// Prob14p03_seq_edge_8b_capture_test
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
  logic [7:0] ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .in_   (ref_module_in_),
    .out   (ref_module_out),
    .*
  );

  logic       top_module_reset;
  logic [7:0] top_module_in_;
  logic [7:0] top_module_out;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .in_   (top_module_in_),
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
    input logic       reset,
    input logic [7:0] in_
  );

    ref_module_in_ = reset;
    ref_module_in_ = in_;

    top_module_in_ = reset;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_reset, top_module_in_, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_one_bit_toggle
  //----------------------------------------------------------------------

  task test_case_1_one_bit_toggle();
    $display( "\ntest_case_1_one_bit_toggle" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_one_bit_repeat
  //----------------------------------------------------------------------

  task test_case_2_one_bit_repeat();
    $display( "\ntest_case_2_one_bit_repeat" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0001 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_many_bits
  //----------------------------------------------------------------------

  task test_case_3_many_bits();
    $display( "\ntest_case_3_many_bits" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b1010_1010 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b1010_1010 );
    compare( 0, 8'b0101_0101 );
    compare( 0, 8'b1111_1111 );
    compare( 0, 8'b0101_0101 );
    compare( 0, 8'b1111_1111 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b1010_1010 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b1010_1010 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_example
  //----------------------------------------------------------------------

  task test_case_4_example();
    $display( "\ntest_case_4_example" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0001_0001 );
    compare( 0, 8'b0101_0101 );
    compare( 0, 8'b0001_0001 );
    compare( 0, 8'b0100_0100 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_directed_reset
  //----------------------------------------------------------------------

  task test_case_5_directed_reset();
    $display( "\ntest_case_5_directed_reset" );
    t.reset_sequence();

    //       rs in_
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0001_0001 );
    compare( 0, 8'b0101_0101 );
    compare( 0, 8'b0001_0001 );
    compare( 0, 8'b0100_0100 );
    compare( 0, 8'b0000_0000 );
    compare( 0, 8'b0000_0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random
  //----------------------------------------------------------------------

  task test_case_6_random();
    $display( "\ntest_case_6_random" );
    t.reset_sequence();

    for ( int i = 0; i < 60; i = i+1 )
      compare( 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random_reset
  //----------------------------------------------------------------------

  task test_case_7_random_reset();
    $display( "\ntest_case_7_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 60; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_one_bit_toggle();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_one_bit_repeat();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_many_bits();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_example();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_directed_reset();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_random_reset();

    $write("\n");
    $finish;
  end

endmodule

