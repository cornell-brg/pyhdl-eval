//========================================================================
// Prob05p11_comb_mux_param_ninputs_test
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
  // nports2 nbits4: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [3:0] nports2_nbits4_ref_module_in_ [2];
  logic       nports2_nbits4_ref_module_sel;
  logic [3:0] nports2_nbits4_ref_module_out;

  RefModule
  #(
    .nports (2),
    .nbits  (4)
  )
  nports2_nports2_nbits4_ref_module
  (
    .in_ (nports2_nbits4_ref_module_in_),
    .sel (nports2_nbits4_ref_module_sel),
    .out (nports2_nbits4_ref_module_out)
  );

  logic [3:0] nports2_nbits4_top_module_in_ [2];
  logic       nports2_nbits4_top_module_sel;
  logic [3:0] nports2_nbits4_top_module_out;

  TopModule
  #(
    .nports (2),
    .nbits  (4)
  )
  nports2_nbits4_top_module
  (
    .in_ (nports2_nbits4_top_module_in_),
    .sel (nports2_nbits4_top_module_sel),
    .out (nports2_nbits4_top_module_out)
  );

  //----------------------------------------------------------------------
  // nports2 nbits4: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nports2_nbits4_compare
  (
    input logic [3:0] in0,
    input logic [3:0] in1,
    input logic       sel
  );

    nports2_nbits4_ref_module_in_[0] = in0;
    nports2_nbits4_ref_module_in_[1] = in1;
    nports2_nbits4_ref_module_sel    = sel;

    nports2_nbits4_top_module_in_[0] = in0;
    nports2_nbits4_top_module_in_[1] = in1;
    nports2_nbits4_top_module_sel    = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x > %x", t.cycles,
                nports2_nbits4_top_module_in_[0],
                nports2_nbits4_top_module_in_[1],
                nports2_nbits4_top_module_sel,
                nports2_nbits4_top_module_out );

    `TEST_UTILS_CHECK_EQ( nports2_nbits4_top_module_out, nports2_nbits4_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nports2 nbits4: test_case_1_nports2_nbits4_directed
  //----------------------------------------------------------------------

  task test_case_1_nports2_nbits4_directed();
    $display( "\ntest_case_1_nports2_nbits4_directed" );
    t.reset_sequence();

    nports2_nbits4_compare(0,0,0);
    nports2_nbits4_compare(0,1,1);
    nports2_nbits4_compare(0,0,0);
    nports2_nbits4_compare(0,1,1);
    nports2_nbits4_compare(1,0,0);
    nports2_nbits4_compare(1,1,1);
    nports2_nbits4_compare(1,0,0);
    nports2_nbits4_compare(1,1,1);

    nports2_nbits4_compare(0,0,0);
    nports2_nbits4_compare(0,2,1);
    nports2_nbits4_compare(0,0,0);
    nports2_nbits4_compare(0,2,1);
    nports2_nbits4_compare(2,0,0);
    nports2_nbits4_compare(2,2,1);
    nports2_nbits4_compare(2,0,0);
    nports2_nbits4_compare(2,2,1);

  endtask

  //----------------------------------------------------------------------
  // nports4 nbits13: Instantiate reference and top modules
  //----------------------------------------------------------------------

  logic [12:0] nports4_nbits13_ref_module_in_ [4];
  logic [ 1:0] nports4_nbits13_ref_module_sel;
  logic [12:0] nports4_nbits13_ref_module_out;

  RefModule
  #(
    .nports (4),
    .nbits  (13)
  )
  nports4_nbits13_ref_module
  (
    .in_ (nports4_nbits13_ref_module_in_),
    .sel (nports4_nbits13_ref_module_sel),
    .out (nports4_nbits13_ref_module_out)
  );

  logic [12:0] nports4_nbits13_top_module_in_ [4];
  logic [ 1:0] nports4_nbits13_top_module_sel;
  logic [12:0] nports4_nbits13_top_module_out;

  TopModule
  #(
    .nports (4),
    .nbits  (13)
  )
  nports4_nbits13_top_module
  (
    .in_ (nports4_nbits13_top_module_in_),
    .sel (nports4_nbits13_top_module_sel),
    .out (nports4_nbits13_top_module_out)
  );

  //----------------------------------------------------------------------
  // nports4 nbits13: compare
  //----------------------------------------------------------------------
  // All tasks start at #1 after the rising edge of the clock. So we
  // write the inputs #1 after the rising edge, and check the outputs #1
  // before the next rising edge.

  task nports4_nbits13_compare
  (
    input logic [12:0] in0,
    input logic [12:0] in1,
    input logic [12:0] in2,
    input logic [12:0] in3,
    input logic [ 1:0] sel
  );

    nports4_nbits13_ref_module_in_[0] = in0;
    nports4_nbits13_ref_module_in_[1] = in1;
    nports4_nbits13_ref_module_in_[2] = in2;
    nports4_nbits13_ref_module_in_[3] = in3;
    nports4_nbits13_ref_module_sel    = sel;

    nports4_nbits13_top_module_in_[0] = in0;
    nports4_nbits13_top_module_in_[1] = in1;
    nports4_nbits13_top_module_in_[2] = in2;
    nports4_nbits13_top_module_in_[3] = in3;
    nports4_nbits13_top_module_sel    = sel;

    #8;

    if ( t.n != 0 )
      $display( "%3d: %x %x %x %x %x > %x", t.cycles,
                nports4_nbits13_top_module_in_[0],
                nports4_nbits13_top_module_in_[1],
                nports4_nbits13_top_module_in_[2],
                nports4_nbits13_top_module_in_[3],
                nports4_nbits13_top_module_sel,
                nports4_nbits13_top_module_out );

    `TEST_UTILS_CHECK_EQ( nports4_nbits13_top_module_out, nports4_nbits13_ref_module_out );

    #2;

  endtask

  //----------------------------------------------------------------------
  // nports4_nbits13: test_case_2_nports4_nbits13_directed
  //----------------------------------------------------------------------

  task test_case_2_nports4_nbits13_directed();
    $display( "\ntest_case_2_nports4_nbits13_directed" );
    t.reset_sequence();

    nports4_nbits13_compare(0,0,0,0,0);
    nports4_nbits13_compare(1,0,0,0,0);
    nports4_nbits13_compare(0,0,0,0,1);
    nports4_nbits13_compare(0,1,0,0,1);
    nports4_nbits13_compare(0,0,0,0,2);
    nports4_nbits13_compare(0,0,1,0,2);
    nports4_nbits13_compare(0,0,0,0,3);
    nports4_nbits13_compare(0,0,0,1,3);

    nports4_nbits13_compare(0,0,0,0,0);
    nports4_nbits13_compare(2,0,0,0,0);
    nports4_nbits13_compare(0,0,0,0,1);
    nports4_nbits13_compare(0,2,0,0,1);
    nports4_nbits13_compare(0,0,0,0,2);
    nports4_nbits13_compare(0,0,2,0,2);
    nports4_nbits13_compare(0,0,0,0,3);
    nports4_nbits13_compare(0,0,0,2,3);

  endtask

  //----------------------------------------------------------------------
  // nports4 nbits13: test_case_3_nports4_nbits13_random
  //----------------------------------------------------------------------
  // svt.seed is set to a known value in the reset() task, so when use
  // $urandom(t.seed) we will get reproducible random numbers no matter
  // the order that test cases are executed.

  task test_case_3_nports4_nbits13_random();
    $display( "\ntest_case_3_nports4_nbits13_random" );
    t.reset_sequence();

    for ( int i = 0; i < 20; i = i+1 ) begin
     nports4_nbits13_compare( $urandom(t.seed), $urandom(t.seed),
                              $urandom(t.seed), $urandom(t.seed),
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

    if ((t.n <= 0) || (t.n == 1)) test_case_1_nports2_nbits4_directed();
    if ((t.n <= 0) || (t.n == 2)) test_case_2_nports4_nbits13_directed();
    if ((t.n <= 0) || (t.n == 3)) test_case_3_nports4_nbits13_random();

    $write("\n");
    $finish;
  end

endmodule
