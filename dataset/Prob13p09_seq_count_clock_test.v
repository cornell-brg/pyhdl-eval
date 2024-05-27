//========================================================================
// Prob13p09_seq_count_clock_test
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
  logic       ref_module_tick;
  logic       ref_module_set_en;
  logic [3:0] ref_module_set_hours;
  logic [5:0] ref_module_set_mins;
  logic       ref_module_set_pm;
  logic [3:0] ref_module_hours;
  logic [5:0] ref_module_mins;
  logic       ref_module_pm;

  RefModule ref_module
  (
    .reset     (reset || ref_module_reset),
    .tick      (ref_module_tick),
    .set_en    (ref_module_set_en),
    .set_hours (ref_module_set_hours),
    .set_mins  (ref_module_set_mins),
    .set_pm    (ref_module_set_pm),
    .hours     (ref_module_hours),
    .mins      (ref_module_mins),
    .pm        (ref_module_pm),
    .*
  );

  logic       top_module_reset;
  logic       top_module_tick;
  logic       top_module_set_en;
  logic [3:0] top_module_set_hours;
  logic [5:0] top_module_set_mins;
  logic       top_module_set_pm;
  logic [3:0] top_module_hours;
  logic [5:0] top_module_mins;
  logic       top_module_pm;

  TopModule top_module
  (
    .reset     (reset || top_module_reset),
    .tick      (top_module_tick),
    .set_en    (top_module_set_en),
    .set_hours (top_module_set_hours),
    .set_mins  (top_module_set_mins),
    .set_pm    (top_module_set_pm),
    .hours     (top_module_hours),
    .mins      (top_module_mins),
    .pm        (top_module_pm),
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
    input logic       tick,
    input logic       set_en,
    input logic [3:0] set_hours,
    input logic [5:0] set_mins,
    input logic       set_pm
  );

    ref_module_reset     = reset;
    ref_module_tick      = tick;
    ref_module_set_en    = set_en;
    ref_module_set_hours = set_hours;
    ref_module_set_mins  = set_mins;
    ref_module_set_pm    = set_pm;

    top_module_reset     = reset;
    top_module_tick      = tick;
    top_module_set_en    = set_en;
    top_module_set_hours = set_hours;
    top_module_set_mins  = set_mins;
    top_module_set_pm    = set_pm;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x %x > %x %x %x", t.cycles,
                top_module_reset,    top_module_tick,
                top_module_set_en,   top_module_set_hours,
                top_module_set_mins, top_module_set_pm,
                top_module_hours,    top_module_mins,
                top_module_pm );

    `TEST_UTILS_CHECK_EQ( top_module_hours, ref_module_hours );
    `TEST_UTILS_CHECK_EQ( top_module_mins,  ref_module_mins  );
    `TEST_UTILS_CHECK_EQ( top_module_pm,    ref_module_pm    );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_basic
  //----------------------------------------------------------------------

  task test_case_1_basic();
    $display( "\ntest_case_1_basic" );
    t.reset_sequence();

    //       rs tk st hr mi pm
    compare( 0, 0, 1, 1, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_tick
  //----------------------------------------------------------------------

  task test_case_2_tick();
    $display( "\ntest_case_2_tick" );
    t.reset_sequence();

    //       rs tk st hr mi pm
    compare( 0, 0, 1, 1, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 0, 0, 0, 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_multi_set
  //----------------------------------------------------------------------

  task test_case_3_multi_set();
    $display( "\ntest_case_3_multi_set" );
    t.reset_sequence();

    //       rs tk st hr  mi pm
    compare( 0, 0, 1,  1,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

    compare( 0, 0, 1, 10, 30, 1 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

    compare( 0, 0, 1,  7, 45, 1 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_min_wraparound
  //----------------------------------------------------------------------

  task test_case_4_min_wraparound();
    $display( "\ntest_case_4_min_wraparound" );
    t.reset_sequence();

    //       rs tk st hr mi pm
    compare( 0, 0, 1, 1, 50, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );
    compare( 0, 1, 0, 0,  0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_hour_wraparound
  //----------------------------------------------------------------------

  task test_case_5_hour_wraparound();
    $display( "\ntest_case_5_hour_wraparound" );
    t.reset_sequence();

    //       rs tk st hr  mi pm
    compare( 0, 0, 1, 11, 55, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

    compare( 0, 0, 1, 12, 55, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

    compare( 0, 0, 1, 11, 55, 1 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

    compare( 0, 0, 1, 12, 55, 1 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );
    compare( 0, 1, 0,  0,  0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_6_directed_reset
  //----------------------------------------------------------------------

  task test_case_6_directed_reset();
    $display( "\ntest_case_6_directed_reset" );
    t.reset_sequence();

    //       rs tk st hr mi pm
    compare( 0, 0, 1, 1, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 1, 1, 0, 0, 0, 0 );
    compare( 1, 1, 0, 0, 0, 0 );
    compare( 1, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );
    compare( 0, 1, 0, 0, 0, 0 );

  endtask

  //----------------------------------------------------------------------
  // test_case_7_random
  //----------------------------------------------------------------------

  task test_case_7_random();
    $display( "\ntest_case_7_random" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 ) begin
      compare
      (
        0,                         // reset
        $urandom(t.seed),          // tick
        $urandom(t.seed),          // set_
        ($urandom(t.seed) % 12)+1, // set_hours
        $urandom(t.seed) % 60,     // set_mins
        $urandom(t.seed)           // set_pm
      );
    end


  endtask

  //----------------------------------------------------------------------
  // test_case_8_random_reset
  //----------------------------------------------------------------------

  task test_case_8_random_reset();
    $display( "\ntest_case_8_random_reset" );
    t.reset_sequence();

    for ( int i = 0; i < 50; i = i+1 ) begin
      compare
      (
        $urandom(t.seed),          // reset
        $urandom(t.seed),          // tick
        $urandom(t.seed),          // set_
        ($urandom(t.seed) % 12)+1, // set_hours
        $urandom(t.seed) % 60,     // set_mins
        $urandom(t.seed)           // set_pm
      );
    end

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_basic();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_tick();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_multi_set();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_min_wraparound();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_hour_wraparound();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_directed_reset();
    if ((t.n <= 0) || (t.n == 7)) test_case_7_random();
    if ((t.n <= 0) || (t.n == 8)) test_case_8_random_reset();

    $write("\n");
    $finish;
  end

endmodule

