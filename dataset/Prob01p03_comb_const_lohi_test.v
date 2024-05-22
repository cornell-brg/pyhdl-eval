//========================================================================
// Prob01p03_comb_const_lohi_test
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

  logic ref_module_lo;
  logic ref_module_hi;

  RefModule ref_module
  (
    .lo (ref_module_lo),
    .hi (ref_module_hi)
  );

  logic top_module_lo;
  logic top_module_hi;

  TopModule top_module
  (
    .lo (top_module_lo),
    .hi (top_module_hi)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare();

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x", t.cycles, top_module_lo, top_module_hi );

    `TEST_UTILS_CHECK_EQ( top_module_lo, ref_module_lo );
    `TEST_UTILS_CHECK_EQ( top_module_hi, ref_module_hi );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare();
    compare();

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

