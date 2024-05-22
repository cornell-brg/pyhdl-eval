//========================================================================
// Prob10p06_seq_gates_8b_dff_byte_test
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

  logic [ 1:0] ref_module_en;
  logic [15:0] ref_module_d;
  logic [15:0] ref_module_q;

  RefModule ref_module
  (
    .en (ref_module_en),
    .d  (ref_module_d),
    .q  (ref_module_q),
    .*
  );

  logic [ 1:0] top_module_en;
  logic [15:0] top_module_d;
  logic [15:0] top_module_q;

  TopModule top_module
  (
    .en (top_module_en),
    .d  (top_module_d),
    .q  (top_module_q),
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
    input logic [ 1:0] en,
    input logic [15:0] d,
    input logic        check_output
  );

    ref_module_en = en;
    ref_module_d  = d;

    top_module_en = en;
    top_module_d  = d;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_en, top_module_d, top_module_q );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_q, ref_module_q );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_both_enabled
  //----------------------------------------------------------------------

  task test_case_1_both_enabled();
    $display( "\ntest_case_1_both_enabled" );
    t.reset_sequence();

    compare( 2'b00, 16'h0000, 0 ); // do not check output
    compare( 2'b11, 16'h0000, 1 );
    compare( 2'b11, 16'h0000, 1 ); // prev: 0 -> 0 0
    compare( 2'b11, 16'h0201, 1 ); // prev: 0 -> 1 0
    compare( 2'b11, 16'h0201, 1 ); // prev: 1 -> 1 1
    compare( 2'b11, 16'h0000, 1 ); // prev: 1 -> 0 1
    compare( 2'b11, 16'h0000, 1 );
    compare( 2'b11, 16'h0000, 1 );
    compare( 2'b11, 16'h4567, 1 );
    compare( 2'b11, 16'h89ab, 1 );
    compare( 2'b11, 16'hcdef, 1 );
    compare( 2'b11, 16'h0000, 1 );
    compare( 2'b11, 16'h0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_one_enabled
  //----------------------------------------------------------------------

  task test_case_2_one_enabled();
    $display( "\ntest_case_2_one_enabled" );
    t.reset_sequence();

    compare( 2'b01, 16'h0000, 0 ); // do not check output
    compare( 2'b01, 16'h0000, 1 );
    compare( 2'b01, 16'h0000, 1 ); // prev: 0 -> 0 0
    compare( 2'b01, 16'h0201, 1 ); // prev: 0 -> 1 0
    compare( 2'b01, 16'h0201, 1 ); // prev: 1 -> 1 1
    compare( 2'b01, 16'h0000, 1 ); // prev: 1 -> 0 1
    compare( 2'b01, 16'h0000, 1 );
    compare( 2'b01, 16'h0000, 1 );
    compare( 2'b01, 16'h4567, 1 );
    compare( 2'b01, 16'h89ab, 1 );
    compare( 2'b01, 16'hcdef, 1 );
    compare( 2'b01, 16'h0000, 1 );
    compare( 2'b01, 16'h0000, 1 );

    compare( 2'b10, 16'h0000, 1 );
    compare( 2'b10, 16'h0000, 1 ); // prev: 0 -> 0 0
    compare( 2'b10, 16'h0201, 1 ); // prev: 0 -> 1 0
    compare( 2'b10, 16'h0201, 1 ); // prev: 1 -> 1 1
    compare( 2'b10, 16'h0000, 1 ); // prev: 1 -> 0 1
    compare( 2'b10, 16'h0000, 1 );
    compare( 2'b10, 16'h0000, 1 );
    compare( 2'b10, 16'h4567, 1 );
    compare( 2'b10, 16'h89ab, 1 );
    compare( 2'b10, 16'hcdef, 1 );
    compare( 2'b10, 16'h0000, 1 );
    compare( 2'b10, 16'h0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_none_enabled
  //----------------------------------------------------------------------

  task test_case_3_none_enabled();
    $display( "\ntest_case_3_none_enabled" );
    t.reset_sequence();

    compare( 2'b00, 16'h0000, 0 ); // do not check output
    compare( 2'b00, 16'h0000, 1 );
    compare( 2'b00, 16'h0000, 1 ); // prev: 0 -> 0 0
    compare( 2'b00, 16'h0201, 1 ); // prev: 0 -> 1 0
    compare( 2'b00, 16'h0201, 1 ); // prev: 1 -> 1 1
    compare( 2'b00, 16'h0000, 1 ); // prev: 1 -> 0 1
    compare( 2'b00, 16'h0000, 1 );
    compare( 2'b00, 16'h0000, 1 );
    compare( 2'b00, 16'h4567, 1 );
    compare( 2'b00, 16'h89ab, 1 );
    compare( 2'b00, 16'hcdef, 1 );
    compare( 2'b00, 16'h0000, 1 );
    compare( 2'b00, 16'h0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_4_random();
    $display( "\ntest_case_4_random" );
    t.reset_sequence();

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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_both_enabled();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_one_enabled();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_none_enabled();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random();

    $write("\n");
    $finish;
  end

endmodule

