//========================================================================
// Prob11p05_seq_bool_waveform1_test
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
  logic ref_module_f;

  RefModule ref_module
  (
    .a (ref_module_a),
    .f (ref_module_f),
    .*
  );

  logic top_module_a;
  logic top_module_f;

  TopModule top_module
  (
    .a (top_module_a),
    .f (top_module_f),
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
    input logic a,
    input logic check_output
  );

    ref_module_a = a;
    top_module_a = a;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_a, top_module_f );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_f, ref_module_f );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 0, 0 ); // do not check output
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_example
  //----------------------------------------------------------------------

  task test_case_2_example();
    $display( "\ntest_case_2_example" );
    t.reset_sequence();

    compare( 0, 0 ); // do not check output
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 1, 1 );
    compare( 0, 1 );
    compare( 1, 1 );
    compare( 0, 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_example();

    $write("\n");
    $finish;
  end

endmodule

