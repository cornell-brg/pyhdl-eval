
# PyMTL Auto-Evaluation for Hardware Design and Verification

This README provides step-by-step instructions on how to reproduce
various results in the project.

### Setup Linux Environment

First you can use my environment modules to reproduce my
development environment.

```
 % module purge
 % setenv PATH "/home/cbatten/install/pkgs/modules-5.3.1/bin:$PATH"
 % source /home/cbatten/install/pkgs/modules-5.3.1/init/tcsh
 % module use /home/cbatten/install/modules
 % module restore /home/cbatten/.module/py3.11.0-llm-pymtl3
```

### Clone the Repos

You should clone this repo as well as the pregen repo which has
pregenerated content to avoid having requery the LLM. This also ensures
the results are reproducible since obviously the same LLM query can
produce different response. If you want to rerun the LLM queries in any
of the experiments below, just do not use the --with-pregen configure
option.

```
 % mkdir -p $HOME/vc/git-nvidia/cbatten
 % cd $HOME/vc/git-nvidia/cbatten
 % git clone ssh://git@gitlab-master.nvidia.com:12051/cbatten/pymtl-eval-pregen.git
 % git clone ssh://git@gitlab-master.nvidia.com:12051/cbatten/pymtl-eval.git
 % cd pymtl-eval
 % TOPDIR=$PWD
```

### Reproduce Baseline Results

Let's first reproduce the VerilogEval experiment using iverilog for the
testing. We reproduce the full 20 sample experiment as well as just the 2
sample experiment.

```
 % mkdir $TOPDIR/build-baseline-20samples
 % cd $TOPDIR/build-baseline-20samples
 % ../configure --with-pregen=../../pymtl-eval-pregen/2024-02-28-baseline-20samples
 % make -j16
 ...
 pass_rate = 42.24

 % mkdir $TOPDIR/build-baseline-2samples
 % cd $TOPDIR/build-baseline-2samples
 % ../configure --with-pregen=../../pymtl-eval-pregen/2024-02-28-baseline-2samples
 % make NUM_SAMPLES=2 -j16
 ...
 pass_rate = 41.99
```

