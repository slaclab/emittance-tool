import h5py
import numpy as np
from pyemittance.pyscan import PShellFunction, function_value

def get_wire_scanner_readable(wire_scanner, blms, scan_type, n_points, n_backgrounds=10, bunch_number=1):

    # The last two values are zero because we are using one wire (scan_type).
    scan_range = []
    # In um/s
    bpms = []
    n_cycles = 1

    # This two parameter has to always be the same for the wire scan.
    plt = None
    save_raw = False
    adaptive = False # something with range
    beamOKflag = True # set to True for real measurements, can be set to False for tests

    script_name = "Diagnostics/WireScan.py"
    parameters = [
            wire_scanner,
            scan_type,
            scan_range,
            n_cycles,
            n_points,
            bpms,
            blms,
            n_backgrounds,
            plt,
            save_raw,
            bunch_number,
            adaptive,
            beamOKflag,
            ]
    pshell = PShellFunction(script_name=script_name, parameters=parameters)

    readables = function_value(pshell.read)
    return readables

def read_h5(entry):
    h5_file1, rest = entry.split('.h5')
    h5_file1 += '.h5'
    rest = rest[1:] # remove leading slash

    with h5py.File(h5_file1, 'r') as f:
        output = np.array(f[rest])
    return output


if __name__ == '__main__':
    wire_scanner = "S30CB09-DWSC440"
    blms = ["S10DI01-DBLM045"]
    scan_type = 'X1'
    n_points = 200

    wire_scan_readable = get_wire_scanner_readable(wire_scanner, blms, scan_type, n_points)

    # Result format: [[[cycles]], ...]
    # Example: [[[10.0, 20.0, 50.0, 60.0, '...h5|x_0001/w_pos', '...h5|x_0001/blm1']]]
    #result = scan(positioner=positioner, readables=readables)


