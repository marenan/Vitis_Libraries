/*
 * Copyright 2022 Xilinx, Inc.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef __DEVICE_DEFS__
#define __DEVICE_DEFS__

// Preamble
// This file exists to make preprocessor clauses more readable by abstracting the trait of the device that the clause
// depends on
// rather than some oblique reference to the device.
// This file is used by both UUT and REF.
// Glossary:
// __AIE_ARCH__ can take values 10 (AIE1), 20 (AIE2, aka AIE-ML), 21 (AIE_PS), 22 (AIE_PS2)
// Even though most of these could be expressed in a boolean fashion, the convention is to use int
// so that in the UUT code you can write #if __X__ == 1 || __Y__ ==2 which becomes awkward with defined(__Y__).

// Error trap for unidentified arch
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10) || (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || \
    (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
// all ok
#else
//#error Unexpected __AIE_ARCH__ or __AIEARCH__ encountered //removed because compilation of gen_cfo.cpp fails here
#endif

//----------------------------------
// FFT R4 stage support. AIE2 supports true Radix4, but AIE1 spoofs this with 2 stages of radix2.
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __FFT_R4_IMPL__ 0
#endif

#if (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || \
    (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
#define __FFT_R4_IMPL__ 1
#endif

//----------------------------------
// FFT cfloat support
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_CFLOAT__ 1
// #warning Supports cfloats

#else
#define __SUPPORTS_CFLOAT__ 0
// #warning AIE Architecture does not supports cfloats
#endif

#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __HAS_SYM_PREADD__ 1
#else
#define __HAS_SYM_PREADD__ 0
#endif

//----------------------------------
// Accumulator widths
// reference to accumulator widths which do not exist on a device leads to a compile time error. These definitions allow
// such code to be claused out prior to that stage of compilation.
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_ACC48__
#define __SUPPORTS_ACC80__
#endif

#if (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || \
    (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
#define __SUPPORTS_ACC32__
#define __SUPPORTS_ACC64__
#endif

//----------------------------------
// Stream support
// clauses getc_wss
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_GETC_WSS__
#endif

//----------------------------------
// Cascade support
// clauses put_mcd and get_scd_v8int32
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_PUT_MCD__
#endif

#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __STREAMS_PER_TILE__ 2
#elif (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || \
    (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
#define __STREAMS_PER_TILE__ 1
#else
// error trap
#define __STREAMS_PER_TILE__ -1
#endif

#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define MCD_SIZE 256
#define SCD_SIZE 256
#else
#define MCD_SIZE 512
#define SCD_SIZE 512
#endif

//----------------------------------
// Misc
// not equal
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_NE32__
#endif

//----------------------------------
// SINCOS scalar intrinsic present in hw in AIE1 but not in AIE2
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SINCOS_IN_HW__ 1
#endif

#if (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || \
    (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
#define __SINCOS_IN_HW__ 0
#endif

//----------------------------------
// v8int16 supported in AIE1, not AIE2
#if (__AIE_ARCH__ == 10) || (__AIEARCH__ == 10)
#define __SUPPORTS_V8INT16__ 1
#define __SUPPORTS_V16INT16__ 1
#endif

#if (__AIE_ARCH__ == 20) || (__AIE_ARCH__ == 21) || (__AIE_ARCH__ == 22) || (__AIEARCH__ == 20) || \
    (__AIEARCH__ == 21) || (__AIEARCH__ == 22)
#define __SUPPORTS_V8INT16__ 0
#define __SUPPORTS_V16INT16__ 0
#endif

#endif // __DEVICE_DEFS__
