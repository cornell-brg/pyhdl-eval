//========================================================================
// Prob03p08_comb_gates_100_input_test
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

  logic [99:0] ref_module_in_;
  logic        ref_module_out_and;
  logic        ref_module_out_nand;
  logic        ref_module_out_or;
  logic        ref_module_out_nor;

  RefModule ref_module
  (
    .in_      (ref_module_in_),
    .out_and  (ref_module_out_and),
    .out_nand (ref_module_out_nand),
    .out_or   (ref_module_out_or),
    .out_nor  (ref_module_out_nor)
  );

  logic [99:0] top_module_in_;
  logic        top_module_out_and;
  logic        top_module_out_nand;
  logic        top_module_out_or;
  logic        top_module_out_nor;

  TopModule top_module
  (
    .in_      (top_module_in_),
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
    input logic [99:0] in_
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x %x %x %x", t.cycles,
                top_module_in_,
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

    compare( 100'h0_0000_0000_0000_0000_0000_0000 );
    compare( 100'h0_1234_1234_1234_1234_1234_1234 );
    compare( 100'h1_89ab_cdef_89ab_cdef_89ab_cdef );
    compare( 100'h2_4567_89ab_cdef_4567_89ab_cdef );
    compare( 100'h4_0123_4567_89ab_cdef_0123_4567 );
    compare( 100'h8_dead_beef_dead_beef_dead_beef );
    compare( 100'hf_ffff_ffff_ffff_ffff_ffff_ffff );

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

    for ( int i = 0; i < 20; i = i+1 ) begin
      compare( { $urandom(t.seed), $urandom(t.seed),
                 $urandom(t.seed), $urandom(t.seed) } );
    end

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

