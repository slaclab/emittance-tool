import logging
import numpy as np

from OMEpicsChannel import EpicsChannel
from pyemittance.myEnergyManager import EnergyManager
from OMType import FacilityContainer
from OMSwissFELmagnet import SwissFELmagnet
from pyemittance.OMLayoutNov2020 import SwissFEL

import pyemittance.pyscan
import pyemittance.pyscan.interface.pyScan as PyScan

from epics import caget

from cam_server import PipelineClient
from cam_server.utils import get_host_port_from_stream_address

import pyemittance.EmittanceToolConfig
import pyemittance.beamdynamics

PreDefinedGroups = [
        'Bend:I-SET',
        'Bend:PS-MODE',
        'Quad:I-SET',
        'Quad:PS-MODE',
        'PQuad:KL',
        'PQuadMotor:X',
        'RFsystem:GET-RF-READY-STATUS',
        'RFsystem:GET-STATION-MODE',
        'RFsystem:GET-STATION-STATE',
        'RFsystem:SET-ACC-VOLT',
        'RFsystem:SET-VSUM-PHASE',
        'RFsystem:SET-BEAM-PHASE',
        ]

Layout = SwissFEL(alt=0) # 0 for current state
EM = EnergyManager()
SF = FacilityContainer(Layout, 1)  # 1 is with bending on, 2 with bendings off!
print('SF.writeFacility(EM)')
SF.writeFacility(EM)

# initiate connection to EPICS system
EC = EpicsChannel()
EC.cafe.setOpenDefaultPendTime(2.0)
EC.switchOutput()
print('SF.writeFacility(EC, 1)')
SF.writeFacility(EC, 1)
EC.createHandle(PreDefinedGroups)

SM = SwissFELmagnet()
print('SF.writeFacility(SM)')
SF.writeFacility(SM)

def perform_meas_wire_scanner():
    pass


