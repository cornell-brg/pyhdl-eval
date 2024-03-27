
# PyMTL Auto-Evaluation for Hardware Design and Verification

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
 % module restore ${CBATTEN_INSTALL}/collections/pymtl-eval
```

You can also recreate this environment with just a minimal set of
environment modules like this:

```
 % module purge
 % module load iverilog/12.0
 % module load gtkwave/3.3.117
 % module load python3/3.11.0

 % mkdir ${HOME}/venvs
 % cd ${HOME}/venvs
 % python3 -m venv py3.11.0-pymtl-eval
 % source py3.11.0-pymtl-eval/bin/activate

 % pip config --site set global.index-url \
     https://urm.nvidia.com/artifactory/api/pypi/nv-shared-pypi/simple

 % pip install --upgrade pip
 % pip install adlrchat
```

In order to use the LLM gateway you need to log-in to the server.

```
 % export FASTCHAT_HEADLESS="True"
 % adlrchat-login --servername llm_gateway --role adlrchat-chipnemo-llmgateway
```

### Clone the Repos

You should clone this repo as well as the pregen repo which has
pre-generated content to avoid having requery the LLM. This also ensures
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
testing with just two samples.

```
 % cd $TOPDIR
 % git checkout 2024-02-28-baseline

 % mkdir $TOPDIR/build-baseline-tiny
 % cd $TOPDIR/build-baseline-tiny
 % ../configure --with-pregen=../../pymtl-eval-pregen/2024-02-28-baseline-tiny
 % make -j16
 ...
 pass_rate = 41.99
```

Now we can reproduce the full 20 sample experiment although this will
take 10-15 minutes.

```
 % cd $TOPDIR
 % git checkout 2024-02-28-baseline

 % mkdir $TOPDIR/build-baseline
 % cd $TOPDIR/build-baseline
 % ../configure --with-pregen=../../pymtl-eval-pregen/2024-02-28-baseline
 % make -j16
 ...
 pass_rate = 42.24
```

### Reproduce Other Results

Here are all of the reproducible experiments.

| tag                             | comment                                               |
|---------------------------------|-------------------------------------------------------|
| 2024-02-28-baseline             | VerilogEval baseline with my scripts                  |
| 2024-03-04-prompt-ifc           | Reframed prompt with cleaner interface                |
| 2024-03-10-prompt-ifc-chipnemo  | Reframed prompt with cleaner interface using ChipNemo |
| 2024-03-05-const-logic-reset    | Reframed prompt with in-context rules                 |
| 2024-03-26-pymtl-eval-initial   | Initial PyMTL eval experiment with three problems     |

You can reproduce these experiments as follows.

```
 % cd $TOPDIR
 % git checkout tag

 % mkdir $TOPDIR/build-tag
 % cd $TOPDIR/build-tag
 % ../configure --with-pregen=../../pymtl-eval-pregen/tag
 % make -j16
```

