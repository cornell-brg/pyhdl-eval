//========================================================================
// Prob05p02_comb_mux_1b_8to1_test
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

  logic       ref_module_in0;
  logic       ref_module_in1;
  logic       ref_module_in2;
  logic       ref_module_in3;
  logic       ref_module_in4;
  logic       ref_module_in5;
  logic       ref_module_in6;
  logic       ref_module_in7;
  logic [2:0] ref_module_sel;
  logic       ref_module_out;

  RefModule ref_module
  (
    .in0 (ref_module_in0),
    .in1 (ref_module_in1),
    .in2 (ref_module_in2),
    .in3 (ref_module_in3),
    .in4 (ref_module_in4),
    .in5 (ref_module_in5),
    .in6 (ref_module_in6),
    .in7 (ref_module_in7),
    .sel (ref_module_sel),
    .out (ref_module_out)
  );

  logic       top_module_in0;
  logic       top_module_in1;
  logic       top_module_in2;
  logic       top_module_in3;
  logic       top_module_in4;
  logic       top_module_in5;
  logic       top_module_in6;
  logic       top_module_in7;
  logic [2:0] top_module_sel;
  logic       top_module_out;

  TopModule top_module
  (
    .in0 (top_module_in0),
    .in1 (top_module_in1),
    .in2 (top_module_in2),
    .in3 (top_module_in3),
    .in4 (top_module_in4),
    .in5 (top_module_in5),
    .in6 (top_module_in6),
    .in7 (top_module_in7),
    .sel (top_module_sel),
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
    input logic       in0,
    input logic       in1,
    input logic       in2,
    input logic       in3,
    input logic       in4,
    input logic       in5,
    input logic       in6,
    input logic       in7,
    input logic [2:0] sel
  );

    ref_module_in0 = in0;
    ref_module_in1 = in1;
    ref_module_in2 = in2;
    ref_module_in3 = in3;
    ref_module_in4 = in4;
    ref_module_in5 = in5;
    ref_module_in6 = in6;
    ref_module_in7 = in7;
    ref_module_sel = sel;

    top_module_in0 = in0;
    top_module_in1 = in1;
    top_module_in2 = in2;
    top_module_in3 = in3;
    top_module_in4 = in4;
    top_module_in5 = in5;
    top_module_in6 = in6;
    top_module_in7 = in7;
    top_module_sel = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x %x %x %x %x > %x", t.cycles,
                top_module_in0, top_module_in1, top_module_in2,
                top_module_in3, top_module_in4, top_module_in5,
                top_module_in6, top_module_in7, top_module_sel,
                top_module_out );

    `TEST_UTILS_CHECK_EQ( top_module_out, ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // test_case_1_directed
  //----------------------------------------------------------------------

  task test_case_1_directed();
    $display( "\ntest_case_1_directed" );
    t.reset_sequence();

    compare(0,0,0,0,0,0,0,0,0);
    compare(1,0,0,0,0,0,0,0,0);
    compare(0,0,0,0,0,0,0,0,1);
    compare(0,1,0,0,0,0,0,0,1);
    compare(0,0,0,0,0,0,0,0,2);
    compare(0,0,1,0,0,0,0,0,2);
    compare(0,0,0,0,0,0,0,0,3);
    compare(0,0,0,1,0,0,0,0,3);

    compare(0,0,0,0,0,0,0,0,4);
    compare(0,0,0,0,1,0,0,0,4);
    compare(0,0,0,0,0,0,0,0,5);
    compare(0,0,0,0,0,1,0,0,5);
    compare(0,0,0,0,0,0,0,0,6);
    compare(0,0,0,0,0,0,1,0,6);
    compare(0,0,0,0,0,0,0,0,7);
    compare(0,0,0,0,0,0,0,1,7);

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

    for ( int i = 0; i < 20; i = i+1 ) begin
      compare( $urandom(t.seed), $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed), $urandom(t.seed),
               $urandom(t.seed), $urandom(t.seed), $urandom(t.seed) );
    end

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
