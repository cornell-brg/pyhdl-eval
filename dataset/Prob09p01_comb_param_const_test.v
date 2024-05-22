//========================================================================
// Prob09p01_comb_param_const_test
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
  // nbits8: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [7:0] nbits8_ref_module_out;

  RefModule
  #(
    .nbits (8),
    .value (8'hef)
  )
  nbits8_ref_module
  (
    .out (nbits8_ref_module_out)
  );

  logic [7:0] nbits8_top_module_out;

  TopModule
  #(
    .nbits (8),
    .value (8'hef)
  )
  nbits8_top_module
  (
    .out (nbits8_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits8_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits8_compare();

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x", t.cycles, nbits8_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits8_top_module_out, nbits8_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_nbits8_directed
  //----------------------------------------------------------------------

  task test_case_1_nbits8_directed();
    $display( "\ntest_case_1_nbits8_directed" );
    t.reset_sequence();

    nbits8_compare();
    nbits8_compare();

  endtask

  //----------------------------------------------------------------------
  // nbits32: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [31:0] nbits32_ref_module_out;

  RefModule
  #(
    .nbits (32),
    .value (32'hcafecafe)
  )
  nbits32_ref_module
  (
    .out (nbits32_ref_module_out)
  );

  logic [31:0] nbits32_top_module_out;

  TopModule
  #(
    .nbits (32),
    .value (32'hcafecafe)
  )
  nbits32_top_module
  (
    .out (nbits32_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits32_compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits32_compare();

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x", t.cycles, nbits32_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits32_top_module_out, nbits32_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_2_nbits32_directed
  //----------------------------------------------------------------------

  task test_case_2_nbits32_directed();
    $display( "\ntest_case_2_nbits32_directed" );
    t.reset_sequence();

    nbits32_compare();
    nbits32_compare();

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits8_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits32_directed();

    $write("\n");
    $finish;
  end

endmodule

