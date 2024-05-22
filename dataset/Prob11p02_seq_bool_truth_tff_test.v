//========================================================================
// Prob11p02_seq_bool_truth_tff_test
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

  logic ref_module_a;
  logic ref_module_b;
  logic ref_module_q;

  RefModule ref_module
  (
    .a (ref_module_a),
    .b (ref_module_b),
    .q (ref_module_q),
    .*
  );

  logic top_module_a;
  logic top_module_b;
  logic top_module_q;

  TopModule top_module
  (
    .a (top_module_a),
    .b (top_module_b),
    .q (top_module_q),
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
    input logic a,
    input logic b,
    input logic check_output
  );

    ref_module_a = a;
    ref_module_b = b;

    top_module_a = a;
    top_module_b = b;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_a, top_module_b, top_module_q );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_q, ref_module_q );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    //       rs t
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 0, 0, 0 ); // do not check output
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_directed_reset
  //----------------------------------------------------------------------

  task test_case_2_directed_reset();
    $display( "\ntest_case_2_directed" );
    t.reset_sequence();

    //       rs t
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 0, 0, 0 ); // do not check output
    compare( 0, 0, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 0, 1, 1 );
    compare( 1, 1, 1 );
    compare( 1, 1, 1 );
    compare( 1, 1, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 1, 0, 1 );
    compare( 1, 0, 1 );
    compare( 1, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

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

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 0, 0, 0 ); // do not check output

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random_reset
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_4_random_reset();
    $display( "\ntest_case_4_random_reset" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 0 ); // do not check output
    compare( 0, 0, 0 ); // do not check output

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_directed_reset();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random_reset();

    $write("\n");
    $finish;
  end

endmodule

