
# PyHDL-Eval: LLM Evaluation for Python-Based Hardware Design Languages

This repo contains a new benchmark and framework specifically designed to
evaluate LLMs on specification-to-RTL tasks when targeting Verilog and
the following five different Python-embedded DSLs:

 - PyMTL3
 - PyRTL
 - MyHDL
 - Migen
 - Amaranth

The benchmark includes 150+ problems developed using an ontological
approach to cover almost 20 subclasses of RTL design. The framework
includes workflow orchestration scripts, in-context learning examples,
Verilog reference solutions, Verilog test benches, Python test scripts,
and a common Python API to enable easily adding new Python-embedded DSLs
for evaluation.

### Setup Linux Environment

In order to use PyHDL-Eval you will need to install iverilog, verilator,
and python3 along with several Python packages. These are the versions
which were used for this project:

 - iverilog (v12)
 - verilator (v5.016)
 - python3 (v3.11.0)

Here is how to install PyMTL3:

```
 % mkdir -p ${HOME}/vc/git-hub/pymtl
 % cd ${HOME}/vc/git-hub/pymtl
 % git clone git@github.com:pymtl/pymtl3
 % cd ${HOME}/vc/git-hub/pymtl/pymtl3
 % git checkout pymtl4.0-dev
 % pip install -r requirements.txt
 % pip install -e .
 % pip list
```

Here is how to test that PyMTL3 is working:

```
 % rm -rf ${HOME}/tmp/misc/pymtl3-test
 % mkdir -p ${HOME}/tmp/misc/pymtl3-test
 % cd ${HOME}/tmp/misc/pymtl3-test
 % cat > pymtl_test.py \
<<'END'
from pymtl3 import *
from pymtl3.passes.backends.verilog import *
from pymtl3.examples.ex00_quickstart import FullAdder
fa = FullAdder()
fa.set_metadata( VerilogTranslationImportPass.enable, True )
fa.apply( VerilogPlaceholderPass() )
fa = VerilogTranslationImportPass()( fa )

fa.apply( DefaultPassGroup(textwave=True) )
fa.sim_reset()
fa.a   @= 0
fa.b   @= 1
fa.cin @= 0
fa.sim_tick()
fa.a   @= 1
fa.b   @= 0
fa.cin @= 1
fa.sim_tick()
fa.print_textwave()
END

 % python pymtl_test.py
```

Here is how to install the other Python-embedded DSLS:

```
 % pip install pyrtl
 % pip install myhdl
 % pip install migen
 % pip install amaranth[builtin-yosys]
```

You will also need the following Python packages:

```
 % pip install langchain
 % pip install langchain-openai
 % pip install langchain-nvidia-ai-endpoints
```

### Basic Testing

Here is how to clone the repo:

```
 % mkdir -p $HOME/vc/git-hub/nvlabs
 % cd $HOME/vc/git-hub/nvlabs
 % git clone git@github.com:nvlabs/pyhdl-eval.git
 % cd pyhdl-eval
 % TOPDIR=$PWD
```

Here is how to run the tests for the pyhdl_eval framework and to also
test all of the Verilog reference solutions using the Python test
scripts.

```
 % mkdir $TOPDIR/build
 % cd $TOPDIR/build
 % pytest ../pyhdl_eval
 % pytest ../dataset
```

Here is how to test all of the Verilog reference solutions using the
Verilog test benches.

```
 % mkdir $TOPDIR/build
 % cd $TOPDIR/build
 % ../configure --with-ref-test
 % make
```

Here is how to run an experiment comparing an LLM in generating Verilog
vs. a Python-embedded DSL using the default LLM (openai/gpt3.5-turbo) and
20 samples per problem.

```
 % mkdir $TOPDIR/build-verilog-vs-pymtl
 % cd $TOPDIR/build-verilog-vs-pymtl
 % ../configure --with-pydsl=pymtl
 % make

 % mkdir $TOPDIR/build-verilog-vs-pyrtl
 % cd $TOPDIR/build-verilog-vs-pyrtl
 % ../configure --with-pydsl=pyrtl
 % make

 % mkdir $TOPDIR/build-verilog-vs-myhdl
 % cd $TOPDIR/build-verilog-vs-myhdl
 % ../configure --with-pydsl=myhdl
 % make

 % mkdir $TOPDIR/build-verilog-vs-migen
 % cd $TOPDIR/build-verilog-vs-migen
 % ../configure --with-pydsl=migen
 % make

 % mkdir $TOPDIR/build-verilog-vs-amaranth
 % cd $TOPDIR/build-verilog-vs-amaranth
 % ../configure --with-pydsl=amaranth
 % make
```

Each of the above experiments will regenerate all of the Verilog samples,
so an alternative approach to use one build directory to evaluate Verilog
and a separate build directory to evaluate each of the Python-embedded
DSLs.

```
 % mkdir $TOPDIR/build-verilog
 % cd $TOPDIR/build-verilog
 % ../configure
 % make

 % mkdir $TOPDIR/build-pyrtl
 % cd $TOPDIR/build-pyrtl
 % ../configure --without-verilog --without-verilog --without-verilog --with-pydsl=pyrtl
 % make

 % mkdir $TOPDIR/build-myhdl
 % cd $TOPDIR/build-myhdl
 % ../configure --without-verilog --with-pydsl=myhdl
 % make

 % mkdir $TOPDIR/build-migen
 % cd $TOPDIR/build-migen
 % ../configure --without-verilog --with-pydsl=migen
 % make

 % mkdir $TOPDIR/build-amaranth
 % cd $TOPDIR/build-amaranth
 % ../configure --without-verilog --with-pydsl=amaranth
 % make
```

