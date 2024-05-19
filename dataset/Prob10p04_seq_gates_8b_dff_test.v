//========================================================================
// Prob10p04_seq_gates_8b_dff_test
//========================================================================

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

  logic [7:0] ref_module_d;
  logic [7:0] ref_module_q;

  RefModule ref_module
  (
    .d (ref_module_d),
    .q (ref_module_q),
    .*
  );

  logic [7:0] top_module_d;
  logic [7:0] top_module_q;

  TopModule top_module
  (
    .d (top_module_d),
    .q (top_module_q),
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
    input logic [7:0] d,
    input logic       check_output
  );

    ref_module_d = d;
    top_module_d = d;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                top_module_d, top_module_q );

    if ( check_output ) begin
      `TEST_UTILS_CHECK_EQ( top_module_q, ref_module_q );
    end

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 8'h00, 0 ); // do not check output
    compare( 8'h00, 1 );
    compare( 8'h00, 1 ); // prev: 0 -> 0 0
    compare( 8'h01, 1 ); // prev: 0 -> 1 0
    compare( 8'h01, 1 ); // prev: 1 -> 1 1
    compare( 8'h00, 1 ); // prev: 1 -> 0 1
    compare( 8'h00, 1 );
    compare( 8'hab, 1 );
    compare( 8'hcd, 1 );
    compare( 8'hef, 1 );
    compare( 8'h00, 1 );
    compare( 8'h00, 1 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_2_random();
    $display( "\ntest_case_2_random" );
    t.reset_sequence();

    compare( 8'h00, 0 ); // do not check output
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_random();

    $write("\n");
    $finish;
  end

endmodule

