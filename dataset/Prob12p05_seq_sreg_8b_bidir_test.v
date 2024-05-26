//========================================================================
// Prob12p05_seq_sreg_8b_bidir_test
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
  logic       ref_module_en;
  logic       ref_module_ld;
  logic [7:0] ref_module_pin;
  logic       ref_module_op;
  logic [7:0] ref_module_pout;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .en    (ref_module_en),
    .ld    (ref_module_ld),
    .pin   (ref_module_pin),
    .op    (ref_module_op),
    .pout  (ref_module_pout),
    .*
  );

  logic       top_module_reset;
  logic       top_module_en;
  logic       top_module_ld;
  logic [7:0] top_module_pin;
  logic       top_module_op;
  logic [7:0] top_module_pout;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .en    (top_module_en),
    .ld    (top_module_ld),
    .pin   (top_module_pin),
    .op    (top_module_op),
    .pout  (top_module_pout),
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
    input logic       en,
    input logic       ld,
    input logic [7:0] pin,
    input logic       op
  );

    ref_module_reset = reset;
    ref_module_en    = en;
    ref_module_ld    = ld;
    ref_module_pin   = pin;
    ref_module_op    = op;

    top_module_reset = reset;
    top_module_en    = en;
    top_module_ld    = ld;
    top_module_pin   = pin;
    top_module_op    = op;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x", t.cycles,
                top_module_reset, top_module_en, top_module_ld,
                top_module_pin, top_module_op, top_module_pout );

    `TEST_UTILS_CHECK_EQ( top_module_pout, ref_module_pout );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_single_ld_left
  //----------------------------------------------------------------------

  task test_case_1_single_ld_left();
    $display( "\ntest_case_1_single_ld_left" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1101_0110, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_single_ld_right
  //----------------------------------------------------------------------

  task test_case_2_single_ld_right();
    $display( "\ntest_case_2_single_ld_right" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 1, 8'b1101_0110, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_multi_ld_left
  //----------------------------------------------------------------------

  task test_case_3_multi_ld_left();
    $display( "\ntest_case_3_multi_ld_left" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1101_0110, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b0110_0101, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1100_1001, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1111_1111, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_multi_ld_right
  //----------------------------------------------------------------------

  task test_case_4_multi_ld_right();
    $display( "\ntest_case_4_multi_ld_right" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 1, 8'b1101_0110, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 1, 8'b0110_0101, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 1, 8'b1100_1001, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 1, 8'b1111_1111, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );
    compare( 0, 0, 0, 8'b0000_0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_enable
  //----------------------------------------------------------------------

  task test_case_5_enable();
    $display( "\ntest_case_5_enable" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1111_1111, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_multi_reset
  //----------------------------------------------------------------------

  task test_case_6_multi_reset();
    $display( "\ntest_case_6_multi_reset" );
    t.reset_sequence();

    //       rs en ld pin          op
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1111_1111, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random
  //----------------------------------------------------------------------

  task test_case_7_random();
    $display( "\ntest_case_7_random" );
    t.reset_sequence();

    for ( int i = 0; i < 60; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed),
                  $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_single_ld_left();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_single_ld_right();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_multi_ld_left();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_multi_ld_right();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_enable();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_multi_reset();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_random();

    $write("\n");
    $finish;
  end

endmodule

