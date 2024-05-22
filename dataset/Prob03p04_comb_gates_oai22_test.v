//========================================================================
// Prob03p04_comb_gates_oai22_test
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

  logic ref_module_in0;
  logic ref_module_in1;
  logic ref_module_in2;
  logic ref_module_in3;
  logic ref_module_out;

  RefModule ref_module
  (
    .in0 (ref_module_in0),
    .in1 (ref_module_in1),
    .in2 (ref_module_in2),
    .in3 (ref_module_in3),
    .out (ref_module_out)
  );

  logic top_module_in0;
  logic top_module_in1;
  logic top_module_in2;
  logic top_module_in3;
  logic top_module_out;

  TopModule top_module
  (
    .in0 (top_module_in0),
    .in1 (top_module_in1),
    .in2 (top_module_in2),
    .in3 (top_module_in3),
    .out (top_module_out)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic in0,
    input logic in1,
    input logic in2,
    input logic in3
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_in2 = in2;
    ref_module_in3 = in3;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_in2 = in2;
    top_module_in3 = in3;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x", t.cycles,
                top_module_in0, top_module_in1,
                top_module_in2, top_module_in3,
                top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0,0,0);
    compare(0,0,0,1);
    compare(0,0,1,0);
    compare(0,0,1,1);
    compare(0,1,0,0);
    compare(0,1,0,1);
    compare(0,1,1,0);
    compare(0,1,1,1);

    compare(1,0,0,0);
    compare(1,0,0,1);
    compare(1,0,1,0);
    compare(1,0,1,1);
    compare(1,1,0,0);
    compare(1,1,0,1);
    compare(1,1,1,0);
    compare(1,1,1,1);

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();

    $write("\n");
    $finish;
  end

endmodule

