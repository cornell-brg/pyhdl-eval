//========================================================================
// Prob18p02_seq_arith_4x1b_add_test
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

  logic ref_module_reset;
  logic ref_module_in0;
  logic ref_module_in1;
  logic ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .in0   (ref_module_in0),
    .in1   (ref_module_in1),
    .out   (ref_module_out),
    .*
  );

  logic top_module_reset;
  logic top_module_in0;
  logic top_module_in1;
  logic top_module_out;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .in0   (top_module_in0),
    .in1   (top_module_in1),
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
    input logic in0,
    input logic in1
  );

    ref_module_reset = reset;
    ref_module_in0   = in0;
    ref_module_in1   = in1;

    top_module_reset = reset;
    top_module_in0   = in0;
    top_module_in1   = in1;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_reset, top_module_in0,
                top_module_in1,   top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_small
  //----------------------------------------------------------------------

  task test_case_1_small();
    $display( "\ntest_case_1_small" );
    t.reset_sequence();

    //       rs i0 i1
    compare( 0, 0, 0 ); // 0000 + 0000
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 1, 0 ); // 0001 + 0000
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 0, 1 ); // 0010 + 0011
    compare( 0, 1, 1 );
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 1, 0 ); // 0011 + 0010
    compare( 0, 1, 1 );
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_large
  //----------------------------------------------------------------------

  task test_case_2_large();
    $display( "\ntest_case_2_large" );
    t.reset_sequence();

    //       rs i0 i1
    compare( 0, 1, 0 ); // 1011 + 0100
    compare( 0, 1, 0 );
    compare( 0, 0, 1 );
    compare( 0, 1, 0 );
    compare( 0, 0, 1 ); // 1100 + 0011
    compare( 0, 0, 1 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 ); // 1101 + 0010
    compare( 0, 0, 1 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 0, 0 ); // 0100 + 0100
    compare( 0, 0, 0 );
    compare( 0, 1, 1 );
    compare( 0, 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_overflow
  //----------------------------------------------------------------------

  task test_case_3_overflow();
    $display( "\ntest_case_3_overflow" );
    t.reset_sequence();

    //       rs i0 i1
    compare( 0, 1, 1 ); // 1111 + 0001
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 0, 1 ); // 1100 + 0111
    compare( 0, 0, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 0 );
    compare( 0, 0, 0 ); // 1000 + 1000
    compare( 0, 0, 0 );
    compare( 0, 0, 0 );
    compare( 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs i0 i1
    compare( 0, 1, 1 ); // 1111 + 0001
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 1 ); // 1111
    compare( 0, 1, 0 );
    compare( 1, 0, 0 ); // reset
    compare( 1, 0, 0 ); // reset
    compare( 1, 0, 0 ); // reset
    compare( 0, 1, 1 ); // 1111 + 0001
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 1 ); // 1111 + 0001
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );
    compare( 0, 1, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random_reset
  //----------------------------------------------------------------------

  task test_case_6_random_reset();
    $display( "\ntest_case_6_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_small();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_large();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_overflow();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random_reset();

    $write("\n");
    $finish;
  end

endmodule

