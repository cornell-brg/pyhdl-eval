//========================================================================
// comb_incr_verilog
//========================================================================
// SPDX-License-Identifier: MIT
// Author : Christopher Batten, NVIDIA
// Date   : May 20, 2024

module TopModule
(
  input  logic [7:0] in_,
  output logic [7:0] out
);

  assign out = in_ + 1;

endmodule

