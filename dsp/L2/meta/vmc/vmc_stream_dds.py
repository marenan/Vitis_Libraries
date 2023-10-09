from dds_mixer import *

#### VMC validators ####


def vmc_validate_output_window_size(args):
    tempargs = {}
    tempargs["TP_INPUT_WINDOW_VSIZE"] = args["output_window_size"]
    tempargs["TT_DATA"] = args["data_type"]
    return validate_TP_WINDOW_VSIZE(tempargs)

def vmc_validate_ssr(args):
    ssr = args["ssr"]
    return fn_validate_ssr(ssr);

#### VMC graph generator ####
def vmc_generate_graph(name, args):
    tmpargs = {}
    tmpargs["TT_DATA"] = args["data_type"]
    tmpargs["TP_MIXER_MODE"] = 0
    tmpargs["TP_INPUT_WINDOW_VSIZE"] = args["output_window_size"]
    tmpargs["TP_NUM_OUTPUTS"] = 1
    tmpargs["TP_SSR"] = args["ssr"]
    tmpargs["TP_API"] = 1
    tmpargs["phaseInc"] = args["phase_increment"]
    tmpargs["initialPhaseOffset"] = 0
    tmpargs["TP_RND"] = args["rnd_mode"]
    tmpargs["TP_SAT"] = args["sat_mode"]
    return generate_graph(name, tmpargs)