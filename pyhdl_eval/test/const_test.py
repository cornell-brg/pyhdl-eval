#=========================================================================
# const_test
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

import pytest

from pyhdl_eval.cfg  import Config, OutputPort
from pyhdl_eval.core import run_sim, dsls

#-------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------

config = Config(
  ports = [
    ( "out", OutputPort(8) ),
  ],
)

#-------------------------------------------------------------------------
# test_case_small
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "dslstr", dsls.keys() )
def test_case_small( dslstr ):
  run_sim( dslstr, __file__, config )

