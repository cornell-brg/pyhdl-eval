//========================================================================
// Prob07p08_comb_arith_8b_sra_test
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

  logic [7:0] ref_module_in_;
  logic [2:0] ref_module_amt;
  logic [7:0] ref_module_out;

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .amt (ref_module_amt),
    .out (ref_module_out)
  );

  logic [7:0] top_module_in_;
  logic [2:0] top_module_amt;
  logic [7:0] top_module_out;

  TopModule top_module
  (
    .in_ (top_module_in_),
    .amt (top_module_amt),
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
    input logic [7:0] in_,
    input logic [2:0] amt
  );

    ref_module_in_ = in_;
    ref_module_amt = amt;

    top_module_in_ = in_;
    top_module_amt = amt;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x", t.cycles,
                top_module_in_, top_module_amt,
                top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_positive
  //----------------------------------------------------------------------

  task test_case_1_positive();
    $display( "\ntest_case_1_positive" );
    t.reset_sequence();

    compare( 8'b0101_1101, 0 );
    compare( 8'b0101_1101, 1 );
    compare( 8'b0101_1101, 2 );
    compare( 8'b0101_1101, 3 );
    compare( 8'b0101_1101, 4 );
    compare( 8'b0101_1101, 5 );
    compare( 8'b0101_1101, 6 );
    compare( 8'b0101_1101, 7 );

  endtask

  //----------------------------------------------------------------------
  // test_case_2_negative
  //----------------------------------------------------------------------

  task test_case_2_negative();
    $display( "\ntest_case_2_negative" );
    t.reset_sequence();

    compare( 8'b1101_0101, 0 );
    compare( 8'b1101_0101, 1 );
    compare( 8'b1101_0101, 2 );
    compare( 8'b1101_0101, 3 );
    compare( 8'b1101_0101, 4 );
    compare( 8'b1101_0101, 5 );
    compare( 8'b1101_0101, 6 );
    compare( 8'b1101_0101, 7 );

  endtask

  //----------------------------------------------------------------------
  // test_case_3_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_random();
    $display( "\ntest_case_3_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_positive();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_negative();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random();

    $write("\n");
    $finish;
  end

endmodule

