//========================================================================
// Prob15p05_seq_arb_4in_weighted_test
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
  logic       ref_module_preset;
  logic [3:0] ref_module_reqs;
  logic [3:0] ref_module_grants;

  RefModule ref_module
  (
    .reset  (reset || ref_module_reset),
    .preset (ref_module_preset),
    .reqs   (ref_module_reqs),
    .grants (ref_module_grants),
    .*
  );

  logic       top_module_reset;
  logic       top_module_preset;
  logic [3:0] top_module_set_priority;
  logic [3:0] top_module_reqs;
  logic [3:0] top_module_grants;

  TopModule top_module
  (
    .reset  (reset || top_module_reset),
    .preset (top_module_preset),
    .reqs   (top_module_reqs),
    .grants (top_module_grants),
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
    input logic       preset,
    input logic [3:0] reqs
  );

    ref_module_reset  = reset;
    ref_module_preset = preset;
    ref_module_reqs   = reqs;

    top_module_reset  = reset;
    top_module_preset = preset;
    top_module_reqs   = reqs;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_reset, top_module_preset,
                top_module_reqs,  top_module_grants );

    `TEST_UTILS_CHECK_EQ( top_module_grants, ref_module_grants );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_one_req
  //----------------------------------------------------------------------

  task test_case_1_one_req();
    $display( "\ntest_case_1_one_req" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b0000 );
    compare( 0, 0, 4'b0001 );
    compare( 0, 0, 4'b0010 );
    compare( 0, 0, 4'b0100 );
    compare( 0, 0, 4'b1000 );
    compare( 0, 0, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reqs
  //----------------------------------------------------------------------

  task test_case_2_all_reqs();
    $display( "\ntest_case_2_all_reqs" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b0000 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_weighted_all
  //----------------------------------------------------------------------

  task test_case_3_weighted_all();
    $display( "\ntest_case_3_weighed_all" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_weighted_01
  //----------------------------------------------------------------------

  task test_case_4_weighted_01();
    $display( "\ntest_case_4_weighed_01" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b0011 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_weighted_23
  //----------------------------------------------------------------------

  task test_case_5_weighted_23();
    $display( "\ntest_case_5_weighed_23" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1100 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_weighted_12
  //----------------------------------------------------------------------

  task test_case_6_weighted_12();
    $display( "\ntest_case_6_weighed_12" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0110 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_weighted_mixed
  //----------------------------------------------------------------------

  task test_case_7_weighted_mixed();
    $display( "\ntest_case_7_weighted_mixed" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0111 );
    compare( 0, 0, 4'b1110 );
    compare( 0, 0, 4'b0000 );
    compare( 0, 0, 4'b0100 );
    compare( 0, 0, 4'b0010 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b0110 );
    compare( 0, 0, 4'b0011 );
    compare( 0, 0, 4'b1100 );
    compare( 0, 0, 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_8_preset
  //----------------------------------------------------------------------

  task test_case_8_preset();
    $display( "\ntest_case_8_preset" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 1, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_9_directed_reset
  //----------------------------------------------------------------------

  task test_case_9_directed_reset();
    $display( "\ntest_case_9_directed_reset" );
    t.reset_sequence();

    //       rs pr reqs
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 1, 0, 4'b1111 );
    compare( 1, 0, 4'b1111 );
    compare( 1, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );
    compare( 0, 0, 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_10_random
  //----------------------------------------------------------------------

  task test_case_10_random();
    $display( "\ntest_case_10_random" );
    t.reset_sequence();

    for ( int i = 0; i < 10; i = i+1 )
      compare( 0, 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_11_random_preset
  //----------------------------------------------------------------------

  task test_case_11_random_preset();
    $display( "\ntest_case_11_random_preset" );
    t.reset_sequence();

    for ( int i = 0; i < 10; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_12_random_reset
  //----------------------------------------------------------------------

  task test_case_12_random_reset();
    $display( "\ntest_case_12_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 10; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n ==  1)) test_case_1_one_req();
    if ((t.n <= 0) || (t.n ==  2)) test_case_2_all_reqs();
    if ((t.n <= 0) || (t.n ==  3)) test_case_3_weighted_all();
    if ((t.n <= 0) || (t.n ==  4)) test_case_4_weighted_01();
    if ((t.n <= 0) || (t.n ==  5)) test_case_5_weighted_23();
    if ((t.n <= 0) || (t.n ==  6)) test_case_6_weighted_12();
    if ((t.n <= 0) || (t.n ==  7)) test_case_7_weighted_mixed();
    if ((t.n <= 0) || (t.n ==  8)) test_case_8_preset();
    if ((t.n <= 0) || (t.n ==  9)) test_case_9_directed_reset();
    if ((t.n <= 0) || (t.n == 10)) test_case_10_random();
    if ((t.n <= 0) || (t.n == 11)) test_case_11_random_preset();
    if ((t.n <= 0) || (t.n == 12)) test_case_12_random_reset();

    $write("\n");
    $finish;
  end

endmodule

