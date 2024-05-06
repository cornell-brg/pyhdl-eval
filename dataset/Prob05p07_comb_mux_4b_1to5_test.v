//========================================================================
// Prob05p07_comb_mux_4b_1to5_test
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

  logic [3:0] ref_module_in_;
  logic [2:0] ref_module_sel;
  logic [3:0] ref_module_out0;
  logic [3:0] ref_module_out1;
  logic [3:0] ref_module_out2;
  logic [3:0] ref_module_out3;
  logic [3:0] ref_module_out4;

  RefModule ref_module
  (
    .in_  (ref_module_in_),
    .sel  (ref_module_sel),
    .out0 (ref_module_out0),
    .out1 (ref_module_out1),
    .out2 (ref_module_out2),
    .out3 (ref_module_out3),
    .out4 (ref_module_out4)
  );

  logic [3:0] top_module_in_;
  logic [2:0] top_module_sel;
  logic [3:0] top_module_out0;
  logic [3:0] top_module_out1;
  logic [3:0] top_module_out2;
  logic [3:0] top_module_out3;
  logic [3:0] top_module_out4;

  TopModule top_module
  (
    .in_  (top_module_in_),
    .sel  (top_module_sel),
    .out0 (top_module_out0),
    .out1 (top_module_out1),
    .out2 (top_module_out2),
    .out3 (top_module_out3),
    .out4 (top_module_out4)
  );

  //----------------------------------------------------------------------
  // compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task compare
  (
    input logic [3:0] in_,
    input logic [2:0] sel
  );

    ref_module_in_ = in_;
    ref_module_sel = sel;

    top_module_in_ = in_;
    top_module_sel = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x > %x %x %x %x %x", t.cycles,
                top_module_in_,  top_module_sel, top_module_out0,
                top_module_out1, top_module_out2, top_module_out3,
                top_module_out4 );

    `TEST_UTILS_CHECK_EQ( top_module_out0, ref_module_out0 );
    `TEST_UTILS_CHECK_EQ( top_module_out1, ref_module_out1 );
    `TEST_UTILS_CHECK_EQ( top_module_out2, ref_module_out2 );
    `TEST_UTILS_CHECK_EQ( top_module_out3, ref_module_out3 );
    `TEST_UTILS_CHECK_EQ( top_module_out4, ref_module_out4 );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_valid
  //----------------------------------------------------------------------

  task test_case_1_valid();
    $display( "\ntest_case_1_valid" );
    t.reset_sequence();

    compare(0,0);
    compare(1,0);
    compare(0,1);
    compare(1,1);
    compare(0,2);
    compare(1,2);
    compare(0,3);
    compare(1,3);
    compare(0,4);
    compare(1,4);

  endtask

  //----------------------------------------------------------------------
  // test_case_2_invalid
  //----------------------------------------------------------------------

  task test_case_2_invalid();
    $display( "\ntest_case_2_invalid" );
    t.reset_sequence();

    compare(0,5);
    compare(1,5);
    compare(0,6);
    compare(1,6);
    compare(0,7);
    compare(1,7);

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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_valid();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_invalid();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_random();

    $write("\n");
    $finish;
  end

endmodule
