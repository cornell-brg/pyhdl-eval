//========================================================================
// Prob09p08_comb_param_rotator_test
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
  logic [1:0] nbits4_ref_module_amt;
  logic       nbits4_ref_module_op;
  logic [3:0] nbits4_ref_module_out;

  RefModule
  #(
    .nbits (4)
  )
  nbits4_ref_module
  (
    .in_ (nbits4_ref_module_in_),
    .amt (nbits4_ref_module_amt),
    .op  (nbits4_ref_module_op),
    .out (nbits4_ref_module_out)
  );

  logic [3:0] nbits4_top_module_in_;
  logic [1:0] nbits4_top_module_amt;
  logic       nbits4_top_module_op;
  logic [3:0] nbits4_top_module_out;

  TopModule
  #(
    .nbits (4)
  )
  nbits4_top_module
  (
    .in_ (nbits4_top_module_in_),
    .amt (nbits4_top_module_amt),
    .op  (nbits4_top_module_op),
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
    input logic [3:0] in_,
    input logic [1:0] amt,
    input logic       op
  );

    nbits4_ref_module_in_ = in_;
    nbits4_ref_module_amt = amt;
    nbits4_ref_module_op  = op;

    nbits4_top_module_in_ = in_;
    nbits4_top_module_amt = amt;
    nbits4_top_module_op  = op;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                nbits4_top_module_in_, nbits4_top_module_amt,
                nbits4_top_module_op,  nbits4_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits4_top_module_out, nbits4_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_nbits4_left_shift
  //----------------------------------------------------------------------

  task test_case_1_nbits4_left_shift();
    $display( "\ntest_case_1_nbits4_left_shift" );
    t.reset_sequence();

    nbits4_compare( 4'b1101, 0, 0 );
    nbits4_compare( 4'b1101, 1, 0 );
    nbits4_compare( 4'b1101, 2, 0 );
    nbits4_compare( 4'b1101, 3, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_nbits4_right_shift
  //----------------------------------------------------------------------

  task test_case_2_nbits4_right_shift();
    $display( "\ntest_case_2_nbits4_right_shift" );
    t.reset_sequence();

    nbits4_compare( 4'b1101, 0, 1 );
    nbits4_compare( 4'b1101, 1, 1 );
    nbits4_compare( 4'b1101, 2, 1 );
    nbits4_compare( 4'b1101, 3, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_nbits4_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_nbits4_random();
    $display( "\ntest_case_3_nbits4_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nbits4_compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // nbits8: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [7:0] nbits8_ref_module_in_;
  logic [2:0] nbits8_ref_module_amt;
  logic       nbits8_ref_module_op;
  logic [7:0] nbits8_ref_module_out;

  RefModule
  #(
    .nbits (8)
  )
  nbits8_ref_module
  (
    .in_ (nbits8_ref_module_in_),
    .amt (nbits8_ref_module_amt),
    .op  (nbits8_ref_module_op),
    .out (nbits8_ref_module_out)
  );

  logic [7:0] nbits8_top_module_in_;
  logic [2:0] nbits8_top_module_amt;
  logic       nbits8_top_module_op;
  logic [7:0] nbits8_top_module_out;

  TopModule
  #(
    .nbits (8)
  )
  nbits8_top_module
  (
    .in_ (nbits8_top_module_in_),
    .amt (nbits8_top_module_amt),
    .op  (nbits8_top_module_op),
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
    input logic [7:0] in_,
    input logic [2:0] amt,
    input logic       op
  );

    nbits8_ref_module_in_ = in_;
    nbits8_ref_module_amt = amt;
    nbits8_ref_module_op  = op;

    nbits8_top_module_in_ = in_;
    nbits8_top_module_amt = amt;
    nbits8_top_module_op  = op;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                nbits8_top_module_in_, nbits8_top_module_amt,
                nbits8_top_module_op,  nbits8_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits8_top_module_out, nbits8_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_4_nbits8_left_shift
  //----------------------------------------------------------------------

  task test_case_4_nbits8_left_shift();
    $display( "\ntest_case_4_nbits8_left_shift" );
    t.reset_sequence();

    nbits8_compare( 8'b0101_1101, 0, 0 );
    nbits8_compare( 8'b0101_1101, 1, 0 );
    nbits8_compare( 8'b0101_1101, 2, 0 );
    nbits8_compare( 8'b0101_1101, 3, 0 );
    nbits8_compare( 8'b0101_1101, 4, 0 );
    nbits8_compare( 8'b0101_1101, 5, 0 );
    nbits8_compare( 8'b0101_1101, 6, 0 );
    nbits8_compare( 8'b0101_1101, 7, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_nbits8_right_shift
  //----------------------------------------------------------------------

  task test_case_5_nbits8_right_shift();
    $display( "\ntest_case_5_nbits8_right_shift" );
    t.reset_sequence();

    nbits8_compare( 8'b1101_0101, 0, 1 );
    nbits8_compare( 8'b1101_0101, 1, 1 );
    nbits8_compare( 8'b1101_0101, 2, 1 );
    nbits8_compare( 8'b1101_0101, 3, 1 );
    nbits8_compare( 8'b1101_0101, 4, 1 );
    nbits8_compare( 8'b1101_0101, 5, 1 );
    nbits8_compare( 8'b1101_0101, 6, 1 );
    nbits8_compare( 8'b1101_0101, 7, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_nbits8_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_6_nbits8_random();
    $display( "\ntest_case_6_nbits8_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nbits8_compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits4_left_shift();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits4_right_shift();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nbits4_random();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_nbits8_left_shift();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_nbits8_right_shift();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_nbits8_random();

    $write("\n");
    $finish;
  end

endmodule

