//========================================================================
// Prob02p11_comb_wires_param_array_test
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
  // nports2 nports2_nbits8: Instantiate reference and top modules
  //----------------------------------------------------------------------
  // If I use logic instead of wire for the output unpacked array it does
  // not seem to work with iverilog, so I use wire instead.

  logic [7:0] nports2_nbits8_ref_module_in_ [2];
  wire  [7:0] nports2_nbits8_ref_module_out [2];

  RefModule
  #(
    .nports (2),
    .nbits  (8)
  )
  nports2_nbits8_ref_module
  (
    .in_ (nports2_nbits8_ref_module_in_),
    .out (nports2_nbits8_ref_module_out)
  );

  logic [7:0] nports2_nbits8_top_module_in_ [2];
  wire  [7:0] nports2_nbits8_top_module_out [2];

  TopModule
  #(
    .nports (2),
    .nbits  (8)
  )
  nports2_nbits8_top_module
  (
    .in_ (nports2_nbits8_top_module_in_),
    .out (nports2_nbits8_top_module_out)
  );

  //----------------------------------------------------------------------
  // nports2_nbits8: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nports2_nbits8_compare
  (
    input logic [7:0] in0,
    input logic [7:0] in1
  );

    nports2_nbits8_ref_module_in_[0] = in0;
    nports2_nbits8_ref_module_in_[1] = in1;

    nports2_nbits8_top_module_in_[0] = in0;
    nports2_nbits8_top_module_in_[1] = in1;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x", t.cycles,
                nports2_nbits8_top_module_in_[0],
                nports2_nbits8_top_module_in_[1],
                nports2_nbits8_top_module_out[0],
                nports2_nbits8_top_module_out[1] );

    `TEST_UTILS_CHECK_EQ( nports2_nbits8_top_module_out[0], nports2_nbits8_ref_module_out[0] );
    `TEST_UTILS_CHECK_EQ( nports2_nbits8_top_module_out[1], nports2_nbits8_ref_module_out[1] );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nports2_nbits8: test_case_1_nports2_nbits8_directed
  //----------------------------------------------------------------------

  task test_case_1_nports2_nbits8_directed();
    $display( "\ntest_case_1_nports2_nbits8_directed" );
    t.reset_sequence();

    nports2_nbits8_compare( 8'h00, 8'h00 );
    nports2_nbits8_compare( 8'h00, 8'h01 );
    nports2_nbits8_compare( 8'h01, 8'h00 );
    nports2_nbits8_compare( 8'h01, 8'h23 );
    nports2_nbits8_compare( 8'h45, 8'h67 );
    nports2_nbits8_compare( 8'h89, 8'hab );
    nports2_nbits8_compare( 8'hcd, 8'hef );

  endtask

  //----------------------------------------------------------------------
  // nports2_nbits8: test_case_2_nbits13_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_2_nports2_nbits8_random();
    $display( "\ntest_case_2_nports2_nbits8_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 )
      nports2_nbits8_compare( $urandom(t.seed), $urandom(t.seed) );

  endtask

  //----------------------------------------------------------------------
  // nports3_nbits13: Instantiate reference and top modules
  //----------------------------------------------------------------------
  // If I use logic instead of wire for the output unpacked array it does
  // not seem to work with iverilog, so I use wire instead.

  logic [12:0] nports3_nbits13_ref_module_in_ [3];
  wire  [12:0] nports3_nbits13_ref_module_out [3];

  RefModule
  #(
    .nports (3),
    .nbits  (13)
  )
  nports3_nbits13_ref_module
  (
    .in_ (nports3_nbits13_ref_module_in_),
    .out (nports3_nbits13_ref_module_out)
  );

  logic [12:0] nports3_nbits13_top_module_in_ [3];
  wire  [12:0] nports3_nbits13_top_module_out [3];

  TopModule
  #(
    .nports (3),
    .nbits  (13)
  )
  nports3_nbits13_top_module
  (
    .in_ (nports3_nbits13_top_module_in_),
    .out (nports3_nbits13_top_module_out)
  );

  //----------------------------------------------------------------------
  // nports3_nbits13: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nports3_nbits13_compare
  (
    input logic [12:0] in0,
    input logic [12:0] in1,
    input logic [12:0] in2
  );

    nports3_nbits13_ref_module_in_[0] = in0;
    nports3_nbits13_ref_module_in_[1] = in1;
    nports3_nbits13_ref_module_in_[2] = in2;

    nports3_nbits13_top_module_in_[0] = in0;
    nports3_nbits13_top_module_in_[1] = in1;
    nports3_nbits13_top_module_in_[2] = in2;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x %x %x", t.cycles,
                nports3_nbits13_top_module_in_[0],
                nports3_nbits13_top_module_in_[1],
                nports3_nbits13_top_module_in_[2],
                nports3_nbits13_top_module_out[0],
                nports3_nbits13_top_module_out[1],
                nports3_nbits13_top_module_out[2] );

    `TEST_UTILS_CHECK_EQ( nports3_nbits13_top_module_out[0], nports3_nbits13_ref_module_out[0] );
    `TEST_UTILS_CHECK_EQ( nports3_nbits13_top_module_out[1], nports3_nbits13_ref_module_out[1] );
    `TEST_UTILS_CHECK_EQ( nports3_nbits13_top_module_out[2], nports3_nbits13_ref_module_out[2] );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nports3_nbits13: test_case_3_nports3_nbits13_directed
  //----------------------------------------------------------------------

  task test_case_3_nports3_nbits13_directed();
    $display( "\ntest_case_3_nports3_nbits13_directed" );
    t.reset_sequence();

    nports3_nbits13_compare( 13'h0000, 13'h0000, 13'h0000 );
    nports3_nbits13_compare( 13'h0000, 13'h0000, 13'h0001 );
    nports3_nbits13_compare( 13'h0000, 13'h0001, 13'h0000 );
    nports3_nbits13_compare( 13'h0001, 13'h0000, 13'h0000 );
    nports3_nbits13_compare( 13'h0123, 13'h1567, 13'h19ab );
    nports3_nbits13_compare( 13'h1def, 13'h0123, 13'h1567 );

  endtask

  //----------------------------------------------------------------------
  // nports3_nbits13: test_case_4_nports3_nbits13_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_4_nports3_nbits13_random();
    $display( "\ntest_case_4_nports3_nbits13_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 ) begin
      nports3_nbits13_compare( $urandom(t.seed), $urandom(t.seed), 
                               $urandom(t.seed) );
    end

  endtask

  //----------------------------------------------------------------------
  // main
  //----------------------------------------------------------------------
  // We start with a #1 delay so that all tasks will essentially start at
  // #1 after the rising edge of the clock.

  initial begin
    #1;

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nports2_nbits8_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nports2_nbits8_random();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nports3_nbits13_directed();
    if ((t.n <= 0) || (t.n == 4)) test_case_4_nports3_nbits13_random();

    $write("\n");
    $finish;
  end

endmodule
