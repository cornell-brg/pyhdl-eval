//========================================================================
// test_utils
//========================================================================
// A very simple verilog test framework.
//
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024
//

`ifndef TEST_UTILS_V
`define TEST_UTILS_V

module TestUtils
(
  output logic clk,
  output logic reset
);

  initial clk = 1'b1;
  always #5 clk = ~clk;

  // This variable holds the +test-case command line argument indicating
  // which test cases to run.

  string vcd_filename;
  int n = 0;
  initial begin

    if ( !$value$plusargs( "test-case=%d", n ) )
      n = 0;

    if ( $value$plusargs( "dump-vcd=%s", vcd_filename ) ) begin
      $dumpfile(vcd_filename);
      $dumpvars();
    end

  end

  // Always call $urandom with this seed variable to ensure that random
  // test cases are both isolated and reproducible.

  int seed = 32'hdeadbeef;

  // Cycle counter with timeout check

  int cycles;

  always @( posedge clk ) begin

    if ( reset )
      cycles <= 0;
    else
      cycles <= cycles + 1;

    if ( cycles > 10000 ) begin
      $display( "  ERROR (cycles=%0d): timeout!\n", cycles );
      $finish;
    end

  end

  // reset

  task reset_sequence();
    seed = 32'hdeadbeef;

    reset = 1;
    #30;
    reset = 0;
  endtask

endmodule

//------------------------------------------------------------------------
// TEST_UTILS_CHECK_EQ
//------------------------------------------------------------------------
// Compare two expressions which can be signals or constants. We use the
// XOR operator so that an X in __ref will match 0, 1, or X in __dut, but
// an X in __dut will only match an X in __ref.

`define TEST_UTILS_CHECK_EQ( __dut, __ref )                             \
  if ( __ref !== ( __ref ^ __dut ^ __ref ) )                            \
    $display( "  ERROR (cycle=%0d): %s != %s (%x != %x)",               \
              t.cycles, "__dut", "__ref", __dut, __ref );               \
  if (1)

`endif /* TEST_UTILS_V */

