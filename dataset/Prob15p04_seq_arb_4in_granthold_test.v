//========================================================================
// Prob15p04_seq_arb_4in_granthold_test
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
  logic [3:0] ref_module_reqs;
  logic [3:0] ref_module_holds;
  logic [3:0] ref_module_grants;

  RefModule ref_module
  (
    .reset  (reset || ref_module_reset),
    .reqs   (ref_module_reqs),
    .holds  (ref_module_holds),
    .grants (ref_module_grants),
    .*
  );

  logic       top_module_reset;
  logic [3:0] top_module_reqs;
  logic [3:0] top_module_holds;
  logic [3:0] top_module_grants;

  TopModule top_module
  (
    .reset  (reset || top_module_reset),
    .reqs   (top_module_reqs),
    .holds  (top_module_holds),
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
    input logic [3:0] reqs,
    input logic [3:0] holds
  );

    ref_module_reset = reset;
    ref_module_reqs  = reqs;
    ref_module_holds = holds;

    top_module_reset = reset;
    top_module_reqs  = reqs;
    top_module_holds = holds;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_reset, top_module_reqs,
                top_module_holds, top_module_grants );

    `TEST_UTILS_CHECK_EQ( top_module_grants, ref_module_grants );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_one_req
  //----------------------------------------------------------------------

  task test_case_1_one_req();
    $display( "\ntest_case_1_one_req" );
    t.reset_sequence();

    //       rs reqs     holds
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b0001, 4'b0000 );
    compare( 0, 4'b0010, 4'b0000 );
    compare( 0, 4'b0100, 4'b0000 );
    compare( 0, 4'b1000, 4'b0000 );
    compare( 0, 4'b0000, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reqs
  //----------------------------------------------------------------------

  task test_case_2_all_reqs();
    $display( "\ntest_case_2_all_reqs" );
    t.reset_sequence();

    //       rs reqs     holds
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_example
  //----------------------------------------------------------------------

  task test_case_3_example();
    $display( "\ntest_case_3_example" );
    t.reset_sequence();

    //       rs reqs     holds
    compare( 0, 4'b1111, 4'b0001 );
    compare( 0, 4'b1111, 4'b0001 );
    compare( 0, 4'b1111, 4'b0001 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b1000 );
    compare( 0, 4'b1111, 4'b1000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b0000, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_directed_reset
  //----------------------------------------------------------------------

  task test_case_4_directed_reset();
    $display( "\ntest_case_4_directed_reset" );
    t.reset_sequence();

    //       rs reqs     holds
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 1, 4'b1111, 4'b0000 );
    compare( 1, 4'b1111, 4'b0000 );
    compare( 1, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );
    compare( 0, 4'b1111, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random_reset
  //----------------------------------------------------------------------

  task test_case_6_random_reset();
    $display( "\ntest_case_6_random_reset" );
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_one_req();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_all_reqs();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_example();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_directed_reset();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random_reset();

    $write("\n");
    $finish;
  end

endmodule

