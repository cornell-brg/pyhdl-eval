//========================================================================
// Prob13p04_seq_count_3b_bin_up_dn_test
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
  logic       ref_module_op;
  logic [2:0] ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .op    (ref_module_op),
    .out   (ref_module_out),
    .*
  );

  logic       top_module_reset;
  logic       top_module_op;
  logic [2:0] top_module_out;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .op    (top_module_op),
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
    input logic op
  );

    ref_module_reset = reset;
    ref_module_op    = op;

    top_module_reset = reset;
    top_module_op    = op;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_reset, top_module_op, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_up
  //----------------------------------------------------------------------

  task test_case_1_up();
    $display( "\ntest_case_1_up" );
    t.reset_sequence();

    for ( int i = 0; i < 5; i = i+1 )
      compare( 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_up_wraparound
  //----------------------------------------------------------------------

  task test_case_2_up_wraparound();
    $display( "\ntest_case_2_up_wraparound" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_dn
  //----------------------------------------------------------------------

  task test_case_3_dn();
    $display( "\ntest_case_3_dn" );
    t.reset_sequence();

    for ( int i = 0; i < 5; i = i+1 )
      compare( 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_dn_wraparound
  //----------------------------------------------------------------------

  task test_case_4_dn_wraparound();
    $display( "\ntest_case_4_dn_wraparound" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_up_dn
  //----------------------------------------------------------------------

  task test_case_5_up_dn();
    $display( "\ntest_case_5_up_dn" );
    t.reset_sequence();

    //       rs op
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_directed_reset
  //----------------------------------------------------------------------

  task test_case_6_directed_reset();
    $display( "\ntest_case_6_directed_reset" );
    t.reset_sequence();

    //       rs op
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 1, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );
    compare( 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random
  //----------------------------------------------------------------------

  task test_case_7_random();
    $display( "\ntest_case_7_random" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_8_random_reset
  //----------------------------------------------------------------------

  task test_case_8_random_reset();
    $display( "\ntest_case_8_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_up();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_up_wraparound();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_dn();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_dn_wraparound();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_up_dn();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_directed_reset();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_random();
    if ((t.n <= 0) || (t.n == 8)) test_case_8_random_reset();

    $write("\n");
    $finish;
  end

endmodule

