import pytest
from pyemittance import beamdynamics
import json

def test_example(num_regression, data_regression, example_data):
    """Executes analyzePyscanRsults and generates metadata. All function arguments are fixtures.
    The float/array results had to be broken apart due to the regression tests and data types.

    """
    meta_data = beamdynamics.analyzePyscanResult(example_data)
    print(meta_data)

    float_data = {
        "sfbd_epics_data.EMITTANCE-X": meta_data["sfbd_epics_data"]["EMITTANCE-X"],
        "sfbd_epics_data.MISMATCH-X": meta_data["sfbd_epics_data"]["MISMATCH-X"],
        "sfbd_epics_data.ALPHA-X": meta_data["sfbd_epics_data"]["ALPHA-X"],
        "sfbd_epics_data.BETA-X": meta_data["sfbd_epics_data"]["BETA-X"],
        "sfbd_epics_data.EMITTANCE-Y": meta_data["sfbd_epics_data"]["EMITTANCE-Y"],
        "sfbd_epics_data.MISMATCH-Y": meta_data["sfbd_epics_data"]["MISMATCH-Y"],
        "sfbd_epics_data.BETA-Y": meta_data["sfbd_epics_data"]["BETA-Y"],
        "sfbd_epics_data.ALPHA-Y": meta_data["sfbd_epics_data"]["ALPHA-Y"],
        "proj_emittance_X.emittance": meta_data["proj_emittance_X"]["emittance"],
        "proj_emittance_X.normalized_emittance" : meta_data["proj_emittance_X"]["normalized_emittance"],
        "proj_emittance_X.mismatch": meta_data["proj_emittance_X"]["mismatch"],
        "proj_emittance_X.beta": meta_data["proj_emittance_X"]["beta"],
        "proj_emittance_X.alpha": meta_data["proj_emittance_X"]["alpha"],
        "proj_emittance_X.gamma": meta_data["proj_emittance_X"]["gamma"],
        "proj_emittance_X.beta0": meta_data["proj_emittance_X"]["beta0"],
        "proj_emittance_X.alpha0": meta_data["proj_emittance_X"]["alpha0"],
        "proj_emittance_X.gamma0": meta_data["proj_emittance_X"]["gamma0"],
        "proj_emittance_Y.emittance": meta_data["proj_emittance_Y"]["emittance"],
        "proj_emittance_Y.normalized_emittance" : meta_data["proj_emittance_Y"]["normalized_emittance"],
        "proj_emittance_Y.mismatch": meta_data["proj_emittance_Y"]["mismatch"],
        "proj_emittance_Y.beta": meta_data["proj_emittance_Y"]["beta"],
        "proj_emittance_Y.alpha": meta_data["proj_emittance_Y"]["alpha"],
        "proj_emittance_Y.gamma": meta_data["proj_emittance_Y"]["gamma"],
        "proj_emittance_Y.beta0": meta_data["proj_emittance_Y"]["beta0"],
        "proj_emittance_Y.alpha0": meta_data["proj_emittance_Y"]["alpha0"],
        "proj_emittance_Y.gamma0": meta_data["proj_emittance_Y"]["gamma0"],
    }
    
    numpy_data = {
        "proj_emittance_X.normalized_emittance_err": meta_data["proj_emittance_X"]["normalized_emittance_err"],
        "proj_emittance_X.emittance_err": meta_data["proj_emittance_X"]["emittance_err"],
        "proj_emittance_X.reconstruction": meta_data["proj_emittance_X"]["reconstruction"],
        "proj_emittance_X.popt": meta_data["proj_emittance_X"]["popt"],
        "proj_emittance_X.pcov": meta_data["proj_emittance_X"]["pcov"],
        "proj_emittance_X.beamsizes": meta_data["proj_emittance_X"]["beamsizes"],
        "proj_emittance_X.beamsizes_err": meta_data["proj_emittance_X"]["beamsizes_err"],
        "proj_emittance_X.design": meta_data["proj_emittance_X"]["design"],
        "proj_emittance_X.R11": meta_data["proj_emittance_X"]["R11"],
        "proj_emittance_X.R12": meta_data["proj_emittance_X"]["R12"],
        "proj_emittance_X.phase_meas": meta_data["proj_emittance_X"]["phase_meas"],
        "proj_emittance_X.phase_design": meta_data["proj_emittance_X"]["phase_design"],
        "proj_emittance_Y.normalized_emittance_err": meta_data["proj_emittance_Y"]["normalized_emittance_err"],
        "proj_emittance_Y.emittance_err": meta_data["proj_emittance_Y"]["emittance_err"],
        "proj_emittance_Y.reconstruction": meta_data["proj_emittance_Y"]["reconstruction"],
        "proj_emittance_Y.popt": meta_data["proj_emittance_Y"]["popt"],
        "proj_emittance_Y.pcov": meta_data["proj_emittance_Y"]["pcov"],
        "proj_emittance_Y.beamsizes": meta_data["proj_emittance_Y"]["beamsizes"],
        "proj_emittance_Y.beamsizes_err": meta_data["proj_emittance_Y"]["beamsizes_err"],
        "proj_emittance_Y.design": meta_data["proj_emittance_Y"]["design"],
        "proj_emittance_Y.R11": meta_data["proj_emittance_Y"]["R11"],
        "proj_emittance_Y.R12": meta_data["proj_emittance_Y"]["R12"],
        "proj_emittance_Y.phase_meas": meta_data["proj_emittance_Y"]["phase_meas"],
        "proj_emittance_Y.phase_design": meta_data["proj_emittance_Y"]["phase_design"],

    }

    # only accepts 1d arrays 
    numpy_data = {item: numpy_data[item].flatten() for item in numpy_data}

    # known issue with np.float64 types
    float_data = {item: float('{:g}'.format(float('{:.6g}'.format(float_data[item])))) for item in float_data}

    num_regression.check(numpy_data)
    data_regression.check(float_data)