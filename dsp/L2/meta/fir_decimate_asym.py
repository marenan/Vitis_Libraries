from aie_common import *
from aie_common_fir import *
import json
import fir_sr_asym as sr_asym
import fir_polyphase_decomposer as poly

import importlib
from pathlib import Path
current_uut_kernel = Path(__file__).stem
# fir_decimate_asym.hpp:        // static_assert(TP_FIR_RANGE_LEN >= FIR_LEN_MIN,"ERROR: Illegal combination of design FIR length and cascade length, resulting in kernel FIR length below minimum required value. ");
# fir_decimate_asym.hpp:        static_assert(TP_FIR_LEN % TP_DECIMATE_FACTOR == 0,"ERROR: TP_FIR_LEN must be a multiple of TP_DECIMATE_FACTOR");
# fir_decimate_asym.hpp:        static_assert(TP_FIR_RANGE_LEN % TP_DECIMATE_FACTOR == 0,"ERROR: Illegal combination of design FIR length and cascade length. TP_FIR_RANGE_LEN must be a multiple of TP_DECIMATE_FACTOR");
# fir_decimate_asym.hpp:        static_assert(TP_DECIMATE_FACTOR >= DECIMATE_FACTOR_MIN && TP_DECIMATE_FACTOR <= DECIMATE_FACTOR_MAX, "ERROR:TP_DECIMATE_FACTOR is outside the supported range.");
# fir_decimate_asym.hpp:        static_assert(TP_SHIFT >= SHIFT_MIN && TP_SHIFT <= SHIFT_MAX, "ERROR: TP_SHIFT is out of the supported range.");
# fir_decimate_asym.hpp:        static_assert(TP_RND >= ROUND_MIN && TP_RND <= ROUND_MAX, "ERROR: TP_RND is out of the supported range.");
# fir_decimate_asym.hpp:        static_assert(TP_SAT >= SAT_MODE_MIN && TP_SAT <= SAT_MODE_MAX, "ERROR: TP_SAT is out of supported range");
# fir_decimate_asym.hpp:        static_assert(TP_SAT != 2, "ERROR: TP_SAT is invalid. Valid values of TP_SAT are 0, 1, and 3");
# fir_decimate_asym.hpp:        static_assert(fnEnumType<TT_DATA>() != enumUnknownType,"ERROR: TT_DATA is not a supported type.");
# fir_decimate_asym.hpp:        static_assert(fnEnumType<TT_COEFF>() != enumUnknownType,"ERROR: TT_COEFF is not a supported type.");
# fir_decimate_asym.hpp:        static_assert(fnFirDecAsymTypeSupport<TT_DATA, TT_COEFF>() != 0, "ERROR: The combination of TT_DATA and TT_COEFF is not supported for this class.");
# fir_decimate_asym.hpp:        static_assert(fnTypeCheckDataCoeffSize<TT_DATA,TT_COEFF>() != 0, "ERROR: TT_DATA type less precise than TT_COEFF is not supported.");
# fir_decimate_asym.hpp:        static_assert(fnTypeCheckDataCoeffCmplx<TT_DATA,TT_COEFF>() != 0, "ERROR: real TT_DATA with complex TT_COEFF is not supported.");
# fir_decimate_asym.hpp:        static_assert(fnTypeCheckDataCoeffFltInt<TT_DATA,TT_COEFF>() != 0, "ERROR: a mix of float and integer types of TT_DATA and TT_COEFF is not supported.");
# fir_decimate_asym.hpp:        static_assert(TP_NUM_OUTPUTS >0 && TP_NUM_OUTPUTS <=2, "ERROR: only single or dual outputs are supported." );
# fir_decimate_asym.hpp:        static_assert(!(std::is_same<TT_DATA,cfloat>::value || std::is_same<TT_DATA,float>::value) || (TP_SHIFT == 0), "ERROR: TP_SHIFT cannot be performed for TT_DATA=cfloat, so must be set to 0");
# fir_decimate_asym.hpp:        static_assert(TP_INPUT_WINDOW_VSIZE % (TP_DECIMATE_FACTOR*m_kLanes) == 0, "ERROR: TP_INPUT_WINDOW_VSIZE must be a multiple of TP_DECIMATE_FACTOR  and of the number of lanes for the MUL/MAC intrinsic");
# fir_decimate_asym.hpp:        static_assert(m_kDataRegVsize-m_kDataLoadVsize >= m_kDFDataRange, "ERROR: TP_DECIMATION_FACTOR exceeded for this data/coeff type combination. Required input data exceeds input vector's register offset address range.");
# fir_decimate_asym.hpp:        static_assert(!(m_kArch == kArchStream && m_kDFX  == kHighDF), "ERROR: TP_DECIMATION_FACTOR exceeded for this data/coeff type combination. Required input data exceeds input vector's register offset address range.");
# fir_decimate_asym.hpp:        static_assert(!(m_kArch == kArchStream &&  m_kInitDataNeeded >= m_kSamplesInBuff), "ERROR: TP_FIR_RANGE_LEN exceeds max supported range for this data/coeff type combination. Increase TP_CASC_LEN to split the workload over more kernels.");
# fir_decimate_asym.hpp:        static_assert(!(m_kArch == kArchStream && TP_INPUT_WINDOW_VSIZE % (TP_DECIMATE_FACTOR*m_kLanes*streamRptFactor) != 0), "ERROR: TP_INPUT_WINDOW_VSIZE must be a multiple of (TP_DECIMATE_FACTOR * 8)  and of the number of lanes for the streaming MUL/MAC intrinsic");
# fir_decimate_sym_graph.hpp:   static_assert(TP_CASC_LEN <= 40,"ERROR: Unsupported Cascade length");
# fir_decimate_sym_graph.hpp:   static_assert(TP_FIR_LEN / TP_CASC_LEN <= kMaxTapsPerKernel,"ERROR: Requested FIR length and Cascade length exceeds supported number of taps per kernel. Please increase the cascade legnth to accomodate the FIR design.");
# fir_decimate_sym_graph.hpp:   static_assert(TP_USE_COEFF_RELOAD == 0 || TP_FIR_LEN  <= kMaxTapsPerKernel,"ERROR: Exceeded maximum supported FIR length with reloadable coefficients. Please limit the FIR length or disable coefficient reload.");
# fir_decimate_sym_graph.hpp:   static_assert(TP_API != 0 || inBufferSize < kMemoryModuleSize, "ERROR: Input Window size (based on requrested window size and FIR length margin) exceeds Memory Module size of 32kB");
# fir_decimate_asym_graph.hpp:  static_assert(TP_CASC_LEN <= 40,"ERROR: Unsupported Cascade length");
# fir_decimate_asym_graph.hpp:  static_assert(TP_API == USE_STREAM_API || TP_DUAL_IP == DUAL_IP_SINGLE,"ERROR: Dual input ports only supported when port API is a stream. ");
# fir_decimate_asym_graph.hpp:  static_assert(TP_FIR_LEN / TP_CASC_LEN <= kMaxTapsPerKernel,"ERROR: Requested FIR length and Cascade length exceeds supported number of taps per kernel. Please increase the cascade legnth to accomodate the FIR design.");
# fir_decimate_asym_graph.hpp:  static_assert(TP_USE_COEFF_RELOAD == 0 || TP_FIR_LEN  <= kMaxTapsPerKernel,"ERROR: Exceeded maximum supported FIR length with reloadable coefficients. Please limit the FIR length or disable coefficient reload.");
# fir_decimate_asym_graph.hpp:  static_assert(TP_API != 0 || bufferSize < kMemoryModuleSize, "ERROR: Input Window size (based on requrested window size and FIR length margin) exceeds Memory Module size of 32kB");


