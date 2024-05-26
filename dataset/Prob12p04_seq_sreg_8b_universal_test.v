//========================================================================
// Prob12p04_seq_sreg_8b_universal_test
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
  logic       ref_module_sin;
  logic [7:0] ref_module_pout;
  logic       ref_module_sout;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .en    (ref_module_en),
    .ld    (ref_module_ld),
    .pin   (ref_module_pin),
    .sin   (ref_module_sin),
    .pout  (ref_module_pout),
    .sout  (ref_module_sout),
    .*
  );

  logic       top_module_reset;
  logic       top_module_en;
  logic       top_module_ld;
  logic [7:0] top_module_pin;
  logic       top_module_sin;
  logic [7:0] top_module_pout;
  logic       top_module_sout;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .en    (top_module_en),
    .ld    (top_module_ld),
    .pin   (top_module_pin),
    .sin   (top_module_sin),
    .pout  (top_module_pout),
    .sout  (top_module_sout),
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
    input logic       sin
  );

    ref_module_reset = reset;
    ref_module_en    = en;
    ref_module_ld    = ld;
    ref_module_pin   = pin;
    ref_module_sin   = sin;

    top_module_reset = reset;
    top_module_en    = en;
    top_module_ld    = ld;
    top_module_pin   = pin;
    top_module_sin   = sin;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x %x", t.cycles,
                top_module_reset, top_module_en,
                top_module_ld, top_module_pin, top_module_sin,
                top_module_pout, top_module_sout );

    `TEST_UTILS_CHECK_EQ( top_module_pout, ref_module_pout );
    `TEST_UTILS_CHECK_EQ( top_module_sout, ref_module_sout );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_single_ld
  //----------------------------------------------------------------------

  task test_case_1_single_ld();
    $display( "\ntest_case_1_single_ld" );
    t.reset_sequence();

    //       rs en ld pin          sin
    compare( 0, 0, 0, 8'b0000_0000, 0 ); //  0: 0000_0000
    compare( 0, 0, 1, 8'b1101_0110, 0 ); //  1: 0000_0000
    compare( 0, 1, 0, 8'b0000_0000, 0 ); //  2: 1101_0110
    compare( 0, 1, 0, 8'b0000_0000, 1 ); //  3: 1010_1100
    compare( 0, 1, 0, 8'b0000_0000, 1 ); //  4: 0101_1001
    compare( 0, 1, 0, 8'b0000_0000, 0 ); //  5: 1011_0011
    compare( 0, 1, 0, 8'b0000_0000, 1 ); //  6: 0110_0110
    compare( 0, 1, 0, 8'b0000_0000, 1 ); //  7: 1100_1101
    compare( 0, 1, 0, 8'b0000_0000, 0 ); //  8: 1001_1011
    compare( 0, 1, 0, 8'b0000_0000, 1 ); //  9: 0011_0110
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 0110_1101
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 1101_1010
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 1011_0100
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 0110_1000
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 1101_0000
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 1010_0000
    compare( 0, 1, 0, 8'b0000_0000, 0 ); // 10: 0100_0000
    compare( 0, 0, 0, 8'b0000_0000, 0 ); // 11: 0100_0000
    compare( 0, 0, 0, 8'b0000_0000, 0 ); // 12: 0100_0000

  endtask

  //----------------------------------------------------------------------
  // test_case_2_multi_ld
  //----------------------------------------------------------------------

  task test_case_2_multi_ld();
    $display( "\ntest_case_2_multi_ld" );
    t.reset_sequence();

    //       rs en ld pin          sin
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1101_0110, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
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
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
    compare( 0, 1, 0, 8'b0000_0000, 1 );
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
  // test_case_3_enable
  //----------------------------------------------------------------------

  task test_case_3_enable();
    $display( "\ntest_case_3_enable" );
    t.reset_sequence();

    //       rs en ld pin          sin
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
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs en ld pin          sin
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 1, 8'b1111_1111, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 1, 0, 0, 8'b0000_0000, 0 );
    compare( 1, 0, 0, 8'b0000_0000, 0 );
    compare( 1, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 1, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );
    compare( 0, 0, 0, 8'b0000_0000, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_single_ld();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_multi_ld();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_enable();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

