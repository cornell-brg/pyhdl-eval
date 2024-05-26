//========================================================================
// Prob12p03_seq_sreg_8b_sipo_test
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
  logic       ref_module_sin;
  logic [7:0] ref_module_pout;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .en    (ref_module_en),
    .sin   (ref_module_sin),
    .pout  (ref_module_pout),
    .*
  );

  logic       top_module_reset;
  logic       top_module_en;
  logic       top_module_sin;
  logic [7:0] top_module_pout;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
    .en    (top_module_en),
    .sin   (top_module_sin),
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
    input logic reset,
    input logic en,
    input logic sin
  );

    ref_module_reset = reset;
    ref_module_en    = en;
    ref_module_sin   = sin;

    top_module_reset = reset;
    top_module_en    = en;
    top_module_sin   = sin;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_reset, top_module_en,
                top_module_sin,   top_module_pout );

    `TEST_UTILS_CHECK_EQ( top_module_pout, ref_module_pout );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_single_one
  //----------------------------------------------------------------------

  task test_case_1_single_one();
    $display( "\ntest_case_1_single_one" );
    t.reset_sequence();

    //       rs en si
    compare( 0, 0, 0 ); //  0: 0000_0000
    compare( 0, 1, 1 ); //  1: 0000_0000
    compare( 0, 1, 0 ); //  2: 0000_0001
    compare( 0, 1, 0 ); //  3: 0000_0010
    compare( 0, 1, 0 ); //  4: 0000_0100
    compare( 0, 1, 0 ); //  5: 0000_1000
    compare( 0, 1, 0 ); //  6: 0001_0000
    compare( 0, 1, 0 ); //  7: 0010_0000
    compare( 0, 1, 0 ); //  8: 0100_0000
    compare( 0, 1, 0 ); //  9: 1000_0000
    compare( 0, 1, 0 ); // 10: 0000_0000
    compare( 0, 0, 0 ); // 11: 0000_0000
    compare( 0, 0, 0 ); // 12: 0000_0000

  endtask

  //----------------------------------------------------------------------
  // test_case_2_many_ones
  //----------------------------------------------------------------------

  task test_case_2_many_ones();
    $display( "\ntest_case_2_many_ones" );
    t.reset_sequence();

    //       rs en si
    compare( 0, 0, 0 ); //  0: 0000_0000
    compare( 0, 1, 1 ); //  1: 0000_0000
    compare( 0, 1, 0 ); //  2: 0000_0001
    compare( 0, 1, 1 ); //  3: 0000_0010
    compare( 0, 1, 0 ); //  4: 0000_0101
    compare( 0, 1, 1 ); //  5: 0000_1010
    compare( 0, 1, 0 ); //  6: 0001_0101
    compare( 0, 1, 1 ); //  7: 0010_1010
    compare( 0, 1, 0 ); //  8: 0101_0101
    compare( 0, 1, 1 ); //  9: 1010_1010
    compare( 0, 1, 0 ); // 10: 0101_0101
    compare( 0, 1, 0 ); // 11: 1010_1010
    compare( 0, 1, 0 ); // 12: 0101_0100
    compare( 0, 1, 0 ); // 13: 1010_1000

  endtask

  //----------------------------------------------------------------------
  // test_case_3_enable
  //----------------------------------------------------------------------

  task test_case_3_enable();
    $display( "\ntest_case_3_enable" );
    t.reset_sequence();

    //       rs en si
    compare( 0, 0, 0 ); //  0: 0000_0000
    compare( 0, 1, 1 ); //  1: 0000_0000
    compare( 0, 1, 1 ); //  2: 0000_0001
    compare( 0, 0, 1 ); //  3: 0000_0011
    compare( 0, 0, 1 ); //  4: 0000_0011
    compare( 0, 0, 1 ); //  5: 0000_0011
    compare( 0, 0, 1 ); //  6: 0000_0011
    compare( 0, 0, 1 ); //  7: 0000_0011
    compare( 0, 0, 1 ); //  8: 0000_0011
    compare( 0, 0, 1 ); //  9: 0000_0011
    compare( 0, 0, 1 ); // 10: 0000_0011
    compare( 0, 0, 1 ); // 11: 0000_0011
    compare( 0, 0, 1 ); // 12: 0000_0011
    compare( 0, 0, 1 ); // 13: 0000_0011

  endtask

  //----------------------------------------------------------------------
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs en si
    compare( 0, 0, 0 ); //  0: 0000_0000
    compare( 0, 1, 1 ); //  1: 0000_0000
    compare( 0, 1, 1 ); //  2: 0000_0001
    compare( 0, 1, 1 ); //  3: 0000_0011
    compare( 0, 1, 1 ); //  4: 0000_0111
    compare( 0, 1, 1 ); //  5: 0000_1111
    compare( 0, 1, 1 ); //  6: 0001_1111
    compare( 0, 1, 1 ); //  7: 0011_1111
    compare( 0, 1, 1 ); //  8: 0111_1111
    compare( 0, 1, 1 ); //  9: 1111_1111
    compare( 0, 1, 1 ); // 10: 1111_1111
    compare( 0, 1, 1 ); // 11: 1111_1111
    compare( 1, 1, 1 ); // 12: 1111_1111
    compare( 1, 1, 1 ); // 13: 0000_0000
    compare( 1, 1, 1 ); // 14: 0000_0000
    compare( 0, 1, 1 ); // 15: 0000_0000
    compare( 0, 1, 1 ); // 16: 0000_0001
    compare( 0, 1, 1 ); // 17: 0000_0011
    compare( 0, 1, 1 ); // 18: 0000_0111
    compare( 0, 1, 1 ); // 19: 0000_1111
    compare( 0, 1, 1 ); // 20: 0001_1111
    compare( 0, 1, 1 ); // 21: 0011_1111
    compare( 0, 1, 1 ); // 22: 0111_1111
    compare( 0, 1, 1 ); // 23: 1111_1111
    compare( 0, 1, 1 ); // 24: 1111_1111

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_single_one();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_many_ones();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_enable();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

