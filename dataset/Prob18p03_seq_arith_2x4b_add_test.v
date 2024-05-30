//========================================================================
// Prob18p03_seq_arith_2x4b_add_test
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
  logic [3:0] ref_module_in0;
  logic [3:0] ref_module_in1;
  logic [3:0] ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .in0   (ref_module_in0),
    .in1   (ref_module_in1),
    .out   (ref_module_out),
    .*
  );

  logic       top_module_reset;
  logic [3:0] top_module_in0;
  logic [3:0] top_module_in1;
  logic [3:0] top_module_out;

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
    input logic       reset,
    input logic [3:0] in0,
    input logic [3:0] in1
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

    //       rs i0       i1
    compare( 0, 4'b0000, 4'b0000 ); // 0000_0000 + 0000_0000
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b0001, 4'b0001 ); // 0000_0001 + 0000_0001
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b0010, 4'b0011 ); // 0000_0010 + 0000_0011
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b0011, 4'b0010 ); // 0000_0011 + 0000_0010
    compare( 0, 4'b0000, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_large
  //----------------------------------------------------------------------

  task test_case_2_large();
    $display( "\ntest_case_2_large" );
    t.reset_sequence();

    //       rs i0       i1
    compare( 0, 4'b0000, 4'b0000 ); // 1011_0000 + 0100_0000
    compare( 0, 4'b1011, 4'b0100 );
    compare( 0, 4'b0000, 4'b0000 ); // 1100_0000 + 0011_0000
    compare( 0, 4'b1100, 4'b0011 );
    compare( 0, 4'b0000, 4'b0000 ); // 1101_0000 + 0010_0000
    compare( 0, 4'b1101, 4'b0010 );
    compare( 0, 4'b0000, 4'b0000 ); // 0100_0000 + 0100_000
    compare( 0, 4'b0100, 4'b0100 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_carry
  //----------------------------------------------------------------------

  task test_case_3_carry();
    $display( "\ntest_case_3_carry" );
    t.reset_sequence();

    //       rs i0       i1
    compare( 0, 4'b1000, 4'b1000 ); // 0000_1000 + 0000_1000
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b1000, 4'b1000 ); // 0000_1000 + 0001_1000
    compare( 0, 4'b0000, 4'b0001 );
    compare( 0, 4'b1000, 4'b1000 ); // 0001_1000 + 0000_1000
    compare( 0, 4'b0001, 4'b0000 );
    compare( 0, 4'b1111, 4'b0001 ); // 0111_1111 + 0000_0001
    compare( 0, 4'b0111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_overflow
  //----------------------------------------------------------------------

  task test_case_4_overflow();
    $display( "\ntest_case_4_overflow" );
    t.reset_sequence();

    //       rs i0       i1
    compare( 0, 4'b0000, 4'b0000 ); // 1111_0000 + 0001_0000
    compare( 0, 4'b1111, 4'b0001 );
    compare( 0, 4'b0000, 4'b0000 ); // 1100_0000 + 0111_0000
    compare( 0, 4'b1100, 4'b0111 );
    compare( 0, 4'b0000, 4'b0000 ); // 1000_0000 + 1000_0000
    compare( 0, 4'b1000, 4'b1000 );
    compare( 0, 4'b1111, 4'b0001 ); // 1111_1111 + 0000_0001
    compare( 0, 4'b1111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_directed_reset
  //----------------------------------------------------------------------

  task test_case_5_directed_reset();
    $display( "\ntest_case_5_directed_reset" );
    t.reset_sequence();

    //       rs i0       i1
    compare( 0, 4'b1111, 4'b0001 ); // 1111_1111 + 0000_0001
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0001 ); // 1111_1111 + 0000_0001
    compare( 1, 4'b0000, 4'b0000 ); // reset
    compare( 1, 4'b0000, 4'b0000 ); // reset
    compare( 1, 4'b0000, 4'b0000 ); // reset
    compare( 0, 4'b1111, 4'b0001 ); // 1111_1111 + 0000_0001
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0001 ); // 1111_1111 + 0000_0001
    compare( 0, 4'b1111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random
  //----------------------------------------------------------------------

  task test_case_6_random();
    $display( "\ntest_case_6_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random_reset
  //----------------------------------------------------------------------

  task test_case_7_random_reset();
    $display( "\ntest_case_7_random_reset" );
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
    if ((t.n <= 0) || (t.n == 3)) test_case_3_carry();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_overflow();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_directed_reset();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_random_reset();

    $write("\n");
    $finish;
  end

endmodule

