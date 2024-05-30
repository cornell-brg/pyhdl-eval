//========================================================================
// Prob17p06_seq_mem_8x8b_1s1w_cam_test
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

  logic       ref_module_write_en;
  logic [2:0] ref_module_write_addr;
  logic [7:0] ref_module_write_data;
  logic       ref_module_search_en;
  logic [7:0] ref_module_search_data;
  logic [7:0] ref_module_search_match;

  RefModule ref_module
  (
    .write_en     (ref_module_write_en),
    .write_addr   (ref_module_write_addr),
    .write_data   (ref_module_write_data),
    .search_en    (ref_module_search_en),
    .search_data  (ref_module_search_data),
    .search_match (ref_module_search_match),
    .*
  );

  logic       top_module_write_en;
  logic [2:0] top_module_write_addr;
  logic [7:0] top_module_write_data;
  logic       top_module_search_en;
  logic [7:0] top_module_search_data;
  logic [7:0] top_module_search_match;

  TopModule top_module
  (
    .write_en     (top_module_write_en),
    .write_addr   (top_module_write_addr),
    .write_data   (top_module_write_data),
    .search_en    (top_module_search_en),
    .search_data  (top_module_search_data),
    .search_match (top_module_search_match),
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
    input logic       write_en,
    input logic [2:0] write_addr,
    input logic [7:0] write_data,
    input logic       search_en,
    input logic [7:0] search_data,
    input logic       check_output
  );

    ref_module_write_en    = write_en;
    ref_module_write_addr  = write_addr;
    ref_module_write_data  = write_data;
    ref_module_search_en   = search_en;
    ref_module_search_data = search_data;

    top_module_write_en    = write_en;
    top_module_write_addr  = write_addr;
    top_module_write_data  = write_data;
    top_module_search_en   = search_en;
    top_module_search_data = search_data;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x", t.cycles,
                top_module_write_en, top_module_write_addr,
                top_module_write_data, top_module_search_en,
                top_module_search_data, top_module_search_match );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_search_match, ref_module_search_match );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // rf_init
  //----------------------------------------------------------------------

  task rf_init();

    //       we wa wd     se sd
    compare( 1, 0, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 1, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 2, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 3, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 4, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 5, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 6, 8'h00, 0, 8'h0, 0 ); // do not check output
    compare( 1, 7, 8'h00, 0, 8'h0, 0 ); // do not check output

  endtask

  //----------------------------------------------------------------------
  // test_case_1_simple
  //----------------------------------------------------------------------

  task test_case_1_simple();
    $display( "\ntest_case_1_simple" );
    t.reset_sequence();

    rf_init();

    //       we wa wd     se sd
    compare( 0, 0, 8'h00, 0, 8'h00, 1 );
    compare( 1, 0, 8'hab, 0, 8'h00, 1 );
    compare( 0, 0, 8'h00, 1, 8'hab, 1 );
    compare( 1, 1, 8'hcd, 0, 8'h00, 1 );
    compare( 0, 0, 8'h00, 1, 8'hcd, 1 );
    compare( 1, 1, 8'hef, 0, 8'h00, 1 );
    compare( 0, 0, 8'h00, 1, 8'hef, 1 );
    compare( 0, 0, 8'h00, 0, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reg
  //----------------------------------------------------------------------

  task test_case_2_all_reg();
    $display( "\ntest_case_2_all_reg" );
    t.reset_sequence();

    rf_init();

    //       we wa wd     se sd
    compare( 1, 0, 8'h01, 0, 8'h00, 1 );
    compare( 1, 1, 8'h23, 0, 8'h00, 1 );
    compare( 1, 2, 8'h45, 0, 8'h00, 1 );
    compare( 1, 3, 8'h67, 0, 8'h00, 1 );
    compare( 1, 4, 8'h89, 0, 8'h00, 1 );
    compare( 1, 5, 8'hab, 0, 8'h00, 1 );
    compare( 1, 6, 8'hcd, 0, 8'h00, 1 );
    compare( 1, 7, 8'hef, 0, 8'h00, 1 );

    compare( 0, 0, 8'h00, 1, 8'h01, 1 );
    compare( 0, 0, 8'h00, 1, 8'h23, 1 );
    compare( 0, 0, 8'h00, 1, 8'h45, 1 );
    compare( 0, 0, 8'h00, 1, 8'h67, 1 );
    compare( 0, 0, 8'h00, 1, 8'h89, 1 );
    compare( 0, 0, 8'h00, 1, 8'hab, 1 );
    compare( 0, 0, 8'h00, 1, 8'hcd, 1 );
    compare( 0, 0, 8'h00, 1, 8'hef, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_multi_match
  //----------------------------------------------------------------------

  task test_case_3_multi_match();
    $display( "\ntest_case_3_multi_match" );
    t.reset_sequence();

    rf_init();

    //       we wa wd     se sd
    compare( 1, 0, 8'h01, 0, 8'h00, 1 );
    compare( 1, 1, 8'h23, 0, 8'h00, 1 );
    compare( 1, 2, 8'hab, 0, 8'h00, 1 );
    compare( 1, 3, 8'h23, 0, 8'h00, 1 );
    compare( 1, 4, 8'h89, 0, 8'h00, 1 );
    compare( 1, 5, 8'hab, 0, 8'h00, 1 );
    compare( 1, 6, 8'h23, 0, 8'h00, 1 );
    compare( 1, 7, 8'hef, 0, 8'h00, 1 );

    compare( 0, 0, 8'h00, 1, 8'h01, 1 );
    compare( 0, 0, 8'h00, 1, 8'h23, 1 );
    compare( 0, 0, 8'h00, 1, 8'h89, 1 );
    compare( 0, 0, 8'h00, 1, 8'hab, 1 );
    compare( 0, 0, 8'h00, 1, 8'hef, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_no_forward
  //----------------------------------------------------------------------

  task test_case_4_no_forward();
    $display( "\ntest_case_4_no_forward" );
    t.reset_sequence();

    rf_init();

    //       we wa wd     se sd
    compare( 1, 0, 8'h01, 1, 8'h01, 1 );
    compare( 1, 1, 8'h23, 1, 8'h23, 1 );
    compare( 1, 2, 8'h45, 1, 8'h45, 1 );
    compare( 1, 3, 8'h67, 1, 8'h67, 1 );
    compare( 1, 4, 8'h89, 1, 8'h89, 1 );
    compare( 1, 5, 8'hab, 1, 8'hab, 1 );
    compare( 1, 6, 8'hcd, 1, 8'hcd, 1 );
    compare( 1, 7, 8'hef, 1, 8'hef, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_random_constrained
  //----------------------------------------------------------------------

  task test_case_5_random_constrained();
    $display( "\ntest_case_5_random_constrained" );
    t.reset_sequence();

    rf_init();

    for ( int i = 0; i < 40; i = i+1 ) begin
      compare
      (
        $urandom(t.seed),         // write_en
        $urandom(t.seed),         // write_addr
        ($urandom(t.seed) % 4)+1, // write_data
        $urandom(t.seed),         // search_en
        ($urandom(t.seed) % 4)+1, // search_data
        1
      );
    end

  endtask

  //----------------------------------------------------------------------
  // test_case_6_random
  //----------------------------------------------------------------------

  task test_case_6_random();
    $display( "\ntest_case_6_random" );
    t.reset_sequence();

    rf_init();

    for ( int i = 0; i < 40; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_simple();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_all_reg();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_multi_match();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_no_forward();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_random_constrained();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();

    $write("\n");
    $finish;
  end

endmodule