#### naming ####
#
# Name functions with prefix
#   validate_ for validators, returning boolean result and error message as a tuple.
#   update_ for updators, returning object with default value and refined candidate constraints.
#   info_ for creating information based on parameters
#   fn_ for internal functions
#
# Name function arguments as template parameters, when possible
# so the code matches easier with API definition.


# Example of validator.
#
# The parameter itself will be passed as first argument for validator functions.
# These functions can have extra parameters as arguments, as specified as last part of in `validator`.
# These extra parameters must appear before current one in "parameters" section.
#
# A validator function returns a dictionary, with required boolean key "is_valid",
# and "err_message" if "is_valid" is False.
#

fn_decimate_asym_lanes = fnNumLanes384b

TP_DECIMATE_FACTOR_min = 2
TP_DECIMATE_FACTOR_max = 7
TP_INPUT_WINDOW_VSIZE_min = 4
TP_SSR_min = 1
TP_PARA_DECI_POLY_min = 1
TP_CASC_LEN_min = 1
TP_CASC_LEN_max = 40
TP_FIR_LEN_min = 4
TP_FIR_LEN_max = 8192
TP_SHIFT_min = 0
TP_SHIFT_max = 61
#TP_API_min=0
#TP_API_max=1
#TP_RND_min=0
#TP_RND_max=7
#AIE_VARIANT_min=1
#AIE_VARIANT_max=2
#TP_DUAL_IP_min=0
#TP_DUAL_IP_max=1
#TP_NUM_OUTPUTS_min=1
#TP_NUM_OUTPUTS_max=2
#TP_USE_COEF_RELOAD_min=0
#TP_USE_COEF_RELOAD_max=2


