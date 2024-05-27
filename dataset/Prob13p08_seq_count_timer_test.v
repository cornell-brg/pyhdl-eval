//========================================================================
// Prob13p08_seq_count_timer_test
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
  logic       ref_module_restart;
  logic       ref_module_tick;
  logic       ref_module_run;
  logic [5:0] ref_module_mins;
  logic [5:0] ref_module_secs;

  RefModule ref_module
  (
    .reset   (reset || ref_module_reset),
    .restart (ref_module_restart),
    .tick    (ref_module_tick),
    .run     (ref_module_run),
    .mins    (ref_module_mins),
    .secs    (ref_module_secs),
    .*
  );

  logic       top_module_reset;
  logic       top_module_restart;
  logic       top_module_tick;
  logic       top_module_run;
  logic [5:0] top_module_mins;
  logic [5:0] top_module_secs;

  TopModule top_module
  (
    .reset   (reset || top_module_reset),
    .restart (top_module_restart),
    .tick    (top_module_tick),
    .run     (top_module_run),
    .mins    (top_module_mins),
    .secs    (top_module_secs),
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
    input logic reset,
    input logic restart,
    input logic tick,
    input logic run
  );

    ref_module_reset   = reset;
    ref_module_restart = restart;
    ref_module_tick    = tick;
    ref_module_run     = run;

    top_module_reset   = reset;
    top_module_restart = restart;
    top_module_tick    = tick;
    top_module_run     = run;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x %x", t.cycles,
                top_module_reset, top_module_restart,
                top_module_tick,  top_module_run,
                top_module_mins,  top_module_secs );

    `TEST_UTILS_CHECK_EQ( top_module_mins, ref_module_mins );
    `TEST_UTILS_CHECK_EQ( top_module_secs, ref_module_secs );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_basic
  //----------------------------------------------------------------------

  task test_case_1_basic();
    $display( "\ntest_case_1_basic" );
    t.reset_sequence();

    //       rs st tk rn
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_tick
  //----------------------------------------------------------------------

  task test_case_2_tick();
    $display( "\ntest_case_2_tick" );
    t.reset_sequence();

    //       rs st tk rn
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 0, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_run
  //----------------------------------------------------------------------

  task test_case_3_run();
    $display( "\ntest_case_3_run" );
    t.reset_sequence();

    //       rs st tk rn
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_sec_wraparound
  //----------------------------------------------------------------------

  task test_case_4_sec_wraparound();
    $display( "\ntest_case_4_sec_wraparound" );
    t.reset_sequence();

    for ( int i = 0; i < 150; i++ )
      compare( 0, 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_saturate
  //----------------------------------------------------------------------

  task test_case_5_saturate();
    $display( "\ntest_case_5_saturate" );
    t.reset_sequence();

    for ( int i = 0; i < (60*60+10); i++ )
      compare( 0, 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_directed_restart
  //----------------------------------------------------------------------

  task test_case_6_directed_restart();
    $display( "\ntest_case_6_directed_restart" );
    t.reset_sequence();

    //       rs st tk rn
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 1, 1, 1 );
    compare( 0, 1, 1, 1 );
    compare( 0, 1, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_directed_reset
  //----------------------------------------------------------------------

  task test_case_7_directed_reset();
    $display( "\ntest_case_7_directed_reset" );
    t.reset_sequence();

    //       rs st tk rn
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 1, 0, 1, 1 );
    compare( 1, 0, 1, 1 );
    compare( 1, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );
    compare( 0, 0, 1, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_8_random
  //----------------------------------------------------------------------

  task test_case_8_random();
    $display( "\ntest_case_8_random" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( 0, 0, $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_9_random_restart
  //----------------------------------------------------------------------

  task test_case_9_random_restart();
    $display( "\ntest_case_9_random_restart" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( 0, $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // test_case_10_random_reset
  //----------------------------------------------------------------------

  task test_case_10_random_reset();
    $display( "\ntest_case_10_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n ==  1)) test_case_1_basic();
    if ((t.n <= 0) || (t.n ==  2)) test_case_2_tick();
    if ((t.n <= 0) || (t.n ==  3)) test_case_3_run();
    if ((t.n <= 0) || (t.n ==  4)) test_case_4_sec_wraparound();
    if ((t.n <= 0) || (t.n ==  5)) test_case_5_saturate();
    if ((t.n <= 0) || (t.n ==  6)) test_case_6_directed_restart();
    if ((t.n <= 0) || (t.n ==  7)) test_case_7_directed_reset();
    if ((t.n <= 0) || (t.n ==  8)) test_case_8_random();
    if ((t.n <= 0) || (t.n ==  9)) test_case_9_random_restart();
    if ((t.n <= 0) || (t.n == 10)) test_case_10_random_reset();

    $write("\n");
    $finish;
  end

endmodule

