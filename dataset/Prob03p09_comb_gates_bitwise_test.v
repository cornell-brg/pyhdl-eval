//========================================================================
// Prob03p09_comb_gates_bitwise_test
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

  logic [3:0] ref_module_in0;
  logic [3:0] ref_module_in1;
  logic [3:0] ref_module_out_and;
  logic [3:0] ref_module_out_nand;
  logic [3:0] ref_module_out_or;
  logic [3:0] ref_module_out_nor;

  RefModule ref_module
  (
    .in0      (ref_module_in0),
    .in1      (ref_module_in1),
    .out_and  (ref_module_out_and),
    .out_nand (ref_module_out_nand),
    .out_or   (ref_module_out_or),
    .out_nor  (ref_module_out_nor)
  );

  logic [3:0] top_module_in0;
  logic [3:0] top_module_in1;
  logic [3:0] top_module_out_and;
  logic [3:0] top_module_out_nand;
  logic [3:0] top_module_out_or;
  logic [3:0] top_module_out_nor;

  TopModule top_module
  (
    .in0      (top_module_in0),
    .in1      (top_module_in1),
    .out_and  (top_module_out_and),
    .out_nand (top_module_out_nand),
    .out_or   (top_module_out_or),
    .out_nor  (top_module_out_nor)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [3:0] in0,
    input logic [3:0] in1
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;

    top_module_in0 = in0;
    top_module_in1 = in1;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x %x %x", t.cycles,
                top_module_in0,     top_module_in1,
                top_module_out_and, top_module_out_nand,
                top_module_out_or,  top_module_out_nor );

    `TEST_UTILS_CHECK_EQ( top_module_out_and,  ref_module_out_and  );
    `TEST_UTILS_CHECK_EQ( top_module_out_nand, ref_module_out_nand );
    `TEST_UTILS_CHECK_EQ( top_module_out_or,   ref_module_out_or   );
    `TEST_UTILS_CHECK_EQ( top_module_out_nor,  ref_module_out_nor  );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 4'b0000, 4'b0000 );
    compare( 4'b0000, 4'b1111 );
    compare( 4'b1111, 4'b0000 );
    compare( 4'b1111, 4'b1111 );
    compare( 4'b1100, 4'b1010 );
    compare( 4'b0011, 4'b0101 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_2_random();
    $display( "\ntest_case_2_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_random();

    $write("\n");
    $finish;
  end

endmodule