def fn_validate_input_window_size(TT_DATA, TT_COEF, TP_FIR_LEN, TP_DECIMATE_FACTOR, TP_INPUT_WINDOW_VSIZE, TP_API, TP_SSR=1):
  # CAUTION: this constant overlaps many factors. The main need is a "strobe" concept that means we unroll until xbuff is back to starting conditions.
  # So number of lanes * decimation factor is the incremental sample need; Which might require a load (which is fixed to 256b currently)
  # This load might load enough samples of X operations, but we can map out that we will need 3 additional 256b loads to wrap round our 1024b buffer
  # Given that we know there will be 3 additional loads, we need to work out how many output vector chunks that covers.
  # 8 seems to work for all current decimation values and lanes across data types..
  streamRptFactor = 8
  if TP_INPUT_WINDOW_VSIZE < TP_INPUT_WINDOW_VSIZE_min:
	    return isError(f"Minimum value for Input window size is {TP_INPUT_WINDOW_VSIZE_min}, but got {TP_INPUT_WINDOW_VSIZE}.")

  # decimator uses 384b accs, but also checks for multiple of decimate factor. When using streams, also takes into account the stream repeat factor.
  windowSizeMultiplier = (fn_decimate_asym_lanes(TT_DATA, TT_COEF)*TP_DECIMATE_FACTOR) if TP_API == 0 else (fn_decimate_asym_lanes(TT_DATA, TT_COEF)*TP_DECIMATE_FACTOR*streamRptFactor)

  # Slightly cheating here by putting in numLanes as the multiplied value.
  checkMultipleLanes =  fn_windowsize_multiple_lanes(TT_DATA, TT_COEF, TP_INPUT_WINDOW_VSIZE, TP_API, numLanes=windowSizeMultiplier)
  #  also checks output size (this isn't done on static asserts for some reason right now)
  checkMaxBuffer = fn_max_windowsize_for_buffer(TT_DATA, TP_FIR_LEN, TP_INPUT_WINDOW_VSIZE, TP_API, TP_SSR, TP_INTERPOLATE_FACTOR=1)
  # Input samples are round-robin split to each SSR input paths, so total frame size must be divisable by SSR factor.
  checkIfDivisableBySSR = fn_windowsize_divisible_by_ssr(TP_INPUT_WINDOW_VSIZE, TP_SSR)

  for check in (checkMultipleLanes,checkMaxBuffer,checkIfDivisableBySSR):
    if check["is_valid"] == False :
      return check

  return isValid

def fn_multiple_decimation(TP_FIR_LEN,TP_DECIMATE_FACTOR, TP_CASC_LEN):
  # why? We already have range check and also can't we just zero-pad anyway??
  if ((TP_FIR_LEN % TP_DECIMATE_FACTOR) != 0) :
    return isError(f"Filter length ({TP_FIR_LEN}) must be a multiple of decimate factor ({TP_DECIMATE_FACTOR}).")

  for TP_KERNEL_POSITION in range(TP_CASC_LEN):
    #Check every kernel's init data needed (different kernels need different DataBuffXOffset)
    TP_FIR_RANGE_LEN =  (
      fnFirRangeRem(TP_FIR_LEN,TP_CASC_LEN,TP_KERNEL_POSITION,TP_DECIMATE_FACTOR)
        if (TP_KERNEL_POSITION == (TP_CASC_LEN-1))
        else
          fnFirRange(TP_FIR_LEN,TP_CASC_LEN,TP_KERNEL_POSITION,TP_DECIMATE_FACTOR)
    )
    if ((TP_FIR_RANGE_LEN % TP_DECIMATE_FACTOR) != 0) :
      return isError(f"Illegal combination of design filter length ({TP_FIR_LEN}) and cascade length ({TP_CASC_LEN}).")
  return isValid

