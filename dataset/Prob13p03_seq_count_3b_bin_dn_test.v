//========================================================================
// Prob13p03_seq_count_3b_bin_dn_test
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
  logic [2:0] ref_module_out;

  RefModule ref_module
  (
    .reset (reset || ref_module_reset),
    .out   (ref_module_out),
    .*
  );

  logic       top_module_reset;
  logic [2:0] top_module_out;

  TopModule top_module
  (
    .reset (reset || top_module_reset),
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
    input logic reset
  );

    ref_module_reset = reset;
    top_module_reset = reset;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_reset, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_basic
  //----------------------------------------------------------------------

  task test_case_1_basic();
    $display( "\ntest_case_1_basic" );
    t.reset_sequence();

    for ( int i = 0; i < 5; i = i+1 )
      compare( 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_wraparound
  //----------------------------------------------------------------------

  task test_case_2_wraparound();
    $display( "\ntest_case_2_wraparound" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_directed_reset
  //----------------------------------------------------------------------

  task test_case_3_directed_reset();
    $display( "\ntest_case_3_directed_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 4; i = i+1 )
      compare( 0 );

    for ( int i = 0; i < 3; i = i+1 )
      compare( 1 );

    for ( int i = 0; i < 6; i = i+1 )
      compare( 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random_reset
  //----------------------------------------------------------------------

  task test_case_4_random_reset();
    $display( "\ntest_case_4_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_basic();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_wraparound();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_directed_reset();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random_reset();

    $write("\n");
    $finish;
  end

endmodule

