//========================================================================
// Prob09p04_comb_param_2to1_mux_test
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
  // nbits4: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [3:0] nbits4_ref_module_in0;
  logic [3:0] nbits4_ref_module_in1;
  logic       nbits4_ref_module_sel;
  logic [3:0] nbits4_ref_module_out;

  RefModule
  #(
    .nbits (4)
  )
  nbits4_ref_module
  (
    .in0 (nbits4_ref_module_in0),
    .in1 (nbits4_ref_module_in1),
    .sel (nbits4_ref_module_sel),
    .out (nbits4_ref_module_out)
  );

  logic [3:0] nbits4_top_module_in0;
  logic [3:0] nbits4_top_module_in1;
  logic       nbits4_top_module_sel;
  logic [3:0] nbits4_top_module_out;

  TopModule
  #(
    .nbits (4)
  )
  nbits4_top_module
  (
    .in0 (nbits4_top_module_in0),
    .in1 (nbits4_top_module_in1),
    .sel (nbits4_top_module_sel),
    .out (nbits4_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits4_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits4_compare
  (
    input logic [3:0] in0,
    input logic [3:0] in1,
    input logic       sel
  );

    nbits4_ref_module_in0 = in0;
    nbits4_ref_module_in1 = in1;
    nbits4_ref_module_sel = sel;

    nbits4_top_module_in0 = in0;
    nbits4_top_module_in1 = in1;
    nbits4_top_module_sel = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                nbits4_top_module_in0, nbits4_top_module_in1,
                nbits4_top_module_sel, nbits4_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits4_top_module_out, nbits4_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_nbits4_directed
  //----------------------------------------------------------------------

  task test_case_1_nbits4_directed();
    $display( "\ntest_case_1_nbits4_directed" );
    t.reset_sequence();

    nbits4_compare(0,0,0);
    nbits4_compare(0,1,1);
    nbits4_compare(0,0,0);
    nbits4_compare(0,1,1);
    nbits4_compare(1,0,0);
    nbits4_compare(1,1,1);
    nbits4_compare(1,0,0);
    nbits4_compare(1,1,1);

    nbits4_compare(0,0,0);
    nbits4_compare(0,2,1);
    nbits4_compare(0,0,0);
    nbits4_compare(0,2,1);
    nbits4_compare(2,0,0);
    nbits4_compare(2,2,1);
    nbits4_compare(2,0,0);
    nbits4_compare(2,2,1);

  endtask

  //----------------------------------------------------------------------
  // nbits13: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [12:0] nbits13_ref_module_in0;
  logic [12:0] nbits13_ref_module_in1;
  logic        nbits13_ref_module_sel;
  logic [12:0] nbits13_ref_module_out;

  RefModule
  #(
    .nbits (13)
  )
  nbits13_ref_module
  (
    .in0 (nbits13_ref_module_in0),
    .in1 (nbits13_ref_module_in1),
    .sel (nbits13_ref_module_sel),
    .out (nbits13_ref_module_out)
  );

  logic [12:0] nbits13_top_module_in0;
  logic [12:0] nbits13_top_module_in1;
  logic        nbits13_top_module_sel;
  logic [12:0] nbits13_top_module_out;

  TopModule
  #(
    .nbits (13)
  )
  nbits13_top_module
  (
    .in0 (nbits13_top_module_in0),
    .in1 (nbits13_top_module_in1),
    .sel (nbits13_top_module_sel),
    .out (nbits13_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits13_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits13_compare
  (
    input logic [12:0] in0,
    input logic [12:0] in1,
    input logic        sel
  );

    nbits13_ref_module_in0 = in0;
    nbits13_ref_module_in1 = in1;
    nbits13_ref_module_sel = sel;

    nbits13_top_module_in0 = in0;
    nbits13_top_module_in1 = in1;
    nbits13_top_module_sel = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                nbits13_top_module_in0, nbits13_top_module_in1,
                nbits13_top_module_sel, nbits13_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits13_top_module_out, nbits13_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_2_nbits13_directed
  //----------------------------------------------------------------------

  task test_case_2_nbits13_directed();
    $display( "\ntest_case_2_nbits13_directed" );
    t.reset_sequence();

    nbits13_compare(0,0,0);
    nbits13_compare(0,1,1);
    nbits13_compare(0,0,0);
    nbits13_compare(0,1,1);
    nbits13_compare(1,0,0);
    nbits13_compare(1,1,1);
    nbits13_compare(1,0,0);
    nbits13_compare(1,1,1);

    nbits13_compare(0,0,0);
    nbits13_compare(0,2,1);
    nbits13_compare(0,0,0);
    nbits13_compare(0,2,1);
    nbits13_compare(2,0,0);
    nbits13_compare(2,2,1);
    nbits13_compare(2,0,0);
    nbits13_compare(2,2,1);

  endtask

  //----------------------------------------------------------------------
  // test_case_3_nbits13_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_nbits13_random();
    $display( "\ntest_case_3_nbits13_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 ) begin
     nbits13_compare( $urandom(t.seed), $urandom(t.seed), 
                      $urandom(t.seed) );
   end

  endtask


  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits4_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits13_directed();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nbits13_random();

    $write("\n");
    $finish;
  end

endmodule