def fn_data_needed_within_buffer_size(TT_DATA, TT_COEF, TP_FIR_LEN, TP_CASC_LEN, TP_API, TP_SSR, TP_DECIMATE_FACTOR):
    if(TP_API == 1):
        streamReadWidthDef = sr_asym.fnStreamReadWidth(TT_DATA, TT_COEF)
        streamReadWidth    = 256 if (TP_DECIMATE_FACTOR%2==0) else streamReadWidthDef
        m_kStreamLoadVsize = streamReadWidth / 8 / fn_size_by_byte(TT_DATA)
        m_kLanes           = fn_decimate_asym_lanes(TT_DATA, TT_COEF)
        m_kVOutSize        = m_kLanes
        TP_MODIFY_MARGIN_OFFSET = TP_SSR - 1
        m_kSamplesInBuff     = (1024//8)//fn_size_by_byte(TT_DATA)
        fir_len_per_ssr      = CEIL(TP_FIR_LEN, (TP_SSR * TP_DECIMATE_FACTOR))//TP_SSR
        for TP_KP in range(TP_CASC_LEN):
            TP_FIR_RANGE_LEN = fnFirRangeRem(fir_len_per_ssr, TP_CASC_LEN, TP_KP, TP_DECIMATE_FACTOR) if (TP_KP == TP_CASC_LEN - 1) else fnFirRange(fir_len_per_ssr,TP_CASC_LEN, TP_KP, TP_DECIMATE_FACTOR)
            m_kFirRangeOffset = sr_asym.fnFirRangeOffset(fir_len_per_ssr, TP_CASC_LEN, TP_KP, TP_DECIMATE_FACTOR)
            emptyInitLanes    = CEIL((fir_len_per_ssr - TP_FIR_RANGE_LEN - m_kFirRangeOffset), TP_DECIMATE_FACTOR) / TP_DECIMATE_FACTOR
            streamInitNullAccs           = emptyInitLanes/ m_kVOutSize
            dataNeededLastKernel         = 1 + TP_DECIMATE_FACTOR * (m_kLanes - 1) + (streamInitNullAccs * TP_DECIMATE_FACTOR * m_kLanes)
            dataOffsetNthKernel          = (fir_len_per_ssr - TP_FIR_RANGE_LEN - m_kFirRangeOffset)
            kMinDataNeeded = (TP_MODIFY_MARGIN_OFFSET + dataNeededLastKernel - dataOffsetNthKernel)
            kMinDataLoaded      = CEIL(kMinDataNeeded, m_kStreamLoadVsize)
            kMinDataLoadCycles = kMinDataLoaded/m_kStreamLoadVsize
            m_kFirRangeOffsetLastKernel    = sr_asym.fnFirRangeOffset(fir_len_per_ssr,TP_CASC_LEN,TP_CASC_LEN-1,TP_DECIMATE_FACTOR)
            m_kInitDataNeededNoCasc    = TP_FIR_RANGE_LEN - 1 + kMinDataLoadCycles * m_kStreamLoadVsize
            m_kInitDataNeeded          = m_kInitDataNeededNoCasc + (dataOffsetNthKernel - streamInitNullAccs * TP_DECIMATE_FACTOR * m_kLanes)
            if (m_kInitDataNeeded > m_kSamplesInBuff) :
              return isError(
                f"Kernel[{TP_KP}] requires too much data ({m_kInitDataNeeded} samples) "\
                  f"to fit in a single buffer ({m_kSamplesInBuff} samples), due to the filter length per kernel- "\
                  f"influenced by filter length ({TP_FIR_LEN}), SSR ({TP_SSR}), cascade length ({TP_CASC_LEN}).\n"
              )
    return isValid

def fn_validate_fir_len(TT_DATA, TT_COEF, TP_FIR_LEN, TP_DECIMATE_FACTOR, TP_CASC_LEN, TP_SSR, TP_API, TP_USE_COEF_RELOAD, AIE_VARIANT):
    if TP_FIR_LEN < TP_FIR_LEN_min or TP_FIR_LEN > TP_FIR_LEN_max :
        return isError(f"Minimum and maximum value for Filter length is {TP_FIR_LEN_min} and {TP_FIR_LEN_max}, respectively, but got {TP_FIR_LEN}.")

    minLenCheck =  fn_min_fir_len_each_kernel(TP_FIR_LEN, TP_CASC_LEN, TP_SSR)
    if AIE_VARIANT == 2:
        if (TP_FIR_LEN / TP_CASC_LEN) <  (TP_DECIMATE_FACTOR):
            return isError(
                f"FIR computation is decomposed into multiple (interpolation * decimation factors) parallel polyphases. Make sure that FIR length {TP_FIR_LEN} is greater or equal to TP_DECIMATE_FACTOR {TP_DECIMATE_FACTOR} * TP_CASC_LEN {TP_CASC_LEN}."
            )

    if AIE_VARIANT == 2:
       firLenPerPhaseDivider = TP_DECIMATE_FACTOR
    else:
       firLenPerPhaseDivider = 1
    maxLenCheck = fn_max_fir_len_each_kernel(TT_DATA, TP_FIR_LEN, TP_CASC_LEN, TP_USE_COEF_RELOAD, TP_SSR, TP_API, firLenPerPhaseDivider)

    dataNeededCheck = fn_data_needed_within_buffer_size(TT_DATA, TT_COEF, TP_FIR_LEN / firLenPerPhaseDivider, TP_CASC_LEN,TP_API, TP_SSR, TP_DECIMATE_FACTOR)
    firMultipleCheck = fn_multiple_decimation(TP_FIR_LEN,TP_DECIMATE_FACTOR, TP_CASC_LEN)
    for check in (minLenCheck,maxLenCheck,dataNeededCheck, firMultipleCheck):
      if check["is_valid"] == False :
        return check

    return isValid

# only get a 4b offset value per lane (single hex digit), whereas some buffers are larger than this,
# so we need to catch the situation where decimate factor causes us to require more data in one op than we can index.
def fn_xoffset_range_valid(TT_DATA, TT_COEF, TP_DECIMATE_FACTOR, TP_API):
  m_kLanes = fn_decimate_asym_lanes(TT_DATA, TT_COEF)

  # When checking against xoffset, shouldn't we check m_kLanes*TP_DECIMATE_FACTOR??
  dataNeededBetweenOutputChunks =  (m_kLanes-1)*TP_DECIMATE_FACTOR

  m_kXoffsetRange = 8 if TT_DATA == "cfloat" else 16;
  #m_kFirInitOffset     = m_kFirRangeOffset + m_kFirMarginOffset;
  #m_kDataBuffXOffset   = m_kFirInitOffset % (m_kWinAccessByteSize/sizeof(TT_DATA));  // Remainder of m_kFirInitOffset divided by 128bit
  # CAUTION Fixed AIE1 constant for window read granularity
  m_kWinAccessByteSize = 128//8
  # Complicated to pull in lots of other code here, so we'll just go for worst case.
  m_kDataBuffXOffset = (m_kWinAccessByteSize//fn_size_by_byte(TT_DATA))-1


  buffSize = (1024//8) // fn_size_by_byte(TT_DATA)
  loadSizeBits = 128 if fn_base_type(TT_DATA) == "int32" else 256
  loadVSize = (loadSizeBits // 8) // fn_size_by_byte(TT_DATA)

  dataNeededWithAlignment = dataNeededBetweenOutputChunks + m_kDataBuffXOffset
  # CAUTION, I've tweaked this vs traits because the previous phrasing didn't make sense to me.
  # m_kDataRegVsize-m_kDataLoadVsize >= m_kDFDataRange
  if (dataNeededWithAlignment > (buffSize - loadVSize)):
    return isError(f"Decimate factor exceeded for this data type and coefficient type combination. Required input data ({dataNeededWithAlignment}) exceeds input vector's register ({(buffSize - loadVSize)}).")

  if (TP_API == 1 and dataNeededBetweenOutputChunks > m_kXoffsetRange):
    return isError(f"Decimate factor exceeded for this data type andcoefficient type combination. Required input data ({dataNeededBetweenOutputChunks}) exceeds input vector's register offset address range ({m_kXoffsetRange}).")

  return isValid

# This logic is copied from the kernel class.

def fn_ssr_poly(AIE_VARIANT, TP_DECIMATE_FACTOR, TP_SSR, TP_PARA_DECI_POLY):

  if AIE_VARIANT == 1 :
    # AIE1 allows for SSR on a non-decomposed design, when, e.g. TP_SSR = 2 and TP_PARA_DECI_POLY = 1.
    return isValid

  if AIE_VARIANT == 2 :
    # AIE-ML only allows SSR on a fully-decomposed design, when, e.g. TP_SSR > 1 only when TP_PARA_DECI_POLY = TP_DECIMATE_FACTOR
    if (TP_DECIMATE_FACTOR > TP_PARA_DECI_POLY) and (TP_SSR > 1) :
      return isError(f" Device only allows SSR (TP_SSR > 1) on a fully decomposed design, i.e. when TP_PARA_DECI_POLY R {TP_PARA_DECI_POLY} = TP_DECIMATE_FACTOR {TP_DECIMATE_FACTOR}.")
    return isValid

def fn_validate_decimate_factor(TT_DATA, TT_COEF, TP_DECIMATE_FACTOR, TP_API, AIE_VARIANT):

  if TP_DECIMATE_FACTOR < TP_DECIMATE_FACTOR_min or TP_DECIMATE_FACTOR > TP_DECIMATE_FACTOR_max :
        return isError(f"Minimum and maximum value for Decimation factor is {TP_DECIMATE_FACTOR_min} and {TP_DECIMATE_FACTOR_max}, respectively, but got {TP_DECIMATE_FACTOR}.")
  if AIE_VARIANT == 1 :
    # Check if permute xoffset is within range for the data type in question
    offsetRangeCheck = fn_xoffset_range_valid(TT_DATA, TT_COEF, TP_DECIMATE_FACTOR, TP_API )
    return offsetRangeCheck

  if AIE_VARIANT == 2 :
    vector1kRegisters = 4 # AIE-ML tile contiants 4 independent 1024-bit vector registers that are used for decimation purposes.
    if TP_DECIMATE_FACTOR > vector1kRegisters :
      return isError(f"Decimation Factor {TP_DECIMATE_FACTOR} exceeds AIE tile's vector registers resources {vector1kRegisters}. Consider using decomposition with TP_PARA_DECI_POLY.")
    return isValid

def fn_validate_dual_ip(TP_API, TP_DUAL_IP, AIE_VARIANT):
    if TP_DUAL_IP == 1 and AIE_VARIANT == 2:
      return isError("Dual input ports not supported on this device.")
    if TP_DUAL_IP == 1 and TP_API == 0 and AIE_VARIANT == 1:
      return isError("Dual input ports only supported when port is a stream.")
    return isValid

def fn_validate_num_outputs(TP_API, TP_NUM_OUTPUTS, AIE_VARIANT):
    if TP_NUM_OUTPUTS == 2 and TP_API == 1 and AIE_VARIANT == 2:
      return isError("Dual output stream ports not supported on this device.")
    return isValid

def fn_type_support(TT_DATA, TT_COEF, AIE_VARIANT):
  if TT_DATA == "int16" and TT_COEF == "int16" and AIE_VARIANT == 1:
    return isError(f"The combination of {TT_DATA} and {TT_COEF} is not supported for this class on this device.")
  # AIE-ML, i.e. variant 2 does support int16/int16
  return isValid

def fn_validate_ssr(TP_SSR, TP_API, TP_DECIMATE_FACTOR, TP_PARA_DECI_POLY, AIE_VARIANT):
    # Only supported for streams
  if TP_SSR < TP_SSR_min:
    return isError(f"Minimum value for SSR is {TP_SSR_min}, but got {TP_SSR}.")
  ssrPolyCheck = fn_ssr_poly(AIE_VARIANT, TP_DECIMATE_FACTOR, TP_SSR, TP_PARA_DECI_POLY)
  return ssrPolyCheck

def fn_validate_deci_poly(TP_PARA_DECI_POLY):
    if TP_PARA_DECI_POLY < TP_PARA_DECI_POLY_min :
        return isError(f"Minimum value for Decimation poly phase is {TP_PARA_DECI_POLY_min}, but got {TP_PARA_DECI_POLY}.")
    return isValid

def fn_validate_casc_len(TP_CASC_LEN):
    if TP_CASC_LEN < TP_CASC_LEN_min or TP_CASC_LEN > TP_CASC_LEN_max :
        return isError(f"Minimum and maximum value for cascade length is {TP_CASC_LEN_min} and {TP_CASC_LEN_max}, respectively, but got {TP_CASC_LEN}.")
    return isValid

#### validation APIs ####
def validate_TT_COEF(args):
    TT_DATA = args["TT_DATA"]
    TT_COEF = args["TT_COEF"]
    AIE_VARIANT = args["AIE_VARIANT"]
    standard_checks = fn_validate_coef_type(TT_DATA, TT_COEF)
    typeCheck = fn_type_support(TT_DATA, TT_COEF, AIE_VARIANT)
    for check in (standard_checks,typeCheck):
      if check["is_valid"] == False :
        return check
    return isValid

def validate_TP_SHIFT(args):
  TT_DATA = args["TT_DATA"]
  TP_SHIFT = args["TP_SHIFT"]
  return fn_validate_shift(TT_DATA, TP_SHIFT)

def validate_TP_SAT(args):
  TP_SAT = args["TP_SAT"]
  return fn_validate_satMode(TP_SAT)

def validate_TP_RND(args):
  TP_RND = args["TP_RND"]
  AIE_VARIANT = args["AIE_VARIANT"]
  return fn_validate_roundMode(TP_RND, AIE_VARIANT)

def validate_TP_INPUT_WINDOW_VSIZE(args):
  check_valid_decompose = poly.fn_validate_decomposer_TP_INPUT_WINDOW_VSIZE(args)
  if (check_valid_decompose["is_valid"] == False):
    # error out before continuing to validate
    return check_valid_decompose

  # valid decompose
  #overwrite args with the decomposed version
  args, uut_kernel = poly.get_modified_args_from_polyphase_decomposer(args, current_uut_kernel)
  # if we've decomposed to another type of kernel, then import that kernel and use that validate function
  if uut_kernel != current_uut_kernel:
    other_kernel = importlib.import_module(uut_kernel)
    return other_kernel.validate_TP_INPUT_WINDOW_VSIZE(args)


  # continue using current library element's validator (with potentially modified parameters)
  TP_INPUT_WINDOW_VSIZE = args["TP_INPUT_WINDOW_VSIZE"]
  TT_DATA = args["TT_DATA"]
  TT_COEF = args["TT_COEF"]
  TP_FIR_LEN = args["TP_FIR_LEN"]
  TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
  TP_API = args["TP_API"]
  TP_SSR = args["TP_SSR"]
  return fn_validate_input_window_size(TT_DATA, TT_COEF, TP_FIR_LEN, TP_DECIMATE_FACTOR, TP_INPUT_WINDOW_VSIZE, TP_API, TP_SSR)



def validate_TP_FIR_LEN(args):
  check_valid_decompose = poly.fn_validate_decomposer_TP_FIR_LEN(args)
  if (check_valid_decompose["is_valid"] == False):
    # error out before continuing to validate
    return check_valid_decompose
  # valid decompose
  #overwrite args with the decomposed version
  args, uut_kernel = poly.get_modified_args_from_polyphase_decomposer(args, current_uut_kernel)
  # if we've decomposed to another type of kernel, then import that kernel and use that validate function
  if uut_kernel != current_uut_kernel:
    other_kernel = importlib.import_module(uut_kernel)
    return other_kernel.validate_TP_FIR_LEN(args)

  # continue using current library element's validator (with potentially modified parameters)

  TT_DATA = args["TT_DATA"]
  TT_COEF = args["TT_COEF"]
  TP_FIR_LEN = args["TP_FIR_LEN"]
  TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
  TP_CASC_LEN = args["TP_CASC_LEN"]
  TP_SSR = args["TP_SSR"]
  TP_API = args["TP_API"]
  TP_USE_COEF_RELOAD = args["TP_USE_COEF_RELOAD"]
  AIE_VARIANT = args["AIE_VARIANT"]
  return fn_validate_fir_len(TT_DATA, TT_COEF, TP_FIR_LEN, TP_DECIMATE_FACTOR, TP_CASC_LEN, TP_SSR, TP_API, TP_USE_COEF_RELOAD, AIE_VARIANT)

def validate_TP_DECIMATE_FACTOR(args):
  TT_DATA = args["TT_DATA"]
  TT_COEF = args["TT_COEF"]
  TP_API = args["TP_API"]
  TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
  TP_PARA_DECI_POLY = args["TP_PARA_DECI_POLY"]
  AIE_VARIANT = args["AIE_VARIANT"]

  paraPolyValid = poly.validate_TP_PARA_DECI_POLY(args)


  kernelDecimate = TP_DECIMATE_FACTOR//TP_PARA_DECI_POLY
  decimateValid = (
    fn_validate_decimate_factor(TT_DATA, TT_COEF, kernelDecimate, TP_API, AIE_VARIANT) if kernelDecimate > 1
    else isValid  # no decimate factor to validate
  )

  for check in (paraPolyValid,decimateValid):
    if check["is_valid"] == False :
      return check
  return isValid



def validate_TP_DUAL_IP(args):
    TP_API = args["TP_API"]
    TP_DUAL_IP = args["TP_DUAL_IP"]
    AIE_VARIANT = args["AIE_VARIANT"]
    return fn_validate_dual_ip(TP_API, TP_DUAL_IP, AIE_VARIANT)

def validate_TP_NUM_OUTPUTS(args):
    TP_API = args["TP_API"]
    TP_NUM_OUTPUTS = args["TP_NUM_OUTPUTS"]
    AIE_VARIANT = args["AIE_VARIANT"]
    return fn_validate_num_outputs(TP_API, TP_NUM_OUTPUTS, AIE_VARIANT)

def validate_TP_SSR(args):
    TP_API = args["TP_API"]
    TP_SSR = args["TP_SSR"]
    TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
    TP_PARA_DECI_POLY = args["TP_PARA_DECI_POLY"]
    AIE_VARIANT = args["AIE_VARIANT"]
    return  fn_validate_ssr(TP_SSR, TP_API, TP_DECIMATE_FACTOR, TP_PARA_DECI_POLY, AIE_VARIANT)

def validate_TP_PARA_DECI_POLY(args):
    TP_PARA_DECI_POLY = args["TP_PARA_DECI_POLY"]
    return fn_validate_deci_poly(TP_PARA_DECI_POLY)

def validate_TP_CASC_LEN(args):
    TP_CASC_LEN = args["TP_CASC_LEN"]
    return fn_validate_casc_len(TP_CASC_LEN)

# Example of updater.
#
# Updater are functions to help GUI to hint user on parameter setting with already given parameters.
# The return object will provide "value" which will be set in the wizard as the dependent parameter is being set.
# The rest of keys are similar to paramster definition, but with candidates of enum or range values refined
# based on previously set values.
#
# An updator function always return a dictionary,
# including key "value" for automatically filled default in GUI as dependent parameters have been set, and
# other keys for overriding the definition of parameter.
#
# For example, if a parameter has definition in JSON as
#  { "name": "foo", "type": "typename", "enum": ["int", "float", "double"] }
# And the updator returns
#  { "value": "int", "enum": ["int", "float"] }
# The GUI would show "int" as default and make "int" and "float" selectable candidates, while disabling "double".
#
# If with given combination, no valid value can be set for the parameter being updated, the upater function
# should set "value" to None, to indicate an error and provide error message via "err_message".
# For example
#  { "value": None, "err_message": "With TT_DATA as 'int' there is no valid option for TT_COEF" }
#
# In this example, the following is the updater for TT_COEF, with TT_DATA as the dependent paramster.
# When GUI generates a wizard, TT_DATA should be required first, as it shows up in parameter list first.
# Once user has provided value for TT_DATA, this function will be called and set the value of TT_COEF.
# Meanwhile, the candidate shown in wizard based on enum will also be updated.
#
def update_TT_COEF(TT_DATA):
    return {"value": TT_DATA,
            "enum": [TT_DATA]}

#### port ####


def info_ports(args):
    """Standard function creating a static dictionary of information
    for upper software to correctly connect the IP.
    Some IP has dynamic number of ports according to parameter set,
    so port information has to be implemented as a function"""
    TT_DATA = args["TT_DATA"]
    TT_COEF = args["TT_COEF"]
    TP_INPUT_WINDOW_VSIZE = args["TP_INPUT_WINDOW_VSIZE"]
    TP_FIR_LEN = args["TP_FIR_LEN"]
    TP_SSR = args["TP_SSR"]
    TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
    TP_PARA_DECI_POLY = args["TP_PARA_DECI_POLY"]
    TP_API = args["TP_API"]
    TP_DUAL_IP = args["TP_DUAL_IP"]
    TP_NUM_OUTPUTS = args["TP_NUM_OUTPUTS"]
    TP_INTERPOLATE_FACTOR = 1

    margin_size = sr_asym.fn_margin_size(TP_FIR_LEN, TT_DATA)
    num_in_ports = TP_SSR * TP_PARA_DECI_POLY
    num_out_ports = TP_SSR
    in_win_size = get_input_window_size(TP_INPUT_WINDOW_VSIZE, num_in_ports, TP_API, TP_DUAL_IP)
    out_win_size = get_output_window_size(TP_INPUT_WINDOW_VSIZE, num_out_ports, TP_API, TP_NUM_OUTPUTS, TP_DECIMATE_FACTOR, TP_INTERPOLATE_FACTOR)

    in_ports = get_port_info("in", "in", TT_DATA, in_win_size, num_in_ports, marginSize=margin_size, TP_API=TP_API)
    in2_ports = (get_port_info("in2", "in", TT_DATA, in_win_size, num_in_ports, marginSize=margin_size, TP_API=TP_API) if (TP_DUAL_IP == 1) else [])
    coeff_ports = (get_parameter_port_info("coeff", "in", TT_COEF, TP_SSR, TP_FIR_LEN, "async") if (args["TP_USE_COEF_RELOAD"] == 1) else [])

    # decimate by 2 for halfband
    out_ports = get_port_info("out", "out", TT_DATA, out_win_size, TP_SSR, TP_API=args["TP_API"])
    out2_ports = (get_port_info("out2", "out", TT_DATA, out_win_size, TP_SSR, TP_API=args["TP_API"]) if (args["TP_NUM_OUTPUTS"] == 2) else [])
    return in_ports + in2_ports + coeff_ports + out_ports + out2_ports


#### graph generator ####
# def get_param_list(**kwargs):
#   [f"{value}{comma}} //{key}" for key, value in kwargs.iteritems() for comma in "," ]
def generate_graph(graphname, args):

  if graphname == "":
    graphname = "default_graphname"

  TT_COEF = args["TT_COEF"]
  TT_DATA = args["TT_DATA"]
  TP_FIR_LEN = args["TP_FIR_LEN"]
  TP_DECIMATE_FACTOR = args["TP_DECIMATE_FACTOR"]
  TP_SHIFT = args["TP_SHIFT"]
  TP_RND = args["TP_RND"]
  TP_CASC_LEN = args["TP_CASC_LEN"]
  TP_INPUT_WINDOW_VSIZE = args["TP_INPUT_WINDOW_VSIZE"]
  TP_USE_COEF_RELOAD = args["TP_USE_COEF_RELOAD"]
  TP_NUM_OUTPUTS = args["TP_NUM_OUTPUTS"]
  TP_DUAL_IP = args["TP_DUAL_IP"]
  TP_API = args["TP_API"]
  TP_SSR = args["TP_SSR"]
  TP_PARA_DECI_POLY = args["TP_PARA_DECI_POLY"]
  coeff_list = args["coeff"]
  TP_SAT = args["TP_SAT"]

  taps = sr_asym.fn_get_taps_vector(TT_COEF, coeff_list)
  constr_args_str = f"taps" if TP_USE_COEF_RELOAD == 0 else ""
  dual_ip_declare_str = f"std::array<adf::port<input>, TP_SSR*TP_PARA_DECI_POLY> in2;" if TP_DUAL_IP == 1 else "// No dual input"
  dual_ip_connect_str = f"adf::connect<> net_in2(in2[inPortIdx], filter.in2[inPortIdx]);" if TP_DUAL_IP == 1 else "// No dual input"
  coeff_ip_declare_str = f"ssr_port_array<input> coeff;" if TP_USE_COEF_RELOAD == 1 else "//No coeff port"
  coeff_ip_connect_str = f"adf::connect<> net_coeff(coeff[outPortIdx], filter.coeff[outPortIdx]);" if TP_USE_COEF_RELOAD == 1 else "//No coeff port"
  dual_op_declare_str = f"ssr_port_array<output> out2;" if TP_NUM_OUTPUTS == 2 else "// No dual output"
  dual_op_connect_str = f"adf::connect<> net_out2(filter.out2[outPortIdx], out2[outPortIdx]);" if TP_NUM_OUTPUTS == 2 else "// No dual output"
  # Use formatted multi-line string to avoid a lot of \n and \t
  code  = (
f"""
class {graphname} : public adf::graph {{
public:
  static constexpr unsigned int TP_SSR = {TP_SSR};
  static constexpr unsigned int TP_PARA_DECI_POLY = {TP_PARA_DECI_POLY};
  template <typename dir>
  using ssr_port_array = std::array<adf::port<dir>, TP_SSR>;

  std::array<adf::port<input>, TP_SSR*TP_PARA_DECI_POLY> in;
  {dual_ip_declare_str}
  {coeff_ip_declare_str}
  ssr_port_array<output> out;
  {dual_op_declare_str}

  std::vector<{TT_COEF}> taps = {taps};
  xf::dsp::aie::fir::decimate_asym::fir_decimate_asym_graph<
    {TT_DATA}, //TT_DATA
    {TT_COEF}, //TT_COEF
    {TP_FIR_LEN}, //TP_FIR_LEN
    {TP_DECIMATE_FACTOR}, //TP_DECIMATE_FACTOR
    {TP_SHIFT}, //TP_SHIFT
    {TP_RND}, //TP_RND
    {TP_INPUT_WINDOW_VSIZE}, //TP_INPUT_WINDOW_VSIZE
    {TP_CASC_LEN}, //TP_CASC_LEN
    {TP_USE_COEF_RELOAD}, //TP_USE_COEF_RELOAD
    {TP_NUM_OUTPUTS}, //TP_NUM_OUTPUTS
    {TP_DUAL_IP}, //TP_DUAL_IP
    {TP_API}, //TP_API
    {TP_SSR}, //TP_SSR
    {TP_PARA_DECI_POLY}, //TP_PARA_DECI_POLY
    {TP_SAT} //TP_SAT
  > filter;

  {graphname}() : filter({constr_args_str}) {{
    adf::kernel *filter_kernels = filter.getKernels();
    for (int i=0; i < 1; i++) {{
      adf::runtime<ratio>(filter_kernels[i]) = 0.9;
    }}
    for (int paraPolyIdx=0; paraPolyIdx < TP_PARA_DECI_POLY; paraPolyIdx++) {{
      for (int ssrIdx=0; ssrIdx < TP_SSR; ssrIdx++) {{
        unsigned inPortIdx = paraPolyIdx + ssrIdx*TP_PARA_DECI_POLY;
        adf::connect<> net_in(in[inPortIdx], filter.in[inPortIdx]);
        {dual_ip_connect_str}
      }}
    }}
    for (int ssrIdx=0; ssrIdx < TP_SSR; ssrIdx++) {{
      unsigned outPortIdx = ssrIdx;
      {coeff_ip_connect_str}
      adf::connect<> net_out(filter.out[outPortIdx], out[outPortIdx]);
      {dual_op_connect_str}
    }}
  }}

}};
""")
  out = {}
  out["graph"] = code
  out["port_info"] = info_ports(args)
  out["headerfile"] = "fir_decimate_asym_graph.hpp"
  out["searchpaths"] = [
       "L2/include/aie",
       "L2/tests/aie/common/inc",
       "L1/include/aie",
       "L1/src/aie",
       "L1/tests/aie/inc",
       "L1/tests/aie/src"
  ]

  return out