def perform_meas_screen(location, measurement_type, ProfName, energy_eV, k_steps, n_images, QuadNames, instance_config_update, measurement_device, dimension='X', dry_run=False):


    print('Perform Meas was called')

    n_images = int(n_images)
    assert n_images >= 1
    number_of_slices = instance_config_update['image_slices']['number_of_slices']
    beamdynamics_obj = beamdynamics.SFEmittanceMeasurementAnalyzer(location, measurement_type, dimension, energy_eV, k_steps)
    QuadK = beamdynamics_obj.QuadK
    energy_MeV = energy_eV/1e6

    # To be saved together with the raw data
    Input = {
            'Measurement location': location,
            'Measurement type': measurement_type,
            'QuadK': QuadK,
            'Profile monitor': ProfName,
            'energy_MeV': energy_MeV,
            'energy_eV': energy_eV,
            'Phase advance step':k_steps,
            'Number of images': n_images,
            'Quadrupole names': np.array(QuadNames),
            'instance_config_update': instance_config_update,
            'Dimension': dimension,
            'Dry run': dry_run,
            'Measurement device': measurement_device,
            'Number of slices': number_of_slices,
            'R11': beamdynamics_obj.R11,
            'R12': beamdynamics_obj.R12,
            'R33': beamdynamics_obj.R33,
            'R34': beamdynamics_obj.R34,
            }


    n_results = QuadK.shape[1]
    use_slices = measurement_type in EmittanceToolConfig.slice_measurement_types

    QuadI = []
    for i in range(0, len(QuadNames)):
        if np.all(QuadK[i] == 0):
            # Temporary fix for quadrupoles that are not in Masamitsus Onlinemodel...
            QuadI.append([0]*len(QuadK[i]))
        else:
            quadkl = SM.QuadrupoleK2KL([QuadNames[i]] * len(QuadK[0]), QuadK[i], 'P')
            QuadI.append(SM.QuadrupoleKL2I([QuadNames[i]] * len(QuadK[0]), quadkl, energy_MeV))

    # get beam sizes for different optics
    QuadIch = []
    for i in range(0, len(QuadNames)):
        QuadIch.append(QuadNames[i].replace('.', '-') + ':I-SET')

    EC.addGroup('QuadI', QuadIch)
    QuadI = np.array(QuadI)

    if dry_run:
        Screen = 'simulation'
    else:
        Screen = ProfName.replace('.', '-')

    writables = []
    for pv_name in QuadIch:
        readback_pv_name = pv_name
        readback_pv_name = readback_pv_name.replace('SET', 'READ')

        writables.append(pyscan.epics_pv(pv_name=pv_name,
                                  readback_pv_name=readback_pv_name,
                                  tolerance=0.01))

    positions = PyScan.convert_to_position_list(pyscan.convert_to_list(QuadI.tolist()))
    positioner = pyscan.VectorPositioner(positions)

    readables = string_readables = [
            'bs://gr_x_fit_standard_deviation',
            'bs://gr_y_fit_standard_deviation',
            'bs://gr_x_fit_mean',
            'bs://gr_y_fit_mean',
            'bs://gr_x_axis',
            'bs://gr_y_axis',
            'bs://gr_x_fit_gauss_function',
            'bs://gr_y_fit_gauss_function',
            'bs://image',
            'bs://x_axis',
            'bs://y_axis',
            ]

    if use_slices:
        readables.extend([
            'bs://coupling',
            'bs://coupling_slope',
            'bs://coupling_offset',])

    if use_slices:
        for slice_number in range(number_of_slices):
            readables.extend([
                'bs://slice_%d_standard_deviation' % slice_number,
                'bs://slice_%d_intensity' % slice_number,
                'bs://slice_%d_center_y' % slice_number,
                'bs://slice_%d_center_x' % slice_number,
                ])

    measurement_interval = 0.4 # this is in principle irrelevant (remove it and check it with beam when you have time)
    settling_time = 2 # this is in principle in ms

    settings = pyscan.scan_settings(settling_time=settling_time,
                             measurement_interval=measurement_interval,
                             n_measurements=int(n_images))
    pyscan.config.bs_read_timeout = 15
    initialization, finalization = None, None

    after_read = None

    pipeline_client = PipelineClient("http://sf-daqsync-01:8889/")
    cam_instance_name = str(Screen) + "_sp1"
    stream_address = pipeline_client.get_instance_stream(cam_instance_name)
    stream_host, stream_port = get_host_port_from_stream_address(stream_address)

    # Configure bsread
    pyscan.config.bs_default_host = stream_host
    pyscan.config.bs_default_port = stream_port

    logging.getLogger("mflow.mflow").setLevel(logging.ERROR)

    # Enable slices for camera
    if use_slices:
        instance_config = pipeline_client.get_instance_config(cam_instance_name)
        original_cam_instance_config = dict(instance_config)
        instance_config["image_background_subtraction"] = True  # enabling background subtraction, but not grabbing it, this option will be add later
        instance_config.update(instance_config_update)
        if dimension == 'X':
            instance_config["image_slices"]['orientation'] = 'vertical'
            instance_config['slice_orientation'] = 'vertical'
        elif dimension == 'Y':
            print('Orientation horizontal')
            instance_config["image_slices"]['orientation'] = 'horizontal'
            instance_config['slice_orientation'] = 'horizontal'

        pipeline_client.set_instance_config(cam_instance_name, instance_config)
    else:
        instance_config = pipeline_client.get_instance_config(cam_instance_name)
        original_cam_instance_config = dict(instance_config)
        instance_config["image_background_subtraction"] = True  # enabling background subtraction, but not grabbing it, this option will be add later
        pipeline_client.set_instance_config(cam_instance_name, instance_config)

    if dry_run:
        result = np.random.random([n_results, n_images, len(string_readables)])
    else:
        print('Starting pyscan')
        raw_result = result = pyscan.scan(positioner=positioner, writables=writables, readables=readables, settings=settings, finalization=finalization, after_read=after_read, initialization=initialization)
        print('pyscan done')

        # Always make result a list of level 3
        if n_images == 1:
            result = [[x] for x in raw_result]

    result_dict = pyscan_result_to_dict(string_readables, result, scrap_bs=True)
    print('result dict generated')
    # ERROR after this

    if dry_run:
        ny, nx = 200, 100
        result_dict['image'] = np.random.random([n_results, n_images, ny, nx])*1e3
        result_dict['x_axis'] = np.ones([n_results, n_images, nx])*np.arange(nx)
        result_dict['y_axis'] = np.ones([n_results, n_images, ny])*np.arange(ny)

    # Apply original config - i.e. remove slices and disable good region
    print('Before Pipeline client set')
    pipeline_client.set_instance_config(cam_instance_name, original_cam_instance_config)
    print('Pipeline client set')

    # 14/06/2019
    # I suspect the following lines sometimes caused a freeze of the emittance tool and the necessity to abort the program while losing all the results

    ## What does this do?
    #for group in EC.cafe.groupList():
    #    if group not in PreDefinedGroups:
    #        EC.cafe.groupClose(group)
    ##ERROR before this
    #print('EC groups closed')

    magnet_data = {}
    magnet_data['Magnets'] = np.array(QuadNames)
    magnet_data['K'] = QuadK
    magnet_data['I-SET'] = np.array(QuadI)

    other_pvs, other_values, laser_data = get_other_data()
    magnet_data['Other'] = np.array(other_pvs)
    magnet_data['Other_values'] = other_values

    output = {
            'Magnet_data': magnet_data,
            'Raw_data': result_dict,
            'Laser_data': laser_data,
            'Input': Input,
            }

    return output

def get_other_data():
    other_pvs = []
    for subdict in EmittanceToolConfig.tdc_dict.values():
        other_pvs.append(subdict['pv'])
        other_pvs.append(subdict['pv_phase'])
        other_pvs.append(subdict['pv_status'])

    laser_data = {}
    for name, pv in EmittanceToolConfig.laser_status.items():
        laser_data[name] = caget(pv, as_string=True)

    for subdict in EmittanceToolConfig.tilt_sext_quad_dict.values():
        for mag_list in subdict.values():
            for name in mag_list:
                if name != 'None':
                    pv = name.replace('.', '-')+':I-READ'
                    other_pvs.append(pv)
    other_values = [caget(pv) for pv in other_pvs]
    return other_pvs, other_values, laser_data

def pyscan_result_to_dict(readables, result, scrap_bs=False):
    """
    Excpects a nested list of order 3.
    Level 1 is the scan index.
    Level 2 is the number of images per scan index (unless this number is 1 in which case this level does not exist).
    Level 3 is the number of readables.

    Returns a shuffled version that takes the form of the dictionary, with the readables as keys.
    """

    output = {}

    for nR, readable in enumerate(readables):
        readable_output1 = []
        for level_scan in result:
            readable_output2 = []
            for level_image in level_scan:
                readable_output2.append(level_image[nR])
            readable_output1.append(readable_output2)

        if scrap_bs and hasattr(readable, 'startswith') and readable.startswith('bs://'):
            readable2 = readable[5:]
        else:
            readable2 = readable

        try:
            output[readable2] = np.array(readable_output1)
        except:
            output[readable2] = readable_output1

    return output

