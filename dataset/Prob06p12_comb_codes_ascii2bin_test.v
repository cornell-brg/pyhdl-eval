//========================================================================
// Prob06p12_comb_codes_ascii2bin_test
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

  logic [15:0] ref_module_in_;
  logic [ 3:0] ref_module_out;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .out (ref_module_out)
  );

  logic [15:0] top_module_in_;
  logic [ 3:0] top_module_out;

  TopModule top_module
  (
    .in_ (top_module_in_),
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
    input logic [15:0] in_
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_in_, top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_valid
  //----------------------------------------------------------------------

  task test_case_1_valid();
    $display( "\ntest_case_1_valid" );
    t.reset_sequence();

    compare( 16'h3030 );
    compare( 16'h3031 );
    compare( 16'h3032 );
    compare( 16'h3033 );

    compare( 16'h3034 );
    compare( 16'h3035 );
    compare( 16'h3036 );
    compare( 16'h3037 );

    compare( 16'h3038 );
    compare( 16'h3039 );
    compare( 16'h3130 );
    compare( 16'h3131 );

    compare( 16'h3132 );
    compare( 16'h3133 );
    compare( 16'h3134 );
    compare( 16'h3135 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_invalid
  //----------------------------------------------------------------------

  task test_case_2_invalid();
    $display( "\ntest_case_2_invalid" );
    t.reset_sequence();

    compare( 16'h0000 );
    compare( 16'h0001 );
    compare( 16'h0002 );
    compare( 16'h0003 );
    compare( 16'h0004 );
    compare( 16'h0005 );
    compare( 16'h0006 );
    compare( 16'h0007 );
    compare( 16'h0008 );
    compare( 16'h0009 );
    compare( 16'h0010 );

    compare( 16'h1010 );
    compare( 16'h2020 );
    compare( 16'h4040 );
    compare( 16'h5050 );
    compare( 16'h6060 );
    compare( 16'h7070 );
    compare( 16'h8080 );
    compare( 16'h9090 );
    compare( 16'ha0a0 );
    compare( 16'hb0b0 );
    compare( 16'hc0c0 );
    compare( 16'hd0d0 );
    compare( 16'he0e0 );
    compare( 16'hf0f0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_random();
    $display( "\ntest_case_3_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_valid();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_invalid();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random();

    $write("\n");
    $finish;
  end

endmodule

