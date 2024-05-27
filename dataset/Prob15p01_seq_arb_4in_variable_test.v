//========================================================================
// Prob15p01_seq_arb_4in_variable_test
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
  logic       ref_module_set_priority_en;
  logic [3:0] ref_module_set_priority;
  logic [3:0] ref_module_reqs;
  logic [3:0] ref_module_grants;

  RefModule ref_module
  (
    .reset           (reset || ref_module_reset),
    .set_priority_en (ref_module_set_priority_en),
    .set_priority    (ref_module_set_priority),
    .reqs            (ref_module_reqs),
    .grants          (ref_module_grants),
    .*
  );

  logic       top_module_reset;
  logic       top_module_set_priority_en;
  logic [3:0] top_module_set_priority;
  logic [3:0] top_module_reqs;
  logic [3:0] top_module_grants;

  TopModule top_module
  (
    .reset           (reset || top_module_reset),
    .set_priority_en (top_module_set_priority_en),
    .set_priority    (top_module_set_priority),
    .reqs            (top_module_reqs),
    .grants          (top_module_grants),
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
    input logic       set_priority_en,
    input logic [3:0] set_priority,
    input logic [3:0] reqs
  );

    ref_module_reset           = reset;
    ref_module_set_priority_en = set_priority_en;
    ref_module_set_priority    = set_priority;
    ref_module_reqs            = reqs;

    top_module_reset           = reset;
    top_module_set_priority_en = set_priority_en;
    top_module_set_priority    = set_priority;
    top_module_reqs            = reqs;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x", t.cycles,
                top_module_reset,        top_module_set_priority_en,
                top_module_set_priority, top_module_reqs,
                top_module_grants );

    `TEST_UTILS_CHECK_EQ( top_module_grants, ref_module_grants );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_one_req
  //----------------------------------------------------------------------

  task test_case_1_one_req();
    $display( "\ntest_case_1_one_req" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 0, 4'b0000, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b0001 );
    compare( 0, 0, 4'b0000, 4'b0010 );
    compare( 0, 0, 4'b0000, 4'b0100 );
    compare( 0, 0, 4'b0000, 4'b1000 );
    compare( 0, 0, 4'b0000, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reqs
  //----------------------------------------------------------------------

  task test_case_2_all_reqs();
    $display( "\ntest_case_2_all_reqs" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 0, 4'b0000, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_set_priority
  //----------------------------------------------------------------------

  task test_case_3_set_priority();
    $display( "\ntest_case_3_set_priority" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 1, 4'b0001, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 1, 4'b0010, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 1, 4'b0100, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 1, 4'b1000, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_priority_wraparound
  //----------------------------------------------------------------------

  task test_case_4_priority_wraparound();
    $display( "\ntest_case_4_priority_wraparound" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 1, 4'b0100, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1011 );
    compare( 0, 0, 4'b0000, 4'b0011 );
    compare( 0, 0, 4'b0000, 4'b0010 );
    compare( 0, 0, 4'b0000, 4'b0000 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_example
  //----------------------------------------------------------------------

  task test_case_5_example();
    $display( "\ntest_case_5_example" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 1, 4'b0001, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b0001 );
    compare( 0, 0, 4'b0000, 4'b0011 );
    compare( 0, 0, 4'b0000, 4'b1110 );
    compare( 0, 0, 4'b0000, 4'b1000 );
    compare( 0, 1, 4'b0100, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1100 );
    compare( 0, 0, 4'b0000, 4'b0011 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_directed_reset
  //----------------------------------------------------------------------

  task test_case_6_directed_reset();
    $display( "\ntest_case_6_directed_reset" );
    t.reset_sequence();

    //       rs st pri      reqs
    compare( 0, 1, 4'b0100, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1011 );
    compare( 0, 0, 4'b0000, 4'b0011 );
    compare( 0, 0, 4'b0000, 4'b0010 );
    compare( 1, 0, 4'b0000, 4'b0000 );
    compare( 1, 0, 4'b0000, 4'b0000 );
    compare( 1, 0, 4'b0000, 4'b0000 );
    compare( 0, 0, 4'b0000, 4'b1111 );
    compare( 0, 0, 4'b0000, 4'b1011 );
    compare( 0, 0, 4'b0000, 4'b0011 );
    compare( 0, 0, 4'b0000, 4'b0010 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random1
  //----------------------------------------------------------------------

  task test_case_6_random1();
    $display( "\ntest_case_6_random1" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( 0, 0, 0, $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random2
  //----------------------------------------------------------------------

  task test_case_7_random2();
    $display( "\ntest_case_7_random2" );
    t.reset_sequence();

    for ( int i = 0; i < 40; i = i+1 ) begin

      logic [1:0] set_priority;
      logic [3:0] set_priority_one_hot;

      set_priority = $urandom(t.seed) % 4;

      case ( set_priority )
        0 : set_priority_one_hot = 4'b0001;
        1 : set_priority_one_hot = 4'b0010;
        2 : set_priority_one_hot = 4'b0100;
        3 : set_priority_one_hot = 4'b1000;
      endcase

      compare( 0, $urandom(t.seed),
               set_priority_one_hot, $urandom(t.seed) );

    end

  endtask

  //----------------------------------------------------------------------
  // test_case_8_random_reset
  //----------------------------------------------------------------------

  task test_case_8_random_reset();
    $display( "\ntest_case_8_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 40; i = i+1 ) begin

      logic [1:0] set_priority;
      logic [3:0] set_priority_one_hot;

      set_priority = $urandom(t.seed) % 4;

      case ( set_priority )
        0 : set_priority_one_hot = 4'b0001;
        1 : set_priority_one_hot = 4'b0010;
        2 : set_priority_one_hot = 4'b0100;
        3 : set_priority_one_hot = 4'b1000;
      endcase

      compare( $urandom(t.seed), $urandom(t.seed), 
               set_priority_one_hot, $urandom(t.seed) );

    end

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
    if ((t.n <= 0) || (t.n == 3)) test_case_3_set_priority();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_priority_wraparound();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_example();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_directed_reset();
    if ((t.n <= 0) || (t.n == 7)) test_case_6_random1();
    if ((t.n <= 0) || (t.n == 8)) test_case_7_random2();
    if ((t.n <= 0) || (t.n == 9)) test_case_8_random_reset();

    $write("\n");
    $finish;
  end

endmodule

