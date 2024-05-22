//========================================================================
// Prob09p06_comb_param_dec_test
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
  // nbits8: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [2:0] nbits8_ref_module_in_;
  logic [7:0] nbits8_ref_module_out;

  RefModule
  #(
    .nbits (8)
  )
  nbits8_ref_module
  (
    .in_ (nbits8_ref_module_in_),
    .out (nbits8_ref_module_out)
  );

  logic [2:0] nbits8_top_module_in_;
  logic [7:0] nbits8_top_module_out;

  TopModule
  #(
    .nbits (8)
  )
  nbits8_top_module
  (
    .in_ (nbits8_top_module_in_),
    .out (nbits8_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits8_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits8_compare
  (
    input logic [2:0] in_
  );

    nbits8_ref_module_in_ = in_;
    nbits8_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits8_top_module_in_, nbits8_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits8_top_module_out, nbits8_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_nbits8_directed
  //----------------------------------------------------------------------

  task test_case_1_nbits8_directed();
    $display( "\ntest_case_1_nbits8_directed" );
    t.reset_sequence();

    nbits8_compare( 3'b000 );
    nbits8_compare( 3'b001 );
    nbits8_compare( 3'b010 );
    nbits8_compare( 3'b011 );
    nbits8_compare( 3'b100 );
    nbits8_compare( 3'b101 );
    nbits8_compare( 3'b110 );
    nbits8_compare( 3'b111 );

  endtask

  //----------------------------------------------------------------------
  // nbits10: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [3:0] nbits10_ref_module_in_;
  logic [9:0] nbits10_ref_module_out;

  RefModule
  #(
    .nbits (10)
  )
  nbits10_ref_module
  (
    .in_ (nbits10_ref_module_in_),
    .out (nbits10_ref_module_out)
  );

  logic [3:0] nbits10_top_module_in_;
  logic [9:0] nbits10_top_module_out;

  TopModule
  #(
    .nbits (10)
  )
  nbits10_top_module
  (
    .in_ (nbits10_top_module_in_),
    .out (nbits10_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits10_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits10_compare
  (
    input logic [3:0] in_
  );

    nbits10_ref_module_in_ = in_;
    nbits10_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits10_top_module_in_, nbits10_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits10_top_module_out, nbits10_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_2_nbits10_valid
  //----------------------------------------------------------------------

  task test_case_2_nbits10_valid();
    $display( "\ntest_case_2_nbits10_valid" );
    t.reset_sequence();

    nbits10_compare( 4'b0000 );
    nbits10_compare( 4'b0001 );
    nbits10_compare( 4'b0010 );
    nbits10_compare( 4'b0011 );
    nbits10_compare( 4'b0100 );
    nbits10_compare( 4'b0101 );
    nbits10_compare( 4'b0110 );
    nbits10_compare( 4'b0111 );
    nbits10_compare( 4'b1000 );
    nbits10_compare( 4'b1001 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_nbits10_invalid
  //----------------------------------------------------------------------

  task test_case_3_nbits10_invalid();
    $display( "\ntest_case_3_nbits10_invalid" );
    t.reset_sequence();

    nbits10_compare( 4'b1010 );
    nbits10_compare( 4'b1011 );
    nbits10_compare( 4'b1100 );
    nbits10_compare( 4'b1101 );
    nbits10_compare( 4'b1110 );
    nbits10_compare( 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits8_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits10_valid();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nbits10_invalid();

    $write("\n");
    $finish;
  end

endmodule

