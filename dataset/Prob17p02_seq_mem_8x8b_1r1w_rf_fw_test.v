//========================================================================
// Prob17p02_seq_mem_8x8b_1r1w_rf_fw_test
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

  logic [2:0] ref_module_read_addr;
  logic [7:0] ref_module_read_data;
  logic       ref_module_write_en;
  logic [2:0] ref_module_write_addr;
  logic [7:0] ref_module_write_data;

  RefModule ref_module
  (
    .read_addr  (ref_module_read_addr),
    .read_data  (ref_module_read_data),
    .write_en   (ref_module_write_en),
    .write_addr (ref_module_write_addr),
    .write_data (ref_module_write_data),
    .*
  );

  logic [2:0] top_module_read_addr;
  logic [7:0] top_module_read_data;
  logic       top_module_write_en;
  logic [2:0] top_module_write_addr;
  logic [7:0] top_module_write_data;

  TopModule top_module
  (
    .read_addr  (top_module_read_addr),
    .read_data  (top_module_read_data),
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
    input logic [2:0] read_addr,
    input logic       write_en,
    input logic [2:0] write_addr,
    input logic [7:0] write_data,
    input logic       check_output
  );

    ref_module_read_addr  = read_addr;
    ref_module_write_en   = write_en;
    ref_module_write_addr = write_addr;
    ref_module_write_data = write_data;

    top_module_read_addr  = read_addr;
    top_module_write_en   = write_en;
    top_module_write_addr = write_addr;
    top_module_write_data = write_data;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x", t.cycles,
                top_module_read_addr, top_module_write_en,
                top_module_write_addr, top_module_write_data,
                top_module_read_data );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_read_data, ref_module_read_data );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // rf_init
  //----------------------------------------------------------------------

  task rf_init();

    //       ra we wa wd
    compare( 0, 1, 0, 8'h00, 0 ); // do not check output
    compare( 0, 1, 1, 8'h00, 0 ); // do not check output
    compare( 0, 1, 2, 8'h00, 0 ); // do not check output
    compare( 0, 1, 3, 8'h00, 0 ); // do not check output
    compare( 0, 1, 4, 8'h00, 0 ); // do not check output
    compare( 0, 1, 5, 8'h00, 0 ); // do not check output
    compare( 0, 1, 6, 8'h00, 0 ); // do not check output
    compare( 0, 1, 7, 8'h00, 0 ); // do not check output

  endtask

  //----------------------------------------------------------------------
  // test_case_1_simple
  //----------------------------------------------------------------------

  task test_case_1_simple();
    $display( "\ntest_case_1_simple" );
    t.reset_sequence();

    rf_init();

    //       ra we wa wd
    compare( 0, 0, 0, 8'h00, 1 );
    compare( 0, 1, 0, 8'hab, 1 );
    compare( 0, 0, 0, 8'h00, 1 );
    compare( 0, 1, 1, 8'hcd, 1 );
    compare( 1, 0, 0, 8'h00, 1 );
    compare( 0, 1, 1, 8'hef, 1 );
    compare( 1, 0, 0, 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_all_reg
  //----------------------------------------------------------------------

  task test_case_2_all_reg();
    $display( "\ntest_case_2_all_reg" );
    t.reset_sequence();

    rf_init();

    //       ra we wa wd
    compare( 0, 1, 0, 8'h01, 1 );
    compare( 0, 1, 1, 8'h23, 1 );
    compare( 0, 1, 2, 8'h45, 1 );
    compare( 0, 1, 3, 8'h67, 1 );
    compare( 0, 1, 4, 8'h89, 1 );
    compare( 0, 1, 5, 8'hab, 1 );
    compare( 0, 1, 6, 8'hcd, 1 );
    compare( 0, 1, 7, 8'hef, 1 );

    compare( 0, 1, 0, 8'hff, 1 );
    compare( 1, 1, 0, 8'hff, 1 );
    compare( 2, 1, 0, 8'hff, 1 );
    compare( 3, 1, 0, 8'hff, 1 );
    compare( 4, 1, 0, 8'hff, 1 );
    compare( 5, 1, 0, 8'hff, 1 );
    compare( 6, 1, 0, 8'hff, 1 );
    compare( 7, 1, 0, 8'hff, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_fordward
  //----------------------------------------------------------------------

  task test_case_3_forward();
    $display( "\ntest_case_3_forward" );
    t.reset_sequence();

    rf_init();

    compare( 0, 1, 0, 8'h01, 1 );
    compare( 0, 1, 1, 8'h23, 1 );
    compare( 0, 1, 2, 8'h45, 1 );
    compare( 0, 1, 3, 8'h67, 1 );
    compare( 0, 1, 4, 8'h89, 1 );
    compare( 0, 1, 5, 8'hab, 1 );
    compare( 0, 1, 6, 8'hcd, 1 );
    compare( 0, 1, 7, 8'hef, 1 );

    compare( 0, 1, 0, 8'h23, 1 );
    compare( 1, 1, 1, 8'h45, 1 );
    compare( 2, 1, 2, 8'h67, 1 );
    compare( 3, 1, 3, 8'h89, 1 );
    compare( 4, 1, 4, 8'hab, 1 );
    compare( 5, 1, 5, 8'hcd, 1 );
    compare( 6, 1, 6, 8'hef, 1 );
    compare( 7, 1, 7, 8'h01, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random
  //----------------------------------------------------------------------

  task test_case_4_random();
    $display( "\ntest_case_4_random" );
    t.reset_sequence();

    rf_init();

    for ( int i = 0; i < 40; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed),
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
    if ((t.n <= 0) || (t.n == 3)) test_case_3_forward();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random();

    $write("\n");
    $finish;
  end

endmodule

