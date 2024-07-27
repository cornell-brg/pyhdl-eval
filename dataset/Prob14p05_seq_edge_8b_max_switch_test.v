//========================================================================
// Prob14p05_seq_edge_8b_max_switch_test
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

  logic [7:0] ref_module_in_;
  logic       ref_module_max_switching;

  RefModule ref_module
  (
    .in_           (ref_module_in_),
    .max_switching (ref_module_max_switching),
    .*
  );

  logic [7:0] top_module_in_;
  logic       top_module_max_switching;

  TopModule top_module
  (
    .in_           (top_module_in_),
    .max_switching (top_module_max_switching),
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
    input logic [7:0] in_,
    input logic       check_output
  );

    ref_module_in_ = in_;
    top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_in_, top_module_max_switching );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_max_switching,
                            ref_module_max_switching );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_without_max_switching
  //----------------------------------------------------------------------

  task test_case_1_without_max_switching();
    $display( "\ntest_case_1_without_max_switching" );
    t.reset_sequence();

    compare( 8'b0000_0000, 0 ); // do not check output
    compare( 8'b0000_0000, 1 );
    compare( 8'b1111_1111, 1 );
    compare( 8'b0000_0000, 1 );
    compare( 8'b0001_0001, 1 );
    compare( 8'b0100_0100, 1 );
    compare( 8'b0010_1001, 1 );
    compare( 8'b0100_0010, 1 );
    compare( 8'b0001_0001, 1 );
    compare( 8'b0100_0010, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_with_max_switching
  //----------------------------------------------------------------------

  task test_case_2_with_max_switching();
    $display( "\ntest_case_2_with_max_switching" );
    t.reset_sequence();

    compare( 8'b0000_0000, 0 ); // do not check output
    compare( 8'b0000_0000, 1 );
    compare( 8'b0001_0001, 1 );
    compare( 8'b0101_0101, 1 );
    compare( 8'b1010_1010, 1 );
    compare( 8'b1010_1010, 1 );
    compare( 8'b0001_0001, 1 );
    compare( 8'b1010_1010, 1 );
    compare( 8'b0101_0101, 1 );
    compare( 8'b1010_1010, 1 );
    compare( 8'b0000_0000, 1 );
    compare( 8'b0000_0000, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random1
  //----------------------------------------------------------------------

  task test_case_3_random1();
    $display( "\ntest_case_3_random1" );
    t.reset_sequence();

    compare( 8'b0000_0000, 0 ); // do not check output
    for ( int i = 0; i < 20; i = i+1 ) begin
      if ( $urandom(t.seed) % 2 == 0 )
        compare( 8'b0101_0101, 1 );
      else
        compare( 8'b1010_1010, 1 );
    end

  endtask

  //----------------------------------------------------------------------
  // test_case_4_random2
  //----------------------------------------------------------------------

  task test_case_4_random2();
    $display( "\ntest_case_4_random2" );
    t.reset_sequence();

    compare( 8'b0000_0000, 0 ); // do not check output
    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), 1 );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_without_max_switching();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_with_max_switching();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random1();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_random2();

    $write("\n");
    $finish;
  end

endmodule

