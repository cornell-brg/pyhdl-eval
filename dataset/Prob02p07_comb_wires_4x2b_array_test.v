//========================================================================
// Prob02p07_comb_wires_4x2b_array_test
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
  // If I use logic instead of wire for the output unpacked array it does
  // not seem to work with iverilog, so I use wire instead.

  logic [1:0] ref_module_in_ [4];
  wire  [1:0] ref_module_out [4];

  RefModule ref_module
  (
    .in_ (ref_module_in_),
    .out (ref_module_out)
  );

  logic [1:0] top_module_in_ [4];
  wire  [1:0] top_module_out [4];

  TopModule top_module
  (
    .in_ (top_module_in_),
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
    input logic [1:0] in0,
    input logic [1:0] in1,
    input logic [1:0] in2,
    input logic [1:0] in3
  );

    ref_module_in_[0] = in0;
    ref_module_in_[1] = in1;
    ref_module_in_[2] = in2;
    ref_module_in_[3] = in3;
    top_module_in_[0] = in0;
    top_module_in_[1] = in1;
    top_module_in_[2] = in2;
    top_module_in_[3] = in3;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x > %x %x %x %x", t.cycles,
                top_module_in_[0], top_module_in_[1],
                top_module_in_[2], top_module_in_[3],
                top_module_out[0], top_module_out[1],
                top_module_out[2], top_module_out[3] );

    `TEST_UTILS_CHECK_EQ( top_module_out[0], ref_module_out[0] );
    `TEST_UTILS_CHECK_EQ( top_module_out[1], ref_module_out[1] );
    `TEST_UTILS_CHECK_EQ( top_module_out[2], ref_module_out[2] );
    `TEST_UTILS_CHECK_EQ( top_module_out[3], ref_module_out[3] );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare( 0, 0, 0, 0 );
    compare( 0, 1, 2, 3 );
    compare( 3, 0, 1, 2 );
    compare( 2, 3, 0, 1 );
    compare( 1, 2, 3, 0 );
    compare( 0, 0, 1, 1 );
    compare( 0, 1, 1, 0 );
    compare( 1, 1, 0, 0 );

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

    for ( int i = 0; i < 20; i = i+1 )
      compare( $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed) );

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

