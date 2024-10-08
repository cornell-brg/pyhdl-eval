#=========================================================================
# Toplevel configure.ac for running LLM codegen experiments
#=========================================================================
# SPDX-License-Identifier: MIT
# Author : Christopher Batten, NVIDIA
# Date   : May 20, 2024

#-------------------------------------------------------------------------
# Project metadata
#-------------------------------------------------------------------------

m4_define( proj_name,         [LLM Code Generation Experiments])
m4_define( proj_maintainer,   [Christopher Batten])
m4_define( proj_abbreviation, [pyhdl-eval])
m4_define( proj_version,      [v0.1])

#-------------------------------------------------------------------------
# Setup
#-------------------------------------------------------------------------

AC_INIT(proj_name,proj_version,proj_maintainer,proj_abbreviation)
AC_CONFIG_SRCDIR([dataset/problems.txt])

#-------------------------------------------------------------------------
# Basic checks
#-------------------------------------------------------------------------

# Checking for iverilog

AC_CHECK_PROGS([IVERILOG],[iverilog],[no])
AS_IF([test "${IVERILOG}" = "no"],
[
  AC_MSG_ERROR([Must have iverilog installed!])
])

# Checking for python

AC_CHECK_PROGS([PYTHON],[python],[no])
AS_IF([test "${PYTHON}" = "no"],
[
  AC_MSG_ERROR([Must have python installed!])
])

AC_MSG_NOTICE([checking whether $PYTHON is version 3+])
python_version=`${PYTHON} --version 2>&1 | cut -d' ' -f2`
python_major_version=`echo $python_version | cut -d. -f1`
AS_IF([test "${python_major_version}" != 3],
[
  AC_MSG_ERROR([Must have python3 installed!])
])

# Checking for pytest

AC_CHECK_PROGS([PYTEST],[pytest],[no])
AS_IF([test "${PYTEST}" = "no"],
[
  AC_MSG_ERROR([Must have pytest installed!])
])

#-------------------------------------------------------------------------
# create config.mk file
#-------------------------------------------------------------------------

AC_MSG_NOTICE([creating config.mk])

cat > config.mk \
<<'END'
#=========================================================================
# problems.mk
#=========================================================================
# Generated by the configure script.

END

#-------------------------------------------------------------------------
# --with-ref-test
#-------------------------------------------------------------------------

AC_ARG_WITH(ref-test,
  AS_HELP_STRING([--with-ref-test],[Enable testing Verilog reference implementations]),
  [cfg_ref_test="yes"],
  [cfg_ref_test="no"])

AC_MSG_NOTICE([testing Verilog reference: ${cfg_ref_test}])
echo "cfg_ref_test:=${cfg_ref_test}" >> config.mk

#-------------------------------------------------------------------------
# --without-verilog
#-------------------------------------------------------------------------

AC_ARG_WITH(verilog,
  AS_HELP_STRING([--without-verilog],[Disable evaluating LLM-generated Verilog]),
  [cfg_verilog="no"],
  [cfg_verilog="yes"])

AC_MSG_NOTICE([evaluate llm-generated verilog: ${cfg_verilog}])
echo "cfg_verilog:=${cfg_verilog}" >> config.mk

#-------------------------------------------------------------------------
# --with-pydsl
#-------------------------------------------------------------------------

AC_ARG_WITH(pydsl,
  AS_HELP_STRING([--with-pydsl],[Enable evaluating LLM-generated Python-embedded DSL]),
  [cfg_pydsl="${with_pydsl}"],
  [cfg_pydsl="no"])

AC_MSG_NOTICE([evaluate llm-generated python-embedded dsl: ${cfg_pydsl}])
echo "cfg_pydsl:=${cfg_pydsl}" >> config.mk

#-------------------------------------------------------------------------
# --with-examples
#-------------------------------------------------------------------------

AC_ARG_WITH(examples,
  AS_HELP_STRING([--with-examples],[Number of in-contex learning examples]),
  [cfg_examples="${with_examples}"],
  [cfg_examples="0"])

