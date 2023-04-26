# Copyright (C) 2019-2022, Xilinx, Inc.
# Copyright (C) 2022-2023, Advanced Micro Devices, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# vitis hls makefile-generator v2.0.0

source settings.tcl

set PROJ "dispNnzCol_test.prj"
set SOLN "sol"

if {![info exists CLKP]} {
  set CLKP 3.3333
}

open_project -reset $PROJ

add_files "${XF_PROJ_ROOT}/L1/tests/hw/dispNnzCol/uut_top.cpp" -cflags "-I ${XF_PROJ_ROOT}/../blas/L1/include/hw -I ${XF_PROJ_ROOT}/L1/tests/hw -I ${XF_PROJ_ROOT}/L1/include/hw -g -O0 -std=c++11 -DSPARSE_maxColParBlocks=256 -DSPARSE_hbmChannels=16 -DSPARSE_dataType=float -DSPARSE_logParEntries=2 -DSPARSE_parEntries=4 -DSPARSE_dataBits=32 -DSPARSE_printWidth=6"
add_files -tb "${XF_PROJ_ROOT}/L1/tests/hw/dispNnzCol/test.cpp" -cflags "-I ${XF_PROJ_ROOT}/../blas/L1/include/hw -I ${XF_PROJ_ROOT}/L1/tests/hw -I ${XF_PROJ_ROOT}/L1/include/hw -g -O0 -std=c++11 -DSPARSE_maxColParBlocks=256 -DSPARSE_hbmChannels=16 -DSPARSE_dataType=float -DSPARSE_logParEntries=2 -DSPARSE_parEntries=4 -DSPARSE_dataBits=32 -DSPARSE_printWidth=6 -I ${XF_PROJ_ROOT}/L1/include/sw"
set_top uut_top

open_solution -reset $SOLN



set_part $XPART
create_clock -period $CLKP

if {$CSIM == 1} {
  csim_design
}

if {$CSYNTH == 1} {
  csynth_design
}

if {$COSIM == 1} {
  cosim_design
}

if {$VIVADO_SYN == 1} {
  export_design -flow syn -rtl verilog
}

if {$VIVADO_IMPL == 1} {
  export_design -flow impl -rtl verilog
}

exit