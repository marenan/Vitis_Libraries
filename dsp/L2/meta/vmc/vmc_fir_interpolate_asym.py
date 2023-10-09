from fir_interpolate_asym import *
from aie_common import *
from vmc_fir_utils import *

#### VMC validators ####
def vmc_validate_coef_type(args):
	data_type = args["data_type"]
	coef_type = args["coef_type"]
	standard_checks =  fn_validate_coef_type(data_type, coef_type)
	AIE_VARIANT = args["AIE_VARIANT"]
	type_check = fn_type_support(data_type, coef_type,AIE_VARIANT)
	for check in (standard_checks,type_check) :
		if check["is_valid"] == False :
			return check
	return {"is_valid": True}
	

def vmc_validate_input_window_size(args):
	input_window_size = args["input_window_size"]
	data_type = args["data_type"]
	use_coeff_reload = args["use_coeff_reload"]
	coef_type = args["coef_type"]
	coeff = args["coeff"]
	interpolate_factor = args["interpolate_factor"]
	api = 0
	ssr = 1
	fir_length = fn_get_fir_length(args)
	return fn_validate_input_window_size(data_type, coef_type, fir_length, interpolate_factor, input_window_size, api, ssr)

def vmc_validate_casc_length(args):
    casc_length = args["casc_length"]
    return fn_validate_casc_len(casc_length);
    
def validate_sat_mode(args):
    sat_mode = args["sat_mode"]
    return fn_validate_satMode(sat_mode);

def vmc_validate_coeff(args):
	use_coeff_reload = args["use_coeff_reload"]
	coef_type = args["coef_type"]
	coeff = args["coeff"]
	data_type = args["data_type"]
	casc_length = args["casc_length"]
	interpolate_factor = args["interpolate_factor"]
	ssr = 1
	api = 0
	dual_ip = 0
	fir_length = fn_get_fir_length(args)
	return fn_validate_fir_len(data_type, coef_type, fir_length, interpolate_factor, casc_length, ssr, api, use_coeff_reload, dual_ip )

def vmc_validate_shift_val(args):
	data_type = args["data_type"]
	shift_val = args["shift_val"]
	return fn_validate_shift(data_type, shift_val)

def vmc_validate_interp_poly(args):
        interp_poly = args["interp_poly"]
        interpolate_factor = args["interpolate_factor"]	
        return fn_validate_para_interp_poly(interpolate_factor, interp_poly)
    
def vmc_validate_ssr(args):
    interpolate_factor = args["interpolate_factor"]
    ssr = 1
    api = 0
    return fn_validate_ssr(ssr, interpolate_factor,api)

def vmc_validate_interpolate_factor(args):
	interpolate_factor = args["interpolate_factor"]
	return fn_validate_interpolate_factor(interpolate_factor)

def vmc_validate_out_ports(args):
	num_outputs = fn_get_num_outputs(args)
	AIE_VARIANT = args["AIE_VARIANT"]
	api = 0
	return fn_validate_num_outputs(api, num_outputs, AIE_VARIANT)

#### VMC graph generator ####
def vmc_generate_graph(name, args):
	tmpargs = {}
	tmpargs["TT_DATA"] = args["data_type"]
	use_coeff_reload = args["use_coeff_reload"]
	coef_type = args["coef_type"]
	coeff = args["coeff"]
	tmpargs["TT_COEF"] = coef_type
	tmpargs["TP_FIR_LEN"] = fn_get_fir_length(args)
	tmpargs["TP_SHIFT"] = args["shift_val"]
	tmpargs["TP_RND"] = args["rnd_mode"]
	tmpargs["TP_INPUT_WINDOW_VSIZE"] = args["input_window_size"]
	tmpargs["TP_INTERPOLATE_FACTOR"] = args["interpolate_factor"]
	tmpargs["TP_CASC_LEN"] = args["casc_length"]
	tmpargs["TP_USE_COEF_RELOAD"] = 1 if args["use_coeff_reload"] else 0
	tmpargs["TP_NUM_OUTPUTS"] = fn_get_num_outputs(args)
	tmpargs["TP_DUAL_IP"] = 0
	tmpargs["TP_API"] = 0
	tmpargs["TP_SSR"] = 1
	tmpargs["coeff"] = args["coeff"]
	tmpargs["TP_SAT"] = args["sat_mode"]
	tmpargs["TP_PARA_INTERP_POLY"] = args["interp_poly"]	   
	return generate_graph(name, tmpargs)
