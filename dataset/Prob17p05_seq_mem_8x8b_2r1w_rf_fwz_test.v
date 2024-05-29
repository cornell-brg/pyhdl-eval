//========================================================================
// Prob17p05_seq_mem_8x8b_2r1w_rf_fwz_test
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

  logic [2:0] ref_module_read_addr0;
  logic [7:0] ref_module_read_data0;
  logic [2:0] ref_module_read_addr1;
  logic [7:0] ref_module_read_data1;
  logic       ref_module_write_en;
  logic [2:0] ref_module_write_addr;
  logic [7:0] ref_module_write_data;

  RefModule ref_module
  (
    .read_addr0 (ref_module_read_addr0),
    .read_data0 (ref_module_read_data0),
    .read_addr1 (ref_module_read_addr1),
    .read_data1 (ref_module_read_data1),
    .write_en   (ref_module_write_en),
    .write_addr (ref_module_write_addr),
    .write_data (ref_module_write_data),
    .*
  );

  logic [2:0] top_module_read_addr0;
  logic [7:0] top_module_read_data0;
  logic [2:0] top_module_read_addr1;
  logic [7:0] top_module_read_data1;
  logic       top_module_write_en;
  logic [2:0] top_module_write_addr;
  logic [7:0] top_module_write_data;

  TopModule top_module
  (
    .read_addr0 (top_module_read_addr0),
    .read_data0 (top_module_read_data0),
    .read_addr1 (top_module_read_addr1),
    .read_data1 (top_module_read_data1),
    .write_en   (top_module_write_en),
    .write_addr (top_module_write_addr),
    .write_data (top_module_write_data),
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
    input logic [2:0] read_addr0,
    input logic [2:0] read_addr1,
    input logic       write_en,
    input logic [2:0] write_addr,
    input logic [7:0] write_data,
    input logic       check_output
  );

    ref_module_read_addr0 = read_addr0;
    ref_module_read_addr1 = read_addr1;
    ref_module_write_en   = write_en;
    ref_module_write_addr = write_addr;
    ref_module_write_data = write_data;

    top_module_read_addr0 = read_addr0;
    top_module_read_addr1 = read_addr1;
    top_module_write_en   = write_en;
    top_module_write_addr = write_addr;
    top_module_write_data = write_data;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x %x", t.cycles,
                top_module_read_addr0, top_module_read_addr1,
                top_module_write_en, top_module_write_addr,
                top_module_write_data, top_module_read_data0, 
                top_module_read_data1 );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_read_data0, ref_module_read_data0 );
      `TEST_UTILS_CHECK_EQ( top_module_read_data1, ref_module_read_data1 );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // rf_init
  //----------------------------------------------------------------------

  task rf_init();

    //       r0 r1 we wa wd
    compare( 0, 0, 1, 1, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 2, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 3, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 4, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 5, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 6, 8'h00, 0 ); // do not check output
    compare( 0, 0, 1, 7, 8'h00, 0 ); // do not check output

  endtask

  //----------------------------------------------------------------------
  // test_case_1_simple
  //----------------------------------------------------------------------

  task test_case_1_simple();
    $display( "\ntest_case_1_simple" );
    t.reset_sequence();

    rf_init();

    //       r0 r1 we wa wd
    compare( 1, 1, 1, 1, 8'hab, 1 );
    compare( 1, 1, 0, 0, 8'h00, 1 );
    compare( 1, 1, 1, 2, 8'hcd, 1 );
    compare( 2, 2, 0, 0, 8'h00, 1 );
    compare( 1, 1, 1, 2, 8'hef, 1 );
    compare( 2, 2, 0, 0, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reg
  //----------------------------------------------------------------------

  task test_case_2_all_reg();
    $display( "\ntest_case_2_all_reg" );
    t.reset_sequence();

    rf_init();

    //       r0 r1 we wa wd
    compare( 1, 1, 1, 1, 8'h23, 1 );
    compare( 1, 1, 1, 2, 8'h45, 1 );
    compare( 1, 1, 1, 3, 8'h67, 1 );
    compare( 1, 1, 1, 4, 8'h89, 1 );
    compare( 1, 1, 1, 5, 8'hab, 1 );
    compare( 1, 1, 1, 6, 8'hcd, 1 );
    compare( 1, 1, 1, 7, 8'hef, 1 );

    compare( 1, 1, 1, 0, 8'hff, 1 );
    compare( 2, 2, 1, 0, 8'hff, 1 );
    compare( 3, 3, 1, 0, 8'hff, 1 );
    compare( 4, 4, 1, 0, 8'hff, 1 );
    compare( 5, 5, 1, 0, 8'hff, 1 );
    compare( 6, 6, 1, 0, 8'hff, 1 );
    compare( 7, 7, 1, 0, 8'hff, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_read_ports
  //----------------------------------------------------------------------

  task test_case_3_read_ports();
    $display( "\ntest_case_3_read_ports" );
    t.reset_sequence();

    rf_init();

    //       r0 r1 we wa wd
    compare( 1, 1, 1, 1, 8'h23, 1 );
    compare( 1, 1, 1, 2, 8'h45, 1 );
    compare( 1, 2, 0, 1, 8'h00, 1 );
    compare( 2, 1, 0, 1, 8'h00, 1 );
    compare( 1, 1, 1, 3, 8'h67, 1 );
    compare( 1, 3, 0, 1, 8'h00, 1 );
    compare( 3, 1, 0, 1, 8'h00, 1 );
    compare( 1, 1, 1, 4, 8'h89, 1 );
    compare( 1, 4, 0, 1, 8'h00, 1 );
    compare( 4, 1, 0, 1, 8'h00, 1 );
    compare( 1, 1, 1, 5, 8'hab, 1 );
    compare( 1, 5, 0, 1, 8'h00, 1 );
    compare( 5, 1, 0, 1, 8'h00, 1 );
    compare( 1, 1, 1, 6, 8'hcd, 1 );
    compare( 1, 6, 0, 1, 8'h00, 1 );
    compare( 6, 1, 0, 1, 8'h00, 1 );
    compare( 1, 1, 1, 7, 8'hef, 1 );
    compare( 1, 7, 0, 1, 8'h00, 1 );
    compare( 7, 1, 0, 1, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_fordward
  //----------------------------------------------------------------------

  task test_case_4_forward();
    $display( "\ntest_case_4_forward" );
    t.reset_sequence();

    rf_init();

    //       r0 r1 we wa wd
    compare( 1, 1, 1, 1, 8'h23, 1 );
    compare( 1, 1, 1, 2, 8'h45, 1 );
    compare( 1, 1, 1, 3, 8'h67, 1 );
    compare( 1, 1, 1, 4, 8'h89, 1 );
    compare( 1, 1, 1, 5, 8'hab, 1 );
    compare( 1, 1, 1, 6, 8'hcd, 1 );
    compare( 1, 1, 1, 7, 8'hef, 1 );

    compare( 1, 1, 1, 1, 8'h45, 1 );
    compare( 2, 1, 1, 2, 8'h67, 1 );
    compare( 3, 1, 1, 3, 8'h89, 1 );
    compare( 4, 1, 1, 4, 8'hab, 1 );
    compare( 5, 1, 1, 5, 8'hcd, 1 );
    compare( 6, 1, 1, 6, 8'hef, 1 );
    compare( 7, 1, 1, 7, 8'h01, 1 );

    compare( 1, 1, 1, 1, 8'h67, 1 );
    compare( 1, 2, 1, 2, 8'h89, 1 );
    compare( 1, 3, 1, 3, 8'hab, 1 );
    compare( 1, 4, 1, 4, 8'hcd, 1 );
    compare( 1, 5, 1, 5, 8'hef, 1 );
    compare( 1, 6, 1, 6, 8'h01, 1 );
    compare( 1, 7, 1, 7, 8'h23, 1 );

    compare( 1, 1, 1, 1, 8'h89, 1 );
    compare( 2, 2, 1, 2, 8'hab, 1 );
    compare( 3, 3, 1, 3, 8'hcd, 1 );
    compare( 4, 4, 1, 4, 8'hef, 1 );
    compare( 5, 5, 1, 5, 8'h01, 1 );
    compare( 6, 6, 1, 6, 8'h23, 1 );
    compare( 7, 7, 1, 7, 8'h45, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_5_zero
  //----------------------------------------------------------------------

  task test_case_5_zero();
    $display( "\ntest_case_5_zero" );
    t.reset_sequence();

    rf_init();

    //       r0 r1 we wa wd
    compare( 0, 0, 1, 0, 8'h01, 1 );
    compare( 0, 0, 0, 0, 8'h00, 1 );
    compare( 0, 0, 1, 0, 8'h23, 1 );
    compare( 0, 0, 0, 0, 8'h00, 1 );
    compare( 0, 1, 1, 0, 8'h45, 1 );
    compare( 0, 1, 0, 0, 8'h00, 1 );
    compare( 0, 1, 1, 0, 8'h67, 1 );
    compare( 0, 1, 0, 0, 8'h00, 1 );
    compare( 1, 0, 1, 0, 8'h89, 1 );
    compare( 1, 0, 0, 0, 8'h00, 1 );
    compare( 1, 0, 1, 0, 8'hab, 1 );
    compare( 1, 0, 0, 0, 8'h00, 1 );

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
    if ((t.n <= 0) || (t.n == 3)) test_case_3_read_ports();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_forward();
    if ((t.n <= 0) || (t.n == 5)) test_case_5_zero();
    if ((t.n <= 0) || (t.n == 6)) test_case_6_random();

    $write("\n");
    $finish;
  end

endmodule

