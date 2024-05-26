//========================================================================
// Prob13p06_seq_count_3b_bin_var_dn_test
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

  logic       ref_module_ld;
  logic [2:0] ref_module_in_;
  logic [2:0] ref_module_out;
  logic       ref_module_done;

  RefModule ref_module
  (
    .ld   (ref_module_ld),
    .in_  (ref_module_in_),
    .out  (ref_module_out),
    .done (ref_module_done),
    .*
  );

  logic       top_module_ld;
  logic [2:0] top_module_in_;
  logic [2:0] top_module_out;
  logic       top_module_done;

  TopModule top_module
  (
    .ld   (top_module_ld),
    .in_  (ref_module_in_),
    .out  (top_module_out),
    .done (top_module_done),
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
    input logic       ld,
    input logic [2:0] in_,
    input logic       check_output
  );

    ref_module_ld  = ld;
    ref_module_in_ = in_;

    top_module_ld  = ld;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_ld,  top_module_in_,
                top_module_out, top_module_done );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_out,  ref_module_out  );
      `TEST_UTILS_CHECK_EQ( top_module_done, ref_module_done );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_done
  //----------------------------------------------------------------------

  task test_case_1_done();
    $display( "\ntest_case_1_done" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_count4
  //----------------------------------------------------------------------

  task test_case_2_count4();
    $display( "\ntest_case_2_count4" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 4, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_count7
  //----------------------------------------------------------------------

  task test_case_3_count7();
    $display( "\ntest_case_3_count7" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 7, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_multi_ld
  //----------------------------------------------------------------------

  task test_case_4_multi_ld();
    $display( "\ntest_case_4_multi_ld" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    compare( 1, 5, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 1, 3, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );
    compare( 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random
  //----------------------------------------------------------------------

  task test_case_5_random();
    $display( "\ntest_case_5_random" );
    t.reset_sequence();

    compare( 1, 0, 0 ); // do not check output
    for ( int i = 0; i < 50; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_done();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_count4();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_count7();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_multi_ld();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random();

    $write("\n");
    $finish;
  end

endmodule

