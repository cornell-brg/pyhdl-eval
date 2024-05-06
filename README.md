
# PyHDL-Eval: LLM Evaluation for Python-Based Hardware Design Languages

This repo contains our LLM evaluation framework for Python-based hardware
design languages. Currently this just includes PyMTL but could eventually
include PyRTL, MyHDL, and Amaranth. The framework also supports
evaluating Verilog HDL which can serve as a baseline for the Python-based
HDLs. The repo includes a dataset as plain text files and also includes
generation and analysis scripts and a Makefile to drive the workflow. The
generation script includes support for easily changing the LLM model and
including/excluding in-context learning rules and in-context learning
examples. The analysis script includes support for categorizing common
errors and outputing the results in both plain text and CSV files.

This README provides step-by-step instructions on how to reproduce
various results in the project.

### Setup Linux Environment

The following commands enable you to use an updated version of
environment modules and my own modulefiles.

```
 % module purge
 % export CBATTEN_INSTALL="/home/scratch.cbatten_research/install"
 % export PATH="${CBATTEN_INSTALL}/pkgs/modules-5.3.1/bin:$PATH"
 % source ${CBATTEN_INSTALL}/pkgs/modules-5.3.1/init/bash
 % module use ${CBATTEN_INSTALL}/modules
```

If you use tcsh instead of `bash` you will need to do the following. Note
that since I don't use `tcsh`, this workflow is only thoroughly tested
using `bash`.

```
 % module purge
 % setenv CBATTEN_INSTALL "/home/scratch.cbatten_research/install"
 % setenv PATH "${CBATTEN_INSTALL}/pkgs/modules-5.3.1/bin:$PATH"
 % source ${CBATTEN_INSTALL}/pkgs/modules-5.3.1/init/tcsh
 % module use ${CBATTEN_INSTALL}/modules
```

If you use the following module collection, then your environment
(including the python virtual environment) will be exactly the same as
what I use.

```
 % module restore ${CBATTEN_INSTALL}/collections/pyhdl-eval
```

You can also recreate this environment with just a minimal set of
environment modules like this:

```
 % module purge
 % module load iverilog/12.0
 % module load gtkwave/3.3.117
 % module load verilator/5.016
 % module load python3/3.11.0

 % mkdir ${HOME}/venvs
 % cd ${HOME}/venvs
 % python3 -m venv py3.11.0-pyhdl-eval
 % source py3.11.0-pyhdl-eval/bin/activate
 % pip install --upgrade pip

 % mkdir -p ${HOME}/vc/git-hub/pymtl
 % cd ${HOME}/vc/git-hub/pymtl
 % git clone git@github.com:pymtl/pymtl3
 % cd ${HOME}/vc/git-hub/pymtl/pymtl3
 % git checkout pymtl4.0-dev
 % pip install -r requirements.txt
 % pip install -e .

 % pip config --site set global.index-url \
     https://urm.nvidia.com/artifactory/api/pypi/nv-shared-pypi/simple

 % pip install adlrchat
 % pip install langchain-nvidia-ai-endpoints
```

In order to use the LLM gateway you need to log-in to the server.

```
 % export FASTCHAT_HEADLESS="True"
 % adlrchat-login --servername llm_gateway     --role adlrchat-chipnemo-llmgateway
 % adlrchat-login --servername amazing-rooster --role fastchat-chipnemo
```

### Clone the Repos

You should clone this repo as well as the pregen repo which has
pre-generated content to avoid having requery the LLM. This also ensures
the results are reproducible since obviously the same LLM query can
produce different response. If you want to rerun the LLM queries in any
of the experiments below, just do not use the --with-pregen configure
option.

```
 % mkdir -p $HOME/vc/git-nvidia/avr
 % cd $HOME/vc/git-nvidia/avr
 % git clone ssh://git@gitlab-master.nvidia.com:12051/avr/pyhdl-eval-pregen.git
 % git clone ssh://git@gitlab-master.nvidia.com:12051/avr/pyhdl-eval.git
 % cd pyhdl-eval
 % TOPDIR=$PWD
```

### Test the Verilog Reference Solutions

You can use pytest to verify that the PyMTL reference models match the
Verilog reference models like this:

```
 % mkdir $TOPDIR/build-test-ref
 % cd $TOPDIR/build-test-ref
 % pytest ../dataset
```

### Reproduce Initial Results with GPT4 Turbo

Here is how to reproduce a very simple initial experiment using GPT4
Turbo on seven problems.

```
 % cd $TOPDIR
 % git checkout 2024-04-22

 % mkdir $TOPDIR/build-gpt4-turbo-icl-ex
 % cd $TOPDIR/build-gpt4-turbo-icl-ex
 % ../configure --with-model=gpt4-turbo --with-examples \
     --with-pregen=../../pyhdl-eval-pregen/2024-04-22/gpt4-turbo-icl-ex
 % make -j16
                                    iverilog (100%)          verilator (100%)         PyMTL (100%)
                                    -----------------------  -----------------------  -----------------------
 Prob01p01_comb_const_zero          ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob01p02_comb_const_one           ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob01p03_comb_const_lohi          ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob01p04_comb_const_32b_value     ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob01p05_comb_const_param         ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob02p01_comb_wires_8b_passthru   ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
 Prob03p01_comb_gates_nor           ..... ..... ..... .....  ..... ..... ..... .....  ..... ..... ..... .....
```

