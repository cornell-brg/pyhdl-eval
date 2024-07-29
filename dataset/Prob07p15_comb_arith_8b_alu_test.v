//========================================================================
// Prob07p15_comb_arith_8b_alu_test
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

  logic [7:0] ref_module_in0;
  logic [7:0] ref_module_in1;
  logic [2:0] ref_module_op;
  logic [7:0] ref_module_out;

  RefModule ref_module
  (
    .in0 (ref_module_in0),
    .in1 (ref_module_in1),
    .op  (ref_module_op),
    .out (ref_module_out)
  );

  logic [7:0] top_module_in0;
  logic [7:0] top_module_in1;
  logic [2:0] top_module_op;
  logic [7:0] top_module_out;

  TopModule top_module
  (
    .in0 (top_module_in0),
    .in1 (top_module_in1),
    .op  (top_module_op),
    .out (top_module_out)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [7:0] in0,
    input logic [7:0] in1,
    input logic [2:0] op
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_op  = op;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_op  = op;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_in0, top_module_in1, top_module_op,
                top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_add
  //----------------------------------------------------------------------

  task test_case_1_add();
    $display( "\ntest_case_1_add" );
    t.reset_sequence();

    compare(   0,  0, 0 );
    compare(   1,  1, 0 );
    compare(   2,  1, 0 );
    compare(   1,  2, 0 );
    compare(  13,  2, 0 );
    compare(  42,  9, 0 );
    compare(  42, 13, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_sub
  //----------------------------------------------------------------------

  task test_case_2_sub();
    $display( "\ntest_case_2_sub" );
    t.reset_sequence();

    compare(   0,  0, 1 );
    compare(   1,  1, 1 );
    compare(   2,  1, 1 );
    compare(   1,  2, 1 );
    compare(  13,  2, 1 );
    compare(  42,  9, 1 );
    compare(  42, 13, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_srl
  //----------------------------------------------------------------------

  task test_case_3_srl();
    $display( "\ntest_case_3_srl" );
    t.reset_sequence();

    compare(   0,  0, 2 );
    compare(   1,  1, 2 );
    compare(   2,  1, 2 );
    compare(   1,  2, 2 );
    compare(  13,  2, 2 );
    compare(  42,  9, 2 );
    compare(  42, 13, 2 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_sll
  //----------------------------------------------------------------------

  task test_case_4_sll();
    $display( "\ntest_case_4_sll" );
    t.reset_sequence();

    compare(   0,  0, 3 );
    compare(   1,  1, 3 );
    compare(   2,  1, 3 );
    compare(   1,  2, 3 );
    compare(  13,  2, 3 );
    compare(  42,  9, 3 );
    compare(  42, 13, 3 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_lt
  //----------------------------------------------------------------------

  task test_case_5_lt();
    $display( "\ntest_case_5_lt" );
    t.reset_sequence();

    compare(   0,  0, 4 );
    compare(   1,  1, 4 );
    compare(   2,  1, 4 );
    compare(   1,  2, 4 );
    compare(  13,  2, 4 );
    compare(  42,  9, 4 );
    compare(  42, 13, 4 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_eq
  //----------------------------------------------------------------------

  task test_case_6_eq();
    $display( "\ntest_case_6_eq" );
    t.reset_sequence();

    compare(   0,  0, 5 );
    compare(   1,  1, 5 );
    compare(   2,  1, 5 );
    compare(   1,  2, 5 );
    compare(  13,  2, 5 );
    compare(  42,  9, 5 );
    compare(  42, 13, 5 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_gt
  //----------------------------------------------------------------------

  task test_case_7_gt();
    $display( "\ntest_case_7_gt" );
    t.reset_sequence();

    compare(   0,  0, 6 );
    compare(   1,  1, 6 );
    compare(   2,  1, 6 );
    compare(   1,  2, 6 );
    compare(  13,  2, 6 );
    compare(  42,  9, 6 );
    compare(  42, 13, 6 );

  endtask

  //----------------------------------------------------------------------
  // test_case_8_invalid
  //----------------------------------------------------------------------

  task test_case_8_invalid();
    $display( "\ntest_case_8_invalid" );
    t.reset_sequence();

    compare(   0,  0, 7 );
    compare(   1,  1, 7 );
    compare(   2,  1, 7 );
    compare(   1,  2, 7 );
    compare(  13,  2, 7 );
    compare(  42,  9, 7 );
    compare(  42, 13, 7 );

  endtask

  //----------------------------------------------------------------------
  // test_case_9_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_9_random();
    $display( "\ntest_case_9_random" );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_add();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_sub();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_srl();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_sll();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_lt();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_eq();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_gt();
    if ((t.n <= 0) || (t.n == 8)) test_case_8_invalid();
    if ((t.n <= 0) || (t.n == 9)) test_case_9_random();

    $write("\n");
    $finish;
  end

endmodule

