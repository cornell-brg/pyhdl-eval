//========================================================================
// Prob04p08_comb_bool_kmap1_test
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

  logic ref_module_a;
  logic ref_module_b;
  logic ref_module_c;
  logic ref_module_f;

  RefModule ref_module
  (
    .a (ref_module_a),
    .b (ref_module_b),
    .c (ref_module_c),
    .f (ref_module_f)
  );

  logic top_module_a;
  logic top_module_b;
  logic top_module_c;
  logic top_module_f;

  TopModule top_module
  (
    .a (top_module_a),
    .b (top_module_b),
    .c (top_module_c),
    .f (top_module_f)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic a,
    input logic b,
    input logic c
  );

    ref_module_a = a;
    ref_module_b = b;
    ref_module_c = c;

    top_module_a = a;
    top_module_b = b;
    top_module_c = c;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                top_module_a, top_module_b, top_module_c,
                top_module_f );

    `TEST_UTILS_CHECK_EQ( top_module_f, ref_module_f );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0,0);
    compare(0,0,1);
    compare(0,1,0);
    compare(0,1,1);
    compare(1,0,0);
    compare(1,0,1);
    compare(1,1,0);
    compare(1,1,1);

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