AC_MSG_NOTICE([number of in-context learning examples: ${cfg_examples}])
echo "cfg_examples:=${cfg_examples}" >> config.mk

#-------------------------------------------------------------------------
# --with-model
#-------------------------------------------------------------------------

AC_ARG_WITH(model,
  AS_HELP_STRING([--with-model],[Large language model to use]),
  [cfg_model="${with_model}"],
  [cfg_model="openai/gpt3.5-turbo"])

AC_MSG_NOTICE([using model: ${cfg_model}])
echo "cfg_model:=${cfg_model}" >> config.mk

#-------------------------------------------------------------------------
# --with-dataset
#-------------------------------------------------------------------------

AC_ARG_WITH(dataset,
  AS_HELP_STRING([--with-dataset],[Directory with dataset files]),
  [cfg_dataset="${with_dataset}"],
  [cfg_dataset="${srcdir}/dataset"])

AC_MSG_NOTICE([using dataset: ${cfg_dataset}])
echo "cfg_dataset:=${cfg_dataset}" >> config.mk

#-------------------------------------------------------------------------
# --with-problems
#-------------------------------------------------------------------------

AC_ARG_WITH(problems,
  AS_HELP_STRING([--with-problems],[File with list of problems]),
  [cfg_problems="${with_problems}"],
  [cfg_problems="${cfg_dataset}/problems.txt"])

AC_MSG_NOTICE([using problems: ${cfg_problems}])
echo "cfg_problems:=${cfg_problems}" >> config.mk

#-------------------------------------------------------------------------
# --with-samples
#-------------------------------------------------------------------------

AC_ARG_WITH(samples,
  AS_HELP_STRING([--with-samples],[Number of samples per problem]),
  [cfg_samples="${with_samples}"],
  [cfg_samples="20"])

AC_MSG_NOTICE([using samples: ${cfg_samples}])
echo "cfg_samples:=${cfg_samples}" >> config.mk

#-------------------------------------------------------------------------
# create config.mk file
#-------------------------------------------------------------------------

AC_MSG_NOTICE([adding problems to config.mk])

echo "" >> config.mk

cat >> config.mk \
<<'END'
problems = \
END

sed -e '/^\s*$/d' -e 's/^\(.*\)$/  \1 \\/' \
    ${cfg_problems} >> config.mk

echo "" >> config.mk

#-------------------------------------------------------------------------
# pregen
#-------------------------------------------------------------------------

AC_ARG_WITH(pregen-dir,
  AS_HELP_STRING([--with-pregen-dir],[Directory for storing pregen files]),
  [cfg_pregen_dir="${with_pregen_dir}"],
  [cfg_pregen_dir="DEFAULT"])

AS_IF([ test "${cfg_pregen_dir}" != "DEFAULT" ],
[
  AC_MSG_NOTICE([using pregen dir: ${cfg_pregen_dir}])
],[
  if [[ -d "../../pyhdl-eval-pregen" ]]; then
    cfg_pregen_dir="../../pyhdl-eval-pregen"
    AC_MSG_NOTICE([using pregen dir: ${cfg_pregen_dir}])
  else
    AC_MSG_NOTICE([no pregen dir specified])
  fi
])

echo "cfg_pregen_dir:=${cfg_pregen_dir}" >> config.mk
echo "" >> config.mk

AC_ARG_WITH(pregen,
  AS_HELP_STRING([--with-pregen],[Use pregen files]),
  [cfg_pregen="${with_pregen}"],
  [cfg_pregen="no"])

AS_IF([ test "${cfg_pregen}" != "no" ],
[
  AC_MSG_NOTICE([using pregen: ${cfg_pregen}])
  cp -r ${cfg_pregen}/* .
])

#-------------------------------------------------------------------------
# Output
#-------------------------------------------------------------------------

AC_CONFIG_FILES([Makefile])
AC_OUTPUT
