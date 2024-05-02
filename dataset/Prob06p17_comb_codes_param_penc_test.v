//========================================================================
// Prob06p17_comb_codes_param_penc_test
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
  // nbits8: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [7:0] nbits8_ref_module_in_;
  logic [2:0] nbits8_ref_module_out;

  RefModule
  #(
    .nbits (8)
  )
  nbits8_ref_module
  (
    .in_ (nbits8_ref_module_in_),
    .out (nbits8_ref_module_out)
  );

  logic [7:0] nbits8_top_module_in_;
  logic [2:0] nbits8_top_module_out;

  TopModule
  #(
    .nbits (8)
  )
  nbits8_top_module
  (
    .in_ (nbits8_top_module_in_),
    .out (nbits8_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits8: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits8_compare
  (
    input logic [7:0] in_
  );

    nbits8_ref_module_in_ = in_;
    nbits8_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits8_top_module_in_, nbits8_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits8_top_module_out, nbits8_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nbits8: test_case_1_nbits8_directed
  //----------------------------------------------------------------------

  task test_case_1_nbits8_directed();
    $display( "\ntest_case_1_nbits8_directed" );
    t.reset_sequence();

    nbits8_compare( 8'b0000_0000 );
    nbits8_compare( 8'b0000_0001 );
    nbits8_compare( 8'b0000_0010 );
    nbits8_compare( 8'b0000_0011 );

    nbits8_compare( 8'b0000_0100 );
    nbits8_compare( 8'b0000_0101 );
    nbits8_compare( 8'b0000_0110 );
    nbits8_compare( 8'b0000_0111 );

    nbits8_compare( 8'b0000_1000 );
    nbits8_compare( 8'b0000_1001 );
    nbits8_compare( 8'b0000_1010 );
    nbits8_compare( 8'b0000_1011 );

    nbits8_compare( 8'b0000_1100 );
    nbits8_compare( 8'b0000_1101 );
    nbits8_compare( 8'b0000_1110 );
    nbits8_compare( 8'b0000_1111 );

    nbits8_compare( 8'b0000_0000 );
    nbits8_compare( 8'b0001_0000 );
    nbits8_compare( 8'b0010_0000 );
    nbits8_compare( 8'b0011_0000 );

    nbits8_compare( 8'b0100_0000 );
    nbits8_compare( 8'b0101_0000 );
    nbits8_compare( 8'b0110_0000 );
    nbits8_compare( 8'b0111_0000 );

    nbits8_compare( 8'b1000_0000 );
    nbits8_compare( 8'b1001_0000 );
    nbits8_compare( 8'b1010_0000 );
    nbits8_compare( 8'b1011_0000 );

    nbits8_compare( 8'b1100_0000 );
    nbits8_compare( 8'b1101_0000 );
    nbits8_compare( 8'b1110_0000 );
    nbits8_compare( 8'b1111_0000 );

  endtask

  //----------------------------------------------------------------------
  // nbits8: test_case_2_nbits8_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_2_nbits8_random();
    $display( "\ntest_case_2_nbits8_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nbits8_compare( $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // nbits10: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [7:0] nbits10_ref_module_in_;
  logic [2:0] nbits10_ref_module_out;

  RefModule
  #(
    .nbits (8)
  )
  nbits10_ref_module
  (
    .in_ (nbits10_ref_module_in_),
    .out (nbits10_ref_module_out)
  );

  logic [7:0] nbits10_top_module_in_;
  logic [2:0] nbits10_top_module_out;

  TopModule
  #(
    .nbits (8)
  )
  nbits10_top_module
  (
    .in_ (nbits10_top_module_in_),
    .out (nbits10_top_module_out)
  );

  //----------------------------------------------------------------------
  // nbits10: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nbits10_compare
  (
    input logic [7:0] in_
  );

    nbits10_ref_module_in_ = in_;
    nbits10_top_module_in_ = in_;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x > %x", t.cycles,
                nbits10_top_module_in_, nbits10_top_module_out );

    `TEST_UTILS_CHECK_EQ( nbits10_top_module_out, nbits10_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nbits10: test_case_3_nbits10_directed
  //----------------------------------------------------------------------

  task test_case_3_nbits10_directed();
    $display( "\ntest_case_3_nbits10_directed" );
    t.reset_sequence();

    nbits10_compare( 10'b00_0000_0000 );
    nbits10_compare( 10'b00_0000_0001 );
    nbits10_compare( 10'b00_0000_0010 );
    nbits10_compare( 10'b00_0000_0011 );

    nbits10_compare( 10'b00_0000_0100 );
    nbits10_compare( 10'b00_0000_0101 );
    nbits10_compare( 10'b00_0000_0110 );
    nbits10_compare( 10'b00_0000_0111 );

    nbits10_compare( 10'b00_0000_1000 );
    nbits10_compare( 10'b00_0000_1001 );
    nbits10_compare( 10'b00_0000_1010 );
    nbits10_compare( 10'b00_0000_1011 );

    nbits10_compare( 10'b00_0000_1100 );
    nbits10_compare( 10'b00_0000_1101 );
    nbits10_compare( 10'b00_0000_1110 );
    nbits10_compare( 10'b00_0000_1111 );

    nbits10_compare( 10'b00_0000_0000 );
    nbits10_compare( 10'b00_0001_0000 );
    nbits10_compare( 10'b00_0010_0000 );
    nbits10_compare( 10'b00_0011_0000 );

    nbits10_compare( 10'b00_0100_0000 );
    nbits10_compare( 10'b00_0101_0000 );
    nbits10_compare( 10'b00_0110_0000 );
    nbits10_compare( 10'b00_0111_0000 );

    nbits10_compare( 10'b00_1000_0000 );
    nbits10_compare( 10'b00_1001_0000 );
    nbits10_compare( 10'b00_1010_0000 );
    nbits10_compare( 10'b00_1011_0000 );

    nbits10_compare( 10'b00_1100_0000 );
    nbits10_compare( 10'b00_1101_0000 );
    nbits10_compare( 10'b00_1110_0000 );
    nbits10_compare( 10'b00_1111_0000 );

    nbits10_compare( 10'b00_0000_0000 );
    nbits10_compare( 10'b01_0000_0000 );
    nbits10_compare( 10'b10_0000_0000 );
    nbits10_compare( 10'b11_0000_0000 );

  endtask

  //----------------------------------------------------------------------
  // nbits10: test_case_4_nbits10_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_4_nbits10_random();
    $display( "\ntest_case_4_nbits10_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nbits10_compare( $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nbits8_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nbits8_random();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nbits10_directed();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_nbits10_random();

    $write("\n");
    $finish;
  end

endmodule

