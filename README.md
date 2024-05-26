
# PyHDL-Eval: LLM Evaluation for Python-Based Hardware Design Languages

This repo contains a new benchmark and framework specifically designed to
evaluate LLMs on specification-to-RTL tasks when targeting Verilog and
the following five different Python-embedded DSLs:

 - PyMTL (https://github.com/pymtl/pymtl3)
 - PyRTL (https://github.com/UCSBarchlab/PyRTL)
 - MyHDL (https://github.com/myhdl/myhdl)
 - Migen (https://github.com/m-labs/migen)
 - Amaranth (https://github.com/amaranth-lang/amaranth)

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

Although you can install PyMTL3 using pip, we want to use a more advanced
development version which means we need to install it from source.

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

We can use a simple full adder example to verify PyMTL3 and Verilator are
installed and working correctly.

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

The remaning Python-embedded DSLs can be installed from source; the
versions used in this project are shown below.

```
 % pip install pyrtl==0.11.1
 % pip install myhdl==0.11.45
 % pip install migen==0.9.2
 % pip install amaranth[builtin-yosys]==0.4.5
```

You will also need the following Python packages:

```
 % pip install langchain==0.1.16
 % pip install langchain-openai==0.1.3
 % pip install langchain-nvidia-ai-endpoints==0.0.11
```

### Basic Testing

Clone the repo.

```
 % mkdir -p $HOME/vc/git-hub/nvlabs
 % cd $HOME/vc/git-hub/nvlabs
 % git clone git@github.com:nvlabs/pyhdl-eval.git
 % cd pyhdl-eval
 % TOPDIR=$PWD
```

We can start by running all of the tests for the `pyhdl_eval` framework
which compares a Verilog reference to PyMTL3, PyRTL, MyHDL, Migen, and
Amaranth implementations of several examples.

```
 % mkdir $TOPDIR/build
 % cd $TOPDIR/build
 % pytest ../dataset
```

We can then compare the Verilog reference implementation to itself using
the Python test benches to ensure these parts of the framework are
working correctly.

```
 % mkdir $TOPDIR/build
 % cd $TOPDIR/build
 % pytest ../dataset
```

We can also compare the Verilog reference implementation to itself using
the Verilog test benches to ensure that these final parts of the
framework are working correctly.

```
 % mkdir $TOPDIR/build
 % cd $TOPDIR/build
 % ../configure --with-ref-test --with-samples=1
 % make
```

Now we can run an experiment comparing an LLM in generating Verilog vs. a
Python-embedded DSL using the default LLM (openai/gpt3.5-turbo) and 20
samples per problem.

```
 % mkdir $TOPDIR/build-verilog-vs-pymtl
 % cd $TOPDIR/build-verilog-vs-pymtl
 % ../configure --with-pydsl=pymtl
 % make
```

We can also experiment with other Python-embedded DSLs using separate
build directories, although we may not want to regenerate all of the
Verilog samples every time.

```
 % mkdir $TOPDIR/build-pyrtl
 % cd $TOPDIR/build-pyrtl
 % ../configure --without-verilog --with-pydsl=pyrtl
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

