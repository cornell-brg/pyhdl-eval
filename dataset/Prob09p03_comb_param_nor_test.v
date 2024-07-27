//========================================================================
// Prob09p03_comb_param_nor_test
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
  // nbits4: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [3:0] nbits4_ref_module_in_;
  logic       nbits4_ref_module_out;

  RefModule
  #(
    .nbits (4)
  )
  nbits4_ref_module
  (
    .in_ (nbits4_ref_module_in_),
    .out (nbits4_ref_module_out)
  );

  logic [3:0] nbits4_top_module_in_;
  logic       nbits4_top_module_out;

  TopModule
  #(
    .nbits (4)
  )
  nbits4_top_module
  (
    .in_ (nbits4_top_module_in_),
    .out (nbits4_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits4_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits4_compare
  (
    input logic [3:0] in_
  );

    nbits4_ref_module_in_ = in_;
    nbits4_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits4_top_module_in_, nbits4_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits4_top_module_out, nbits4_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_nbist4_directed
  //----------------------------------------------------------------------

  task test_case_1_nbits4_directed();
    $display( "\ntest_case_1_nbits4_directed" );
    t.reset_sequence();

    nbits4_compare( 4'b0000 );
    nbits4_compare( 4'b0001 );
    nbits4_compare( 4'b0010 );
    nbits4_compare( 4'b0011 );
    nbits4_compare( 4'b0100 );
    nbits4_compare( 4'b0101 );
    nbits4_compare( 4'b0110 );
    nbits4_compare( 4'b0111 );

    nbits4_compare( 4'b1000 );
    nbits4_compare( 4'b1001 );
    nbits4_compare( 4'b1010 );
    nbits4_compare( 4'b1011 );
    nbits4_compare( 4'b1100 );
    nbits4_compare( 4'b1101 );
    nbits4_compare( 4'b1110 );
    nbits4_compare( 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // nbits13: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [12:0] nbits13_ref_module_in_;
  logic       nbits13_ref_module_out;

  RefModule
  #(
    .nbits (13)
  )
  nbits13_ref_module
  (
    .in_ (nbits13_ref_module_in_),
    .out (nbits13_ref_module_out)
  );

  logic [12:0] nbits13_top_module_in_;
  logic       nbits13_top_module_out;

  TopModule
  #(
    .nbits (13)
  )
  nbits13_top_module
  (
    .in_ (nbits13_top_module_in_),
    .out (nbits13_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits13_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits13_compare
  (
    input logic [12:0] in_
  );

    nbits13_ref_module_in_ = in_;
    nbits13_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits13_top_module_in_, nbits13_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits13_top_module_out, nbits13_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_2_nbits13_directed
  //----------------------------------------------------------------------

  task test_case_2_nbits13_directed();
    $display( "\ntest_case_2_nbits13_directed" );
    t.reset_sequence();

    nbits13_compare( 13'b0_0000_0000_0000 );
    nbits13_compare( 13'b0_0000_0000_0001 );
    nbits13_compare( 13'b0_0000_0000_0010 );
    nbits13_compare( 13'b0_0000_0000_0100 );
    nbits13_compare( 13'b0_0000_0000_1000 );
    nbits13_compare( 13'b0_0000_0001_0000 );
    nbits13_compare( 13'b0_0000_0010_0000 );
    nbits13_compare( 13'b0_0000_0100_0000 );
    nbits13_compare( 13'b0_0000_1000_0000 );
    nbits13_compare( 13'b0_0001_0000_0000 );
    nbits13_compare( 13'b0_0010_0000_0000 );
    nbits13_compare( 13'b0_0100_0000_0000 );
    nbits13_compare( 13'b0_1000_0000_0000 );

    nbits13_compare( 13'b0_0000_0001_0001 );
    nbits13_compare( 13'b0_0000_0010_0010 );
    nbits13_compare( 13'b0_0000_0100_0100 );
    nbits13_compare( 13'b0_0000_1000_1000 );
    nbits13_compare( 13'b0_0001_0001_0001 );
    nbits13_compare( 13'b0_0010_0010_0010 );
    nbits13_compare( 13'b0_0100_0100_0100 );
    nbits13_compare( 13'b0_1000_1000_1000 );
    nbits13_compare( 13'b1_0001_0001_0001 );
    nbits13_compare( 13'b1_0101_0101_0101 );
    nbits13_compare( 13'b0_1010_1010_1010 );
    nbits13_compare( 13'b1_1111_1111_1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_nbits13_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_nbits13_random();
    $display( "\ntest_case_3_nbits13_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nbits13_compare( $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits4_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits13_directed();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nbits13_random();

    $write("\n");
    $finish;
  end

endmodule

