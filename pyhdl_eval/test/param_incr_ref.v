//========================================================================
// param_incr_ref
//========================================================================
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024

module RefModule
#(
  parameter nbits
)(
  input  logic             clk,
  input  logic             reset,
  input  logic [nbits-1:0] in_,
  output logic [nbits-1:0] out
);

  // Sequential logic

  logic [nbits-1:0] reg_out;

  always @( posedge clk ) begin
    if ( reset )
      reg_out <= 0;
    else
      reg_out <= in_;
  end

  // Combinational logic

  logic [nbits-1:0] temp_wire;

  always @(*) begin
    temp_wire = reg_out + 1;
  end

  // Structural connections

  assign out = temp_wire;

endmodule

