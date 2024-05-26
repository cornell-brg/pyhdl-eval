//========================================================================
// count_incr_verilog
//========================================================================
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024

module TopModule
(
  input  logic       clk,
  input  logic       en,
  input  logic       ld,
  input  logic [7:0] in_,
  output logic [7:0] out
);

  // Sequential logic

  logic [7:0] reg_next;
  logic [7:0] reg_out;

  always @( posedge clk ) begin
    if ( ld )
      reg_out <= in_;
    else if ( en )
      reg_out <= reg_next;
  end

  // Combinational logic

  always @(*) begin
    reg_next = reg_out + 1;
  end

  // Structural connections

  assign out = reg_out;

endmodule

