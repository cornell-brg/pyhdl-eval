//========================================================================
// pipe_incr_verilog
//========================================================================
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024

module TopModule
(
  input  logic       clk,
  input  logic [7:0] in0,
  input  logic [7:0] in1,
  output logic [7:0] out
);

  // Stage 0

  logic [7:0] in0_X0;
  logic [7:0] in1_X0;

  always @( posedge clk ) begin
    in0_X0 <= in0;
    in1_X0 <= in1;
  end

  logic [7:0] incr0_X0;
  logic [7:0] incr1_X0;

  assign incr0_X0 = in0_X0 + 1;
  assign incr1_X0 = in1_X0 + 1;

  // Stage 1

  logic [7:0] incr0_X1;
  logic [7:0] incr1_X1;

  always @( posedge clk ) begin
    incr0_X1 <= incr0_X0;
    incr1_X1 <= incr1_X0;
  end

  assign out = incr0_X1 + incr1_X1;

endmodule

