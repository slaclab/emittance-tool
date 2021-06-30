"""
No specific imports, so that you can use this file on any machine.
"""
from copy import deepcopy
from collections import OrderedDict
import numpy as np

# For the GUI only
available_measurementTypes = OrderedDict([
        ('Laser Heater', ['Und. on, Projected (single-quad)', 'Und. off, Projected (multi-quad)', 'Und. off, Projected (single-quad)', 'Espread REF', 'Espread TIGHT', 'Espread LOOSE',]),
        ('BC1', ['Projected (single-quad)', 'Slice (multi-quad)', 'Espread',]),
        ('BC2', ['Projected (single-quad)',]),
        ('Switchyard', ['Projected (single-quad)',]),
        ('Linac 3 End', ['Projected (single-quad)', 'Slice (multi-quad)',]),
        ('Undulator Entrance', ['Projected (single-quad)',]),
        ('Aramis post-undulator', ['Projected (single-quad)', 'Slice (multi-quad)']),
        ('Athos', ['Projected (single-quad)',]),
        ('Athos post-undulator', ['Projected (single-quad)',]),
        ])

single_quad_measurement_types = (
        'Und. on, Projected (single-quad)',
        'Und. off, Projected (single-quad)',
        'Und. on, Projected (single-quad)',
        'Espread REF',
        'Espread TIGHT',
        'Espread LOOSE',
        'Projected (single-quad)',
        'Espread',
        'Slice (single-quad)',
        )

multi_quad_measurement_types = (
        'Slice (multi-quad)',
        'Und. off, Projected (multi-quad)',
        )

slice_measurement_types = (
        'Slice (multi-quad)',
        'Slice (single-quad)',
        )

# defining some variables depending on the measurement location and location
MatchingQuads = {
        'BC1': [
            'SINBC01.MQUA020',
            'SINBC01.MQUA050',
            'SINBC01.MQUA070',
            'SINBC01.MQUA090',
            'SINBC01.MQUA110'],
        'BC2': [
            'S10CB07.MQUA230',
            'S10CB07.MQUA430',
            'S10CB08.MQUA230',
            'S10CB08.MQUA430',
            'S10CB09.MQUA230'],
        'Laser Heater': [
            'SINLH01.MQUA020',
            'SINLH01.MQUA040',
            'SINLH01.MQUA050',
            'SINLH01.MQUA070',
            'SINLH02.MQUA010'],
        'Switchyard': [
            'S20SY01.MQUA020',
            'S20SY01.MQUA030',
            'S20SY01.MQUA050',
            'S20SY01.MQUA080'],
        'Linac 3 End': [
            'S30CB05.MQUA430',
            'S30CB06.MQUA430',
            'S30CB07.MQUA430',
            'S30CB08.MQUA430',
            'S30CB09.MQUA430'],
        'Undulator Entrance': [
            'SARCL01.MQUA020',
            'SARCL01.MQUA050',
            'SARCL01.MQUA080',
            'SARCL01.MQUA100',
            'SARCL01.MQUA140'],
        'Aramis post-undulator': [
            'SARMA01.MQUA120',
            'SARMA01.MQUA140',
            'SARMA02.MQUA050',
            'SARMA02.MQUA120',
            'SARUN01.MQUA080'],
        'Athos': [
            'SATDI01.MQUA040',
            'SATDI01.MQUA050',
            'SATDI01.MQUA220',
            'SATDI01.MQUA230',
            ],
        'Athos post-undulator': [
            'SATMA01.MQUA120',
            'SATMA01.MQUA140',
            'SATMA01.MQUA160',
            'SATMA01.MQUA180',
            'SATMA01.MQUA200',
            ],
        }

# profile monitors (depending on location)
PM = {
        'Laser Heater':'SINSB03.DSCR110',
        'BC1':'S10DI01.DSCR020',
        'BC1_Yslice': 'S10BD01.DSCR030',
        'BC2':'S10MA01.DSCR090',
        'Switchyard': 'S20SY03.DWSC090',
        'Linac 3 End':'SARCL01.DSCR170',
        'Linac 3 End_Yslice': 'SARCL02.DSCR280',
        'Undulator Entrance':'SARMA02.DSCR030',
        'Aramis post-undulator':'SARBD01.DSCR050',
        'Aramis post-undulator_Xslice':'SARBD02.DSCR050',
        'Athos': 'SATMA01.DSCR030',
        'Athos post-undulator': 'SATBD01.DSCR120',
        }

defaultKValues = {
        # For each location, list the measurement quads and their values
        # to get the measurement optics. Use 'None' if it is a symmetric single
        # scan quadrupole.
        'BC1/Slice (single-quad)':[ # Checked
            ('SINDI02.MQUA020', -3.397599593691512e+00),
            ('SINDI02.MQUA030', 3.962446197133111e+00),
            ('SINDI02.MQUA050', 8.338179838181716e+00),
            ('SINDI02.MQUA060', -1.823600754421064e+00),
            ('SINDI02.MQUA090', 5.116221274396137e+00),
            ('S10CB01.MQUA230', -2.032863649011738e+00),
            ('S10CB01.MQUA430', 8.494183666677313e-01),
            ('S10CB02.MQUA230', None),
            ('S10CB02.MQUA430', 0),
            ],
        'BC1/Projected (single-quad)': [ # Checked
            ('SINDI02.MQUA020', -4.254397955064375e-03),
            ('SINDI02.MQUA030', -1.610159973104216e+00),
            ('SINDI02.MQUA050', 1.336802835486416e+00),
            ('SINDI02.MQUA060', 1.321356783612842e+00),
            ('SINDI02.MQUA090', -7.651426248280822e-01),
            ('S10CB01.MQUA230', None), # Varied quadrupole, Reconstruction Point
            ('S10CB01.MQUA430', 0),
            ('S10CB02.MQUA230', 0),
            ('S10CB02.MQUA430', 0),
            ],
        'BC1/Slice (multi-quad)': [
            ('SINDI02.MQUA020', '__file__'), # Must be provided by given file
            ('SINDI02.MQUA030', 0.),
            ('SINDI02.MQUA050', '__file__'),
            ('SINDI02.MQUA060', 0.),
            ('SINDI02.MQUA090', '__file__'),
            ('S10CB01.MQUA230', '__file__'),
            ('S10CB01.MQUA430', '__file__'),
            ('S10CB02.MQUA230', 0.),
            ('S10CB02.MQUA430', 0.),
            ('S10DI01.MQUA030', 0.),
            ('S10BD01.MQUA010', 0.),
            ],
        'BC1/Espread': [
            ('SINDI02.MQUA020', -3.554598021886218e-02),
            ('SINDI02.MQUA030', -1.468128341020001e+00),
            ('SINDI02.MQUA050', 1.323376958976800e+00),
            ('SINDI02.MQUA060', 2.604712843981193e-01),
            ('SINDI02.MQUA090', 9.715215470856654e-02),
            ('S10CB01.MQUA230', None),
            ('S10CB01.MQUA430', 0),
            ('S10CB02.MQUA230', 0),
            ('S10CB02.MQUA430', 0),
            ],
        'BC2/Projected (single-quad)': [ # Checked
            ('S10BC01.MQUA020', 4.650087597813672e-01),
            ('S10BC01.MQUA040', 6.826758713573640e-01),
            ('S10BC01.MQUA060', -2.151865803606123e+00),
            ('S10BC01.MQUA080', 1.854537453467318e+00),
            ('S10BC01.MQUA100', None),
            ('S10BC02.MQSK110', 0),
            ('S10BC02.MQUA120', 0),
            ('S10BC02.MQUA340', 0),
            ('S10BC02.MQSK350', 0),
            ('S10MA01.MQUA020', 0),
            ('S10MA01.MQUA050', 0),
            ('S10MA01.MQUA070', 0),
            ],
        'Laser Heater/Und. off, Projected (single-quad)': [ # Checked
            ('SINLH02.MQUA410', -1.630745965750396e+00),
            ('SINLH03.MQUA030', 6.126219357674612e+00),
            ('SINLH03.MQUA040', -5.656074368043188e+00),
            ('SINLH03.MQUA060', -1.837720293049522e+00),
            ('SINLH03.MQUA080', None),
            ],
        'Laser Heater/Und. on, Projected (single-quad)': [ # Checked
            ('SINLH02.MQUA410', -3.828551699828213e+00),
            ('SINLH03.MQUA030', 7.489602091276538e+00),
            ('SINLH03.MQUA040', -1.030443755940245e+01),
            ('SINLH03.MQUA060', 1.981341727854083e+00),
            ('SINLH03.MQUA080', None),
            ],
        'Laser Heater/Espread REF': [ # Checked
            ('SINLH02.MQUA410', 7.191029497211183e+00),
            ('SINLH03.MQUA030', -1.098271670713132e+01),
            ('SINLH03.MQUA040', 8.044914432905490e+00),
            ('SINLH03.MQUA060', 4.795806485869887e+00),
            ('SINLH03.MQUA080', None),
            ],
        'Laser Heater/Espread TIGHT': [ # Checked
            ('SINLH02.MQUA410', -7.681894223307398e+00),
            ('SINLH03.MQUA030', 9.671267511161043e+00),
            ('SINLH03.MQUA040', -6.492588534601179e+00),
            ('SINLH03.MQUA060', -2.678887613043235e+00),
            ('SINLH03.MQUA080', None),
            ],
        'Laser Heater/Espread LOOSE': [ # Checked
            ('SINLH02.MQUA410', 6.647659642789005e+00),
            ('SINLH03.MQUA030', -1.159864743393859e+01),
            ('SINLH03.MQUA040', 1.097363390364061e+01),
            ('SINLH03.MQUA060', 7.077201972061928e+00),
            ('SINLH03.MQUA080', None),
            ],
        'Laser Heater/Und. off, Projected (multi-quad)': [
            ('SINLH02.MQUA410', '__file__'),
            ('SINLH03.MQUA030', '__file__'),
            ('SINLH03.MQUA040', '__file__'),
            ('SINLH03.MQUA060', '__file__'),
            ('SINLH03.MQUA080', '__file__'),
            ],
        'Switchyard/Projected (single-quad)': [
            ('S20SY02.MQUA070', 2.056181406414312e+00),
            ('S20SY02.MQUA100', -4.924356338386481e-01),
            ('S20SY02.MQUA140', -2.464516792286989e+00),
            ('S20SY02.MQUA180', 2.719983879841830e+00),
            ('S20SY03.MQUA020', -5.951965513937167e-01),
            ],
        'Linac 3 End/Projected (single-quad)': [ # Checked
            ('S30CB10.MQUA430', -1.756841008552548e-02),
            ('S30CB11.MQUA430', 1.150999828973631e-01),
            ('S30CB12.MQUA430', -6.185805837037691e-01),
            ('S30CB13.MQUA430', 7.510541253799776e-01),
            ('S30CB14.MQUA430', -3.269817027099327e-01),
            ('S30CB15.MQUA430', None),
            ('SARCL01.MQUA020', 0),
            ('SARCL01.MQUA050', 0),
            ('SARCL01.MQUA080', 0),
            ('SARCL01.MQUA100', 0),
            ('SARCL01.MQUA140', 0),
            ],
        'Linac 3 End/Slice (multi-quad)': [
            ('S30CB10.MQUA430', -6.292892126189119e-01),
            ('S30CB11.MQUA430', -9.532824154387667e-02),
            ('S30CB12.MQUA430', 7.494309958138627e-01),
            ('S30CB13.MQUA430', -4.253590905352572e-01),
            ('S30CB14.MQUA430', '__file__'),
            ('S30CB15.MQUA430', '__file__'),
            ('SARCL01.MQUA020', '__file__'),
            ('SARCL01.MQUA050', '__file__'),
            ('SARCL01.MQUA080', '__file__'),
            ('SARCL01.MQUA100', '__file__'),
            ('SARCL01.MQUA140', 0.),
            ('SARCL01.MQUA190', 0.),
            ('SARCL02.MQUA130', 0.),
            ('SARCL02.MQUA150', 0.),
            ('SARCL02.MQSK160', 0.),
            ('SARCL02.MQUA210', 0.),
            ('SARCL02.MQUA250', 0.),
            ],
        'Undulator Entrance/Projected (single-quad)': [ # Changed by Eduard on 2020-11-25
            ('SARMA01.MQUA010', -1.178719103760643e+00),
            ('SARMA01.MQUA060', 1.497124834460192e+00),
            ('SARMA01.MQUA080', -1.089159917693736e+00),
            ('SARMA01.MQUA120', 7.850371107507448e-01),
            ('SARMA01.MQUA140', None),
            ('SARMA02.MQUA050', 0), # Needs to be 0 for wire scanner
            ],
        'Aramis post-undulator/Projected (single-quad)': [ # Checked
            ('SARUN13.MQUA080', -2.061063663263000e+00),
            ('SARUN14.MQUA080', 1.421916195980303e+00),
            ('SARUN15.MQUA080', 9.756434398873166e-01),
            ('SARUN16.MQUA080', -2.579999247748875e+00),
            ('SARUN17.MQUA080', 1.534240455230828e+00),
            ('SARUN18.MQUA080', None),
            ('SARUN19.MQUA080', 0.),
            ('SARUN20.MQUA080', 0.),
            ('SARBD01.MQUA020', 0.),
            ],
        'Aramis post-undulator/Slice (multi-quad)': [ # Checked
            ('SARUN15.MQUA080', '__file__'),
            ('SARUN16.MQUA080', '__file__'),
            ('SARUN17.MQUA080', '__file__'),
            ('SARUN18.MQUA080', '__file__'),
            ('SARUN19.MQUA080', '__file__'),
            ('SARUN20.MQUA080', 0.),
            ('SARBD01.MQUA020', 0.),
            ('SARBD02.MQUA030', 0.),
            ],
        'Athos/Projected (single-quad)': [
            ('SATDI01.MQUA250', -7.487880524702719e-01),
            ('SATDI01.MQUA260', 1.437119676428307e+00),
            ('SATDI01.MQUA280', 1.888304214946000e-01),
            ('SATDI01.MQUA300', -8.016960474273966e-01),
            ('SATCB01.MQUA230', None),
            ('SATCB01.MQUA430', 0.),
            ('SATCL02.MQUA230', 0.),
            ('SATCL02.MQUA430', 0.),
            ],
        'Athos post-undulator/Projected (single-quad)':[
            ('SATUN22.MQUA080', -4.352884290621318e-01),
            ('SATMA02.MQUA010', -1.171469785526617e+00),
            ('SATMA02.MQUA020', 4.007108540382343e+00),
            ('SATMA02.MQUA040', -8.509196941176438e-01),
            ('SATMA02.MQUA050', -4.279282251877575e+00),
            ('SATMA02.MQUA070', 3.057828766496955e+00),
            ('SATBD01.MQUA010', None),
            ('SATBD01.MQUA030', 0),
            ('SATBD01.MQUA050', 0),
            ('SATBD01.MQUA070', 0),
            ('SATBD01.MQUA090', 0),
            ],
        }

# measurement quads (depending on location and measurement type)
# extract from defaultKValues
MeasurementQuads = {key: list(list(zip(*value))[0]) for key, value in defaultKValues.items()}

# Length of quad
Lq_dict = {
        'BC1/Projected (single-quad)': 0.15,
        'BC1/Espread': 0.15,
        'BC1/Slice (single-quad)': 0.15,
        'BC2/Projected (single-quad)': 0.15,
        'Laser Heater/Und. off, Projected (single-quad)': 0.15,
        'Laser Heater/Und. on, Projected (single-quad)': 0.15,
        'Laser Heater/Espread REF': 0.15,
        'Laser Heater/Espread TIGHT': 0.15,
        'Laser Heater/Espread LOOSE': 0.15,
        'Switchyard/Projected (single-quad)': 0.15,
        'Linac 3 End/Projected (single-quad)': 0.15,
        'Undulator Entrance/Projected (single-quad)': 0.3,
        'Aramis post-undulator/Projected (single-quad)': 0.08,
        'Athos/Projected (single-quad)': 0.15,
        'Athos post-undulator/Projected (single-quad)': 0.3,
        }

# Length of drifts
Ld_dict = {
        'BC1/Projected (single-quad)': 10.5055 + 4.9,  # from online model and VA
        'BC1/Espread': 10.5055 + 4.9,
        'BC1/Slice (single-quad)': 10.5055 - 4.9,
        'BC2/Projected (single-quad)': 24.4748,  # from online model and VA
        'Laser Heater/Und. off, Projected (single-quad)': 5.1235-0.15,
        'Laser Heater/Und. on, Projected (single-quad)': 5.1235-0.15,
        'Laser Heater/Espread REF': 5.1235-0.15,
        'Laser Heater/Espread TIGHT': 5.1235-0.15,
        'Laser Heater/Espread LOOSE': 5.1235-0.15,
        'Linac 3 End/Projected (single-quad)': 21.0925,
        'Switchyard/Projected (single-quad)': 10.3785,
        'Undulator Entrance/Projected (single-quad)': 4.6945,
        'Aramis post-undulator/Projected (single-quad)': 11.692,
        'Athos/Projected (single-quad)': 19.2905,
        'Athos post-undulator/Projected (single-quad)': 10.5,
        }

# For wire scanners
Ld_dict_WS = deepcopy(Ld_dict)
Ld_dict_WS['Undulator Entrance/Projected (single-quad)'] = 5.25
default_WS_velocity = 600

# Phase advance
muVec_dict = {
        'BC1/Projected (single-quad)': np.linspace(15, 165, 31),
        'BC1/Espread': np.linspace(15, 165, 31),
        'BC2/Projected (single-quad)': np.linspace(15, 165, 31),
        'BC1/Slice (single-quad)': np.linspace(15, 165, 31),
        'Laser Heater/Und. off, Projected (single-quad)': np.linspace(15, 165, 31),
        'Laser Heater/Und. on, Projected (single-quad)': np.linspace(15, 165, 31),
        'Laser Heater/Espread REF': np.linspace(15, 165, 31),
        'Laser Heater/Espread TIGHT': np.linspace(15, 165, 31),
        'Laser Heater/Espread LOOSE': np.linspace(15, 165, 31),
        'Switchyard/Projected (single-quad)': np.linspace(15, 165, 31),
        'Linac 3 End/Projected (single-quad)': np.linspace(15, 165, 31),
        'Undulator Entrance/Projected (single-quad)': np.linspace(20, 160, 29),
        'Aramis post-undulator/Projected (single-quad)': np.linspace(20, 160, 29),
        'Athos/Projected (single-quad)': np.linspace(15, 165, 31),
        'Athos post-undulator/Projected (single-quad)': np.linspace(15, 165, 31),
        }

ws_muVec_dict = deepcopy(muVec_dict)

ws_muVec_dict['BC1/Projected (single-quad)'] = np.arange(30, 150.001, 5)
ws_muVec_dict['Linac 3 End/Projected (single-quad)'] = np.arange(45, 135.001, 5)
#'Linac 3 End/Projected (single-quad)': np.arange(45, 135.01, 5), # Used for wire scan test in October 2018, and 25 November 2018

# reconstruction point and design optics at this point
RP = {
        'BC1/Projected (single-quad)': ['S10CB01.MQUA230'],
        'BC1/Espread': ['S10CB02.MQUA230'],
        'BC1/Slice (single-quad)': ['S10CB02.MQUA230'],
        'BC1/Slice (multi-quad)': ['SINDI02.MQUA020'],
        'BC2/Projected (single-quad)': ['S10BC01.MQUA100'],
        'Laser Heater/Und. off, Projected (multi-quad)': ['SINLH02.MQUA410'],
        'Laser Heater/Und. off, Projected (single-quad)': ['SINLH03.MQUA080'],
        'Laser Heater/Und. on, Projected (single-quad)': ['SINLH03.MQUA080'],
        'Laser Heater/Espread REF': ['SINLH03.MQUA080'],
        'Laser Heater/Espread TIGHT': ['SINLH03.MQUA080'],
        'Laser Heater/Espread LOOSE': ['SINLH03.MQUA080'],
        'Switchyard/Projected (single-quad)': ['S20SY03.MQUA030'],
        'Linac 3 End/Projected (single-quad)': ['S30CB15.MQUA430'],
        'Linac 3 End/Slice (multi-quad)': ['S30CB10.MQUA430'],
        'Undulator Entrance/Projected (single-quad)': ['SARMA01.MQUA140'],
        'Aramis post-undulator/Projected (single-quad)': ['SARUN18.MQUA080'],
        'Aramis post-undulator/Slice (multi-quad)': ['SARUN15.MQUA080'],
        'Athos/Projected (single-quad)': ['SATCB01.MQUA230'],
        'Athos post-undulator/Projected (single-quad)': ['SATBD01.MQUA010'],
      }

wire_scanner, profile_monitor, ws_bdserver = 'Wire scanner', 'Screen', 'WS BD server'
type_dict = {
        'BC1/Projected (single-quad)': (profile_monitor, wire_scanner, ws_bdserver),
        'BC1/Espread': (profile_monitor,),
        'BC1/Slice (single-quad)': (profile_monitor,),
        'BC1/Slice (multi-quad)': (profile_monitor,),
        'BC2/Projected (single-quad)': (profile_monitor,),
        'Laser Heater/Und. off, Projected (multi-quad)': (profile_monitor,),
        'Laser Heater/Und. off, Projected (single-quad)': (profile_monitor,),
        'Laser Heater/Und. on, Projected (single-quad)': (profile_monitor,),
        'Laser Heater/Espread REF': (profile_monitor,),
        'Laser Heater/Espread TIGHT': (profile_monitor,),
        'Laser Heater/Espread LOOSE': (profile_monitor,),
        'Switchyard/Projected (single-quad)': (wire_scanner, ws_bdserver),
        'Linac 3 End/Projected (single-quad)': (profile_monitor, wire_scanner, ws_bdserver),
        'Linac 3 End/Slice (multi-quad)': (profile_monitor,),
        'Undulator Entrance/Projected (single-quad)': (profile_monitor, wire_scanner),
        'Aramis post-undulator/Projected (single-quad)': (profile_monitor,),
        'Aramis post-undulator/Slice (multi-quad)': (profile_monitor,),
        'Athos/Projected (single-quad)': (profile_monitor,),
        'Athos post-undulator/Projected (single-quad)': (profile_monitor,)
      }

wireScanDict = {
        'BC1/Projected (single-quad)':'S10DI01.DWSC010',
        'Linac 3 End/Projected (single-quad)': 'SARCL01.DWSC160',
        'Switchyard/Projected (single-quad)': 'S20SY03.DWSC090',
        'Undulator Entrance/Projected (single-quad)': 'SARMA02.DWSC060',
        }

wireScan_blm_Dict = {
        'BC1/Projected (single-quad)': 'S10DI01-DBLM045',
        'Linac 3 End/Projected (single-quad)': 'SARCL02-DBLM135',
        'Switchyard/Projected (single-quad)': 'S20SY03-DBLM110',
        'Undulator Entrance/Projected (single-quad)': 'SARUN04-DBLM030',
        }

wireScan_wire_enum = {
        'X1': 0,
        'X2': 1,
        'Y1': 2,
        'Y2': 3,
        }

bxD = {
        'BC1/Projected (single-quad)': 11.5541,
        'BC1/Espread': 11.5541,
        'BC1/Slice (single-quad)': 7.01,
        'BC1/Slice (multi-quad)': 11.1557,
        'BC2/Projected (single-quad)': 18.3561,
        'Laser Heater/Und. off, Projected (multi-quad)': 20,
        'Laser Heater/Und. off, Projected (single-quad)': 5.1235,
        'Laser Heater/Und. on, Projected (single-quad)': 5.1235,
        'Laser Heater/Espread REF': 5.1235,
        'Laser Heater/Espread TIGHT': 5.1235,
        'Laser Heater/Espread LOOSE': 10.2470,
        'Switchyard/Projected (single-quad)': 14.0110,
        'Linac 3 End/Projected (single-quad)': 25.311,
        'Linac 3 End/Slice (multi-quad)': 8.830557105,
        'Undulator Entrance/Projected (single-quad)': 5.25, # Changed by Eduard on 2020-11-25
        'Aramis post-undulator/Projected (single-quad)': 13.3114,
        'Aramis post-undulator/Slice (multi-quad)': 15.56,
        'Athos/Projected (single-quad)': 14.5804,
        'Athos post-undulator/Projected (single-quad)': 3.15,
       }

axD = {
        'BC1/Projected (single-quad)': 0.75,
        'BC1/Espread': 0.75,
        'BC1/Slice (single-quad)': 1.25,
        'BC1/Slice (multi-quad)': -1.17,
        'BC2/Projected (single-quad)': 0.75,
        'Laser Heater/Und. off, Projected (multi-quad)': 2.0,
        'Laser Heater/Und. off, Projected (single-quad)': 1.0,
        'Laser Heater/Und. on, Projected (single-quad)': 1.0,
        'Laser Heater/Espread REF': 1.,
        'Laser Heater/Espread TIGHT': 1.,
        'Laser Heater/Espread LOOSE': 2.,
        'Switchyard/Projected (single-quad)': 1.35,
        'Linac 3 End/Projected (single-quad)': 1.2,
        'Linac 3 End/Slice (multi-quad)': 0.5484662386,
        'Undulator Entrance/Projected (single-quad)':1.,  # Changed by Eduard on 2020-11-25
        'Aramis post-undulator/Projected (single-quad)':1.1424,
        'Aramis post-undulator/Slice (multi-quad)': -1.56,
        'Athos/Projected (single-quad)': 0.75,
        'Athos post-undulator/Projected (single-quad)': 0.3,
       }

byD = {
        'BC1/Projected (single-quad)': 11.5541,
        'BC1/Espread': 11.5541,
        'BC1/Slice (single-quad)': 1.4,
        'BC1/Slice (multi-quad)': 50.0,
        'BC2/Projected (single-quad)': 18.3561,
        'Laser Heater/Und. off, Projected (multi-quad)': 0.8,
        'Laser Heater/Und. off, Projected (single-quad)': 5.1235,
        'Laser Heater/Und. on, Projected (single-quad)': 5.1235,
        'Laser Heater/Espread REF': 5.1235,
        'Laser Heater/Espread TIGHT': 5.1235,
        'Laser Heater/Espread LOOSE': 10.2470,
        'Switchyard/Projected (single-quad)': 14.0110,
        'Linac 3 End/Projected (single-quad)': 25.311,
        'Linac 3 End/Slice (multi-quad)': 30.44664836,
        'Undulator Entrance/Projected (single-quad)': 5.25,  # Changed by Eduard on 2020-11-25
        'Aramis post-undulator/Projected (single-quad)':13.3114,
        'Aramis post-undulator/Slice (multi-quad)': 5.74,
        'Athos/Projected (single-quad)': 14.5804,
        'Athos post-undulator/Projected (single-quad)': 3.15,
       }

ayD = {
        'BC1/Projected (single-quad)': 0.75,
        'BC1/Espread': 0.75,
        'BC1/Slice (single-quad)': 0.25,
        'BC1/Slice (multi-quad)': 0.0,
        'BC2/Projected (single-quad)': 0.75,
        'Laser Heater/Und. off, Projected (multi-quad)': 0.0,
        'Laser Heater/Und. off, Projected (single-quad)': 1.0,
        'Laser Heater/Und. on, Projected (single-quad)': 1.0,
        'Laser Heater/Espread REF': 1.,
        'Laser Heater/Espread TIGHT': 1.,
        'Laser Heater/Espread LOOSE': 2.,
        'Switchyard/Projected (single-quad)': 1.35,
        'Linac 3 End/Projected (single-quad)': 1.2,
        'Linac 3 End/Slice (multi-quad)': -1.866499484,
        'Undulator Entrance/Projected (single-quad)': 1.,  # Changed by Eduard on 2020-11-25
        'Aramis post-undulator/Projected (single-quad)':1.1424,
        'Aramis post-undulator/Slice (multi-quad)': 0.58,
        'Athos/Projected (single-quad)': 0.75,
        'Athos post-undulator/Projected (single-quad)': 0.3,
       }

# files+'.txt', constants is length of quads
files_constants_dict = {
        'BC1/Slice (multi-quad)': ('BC1', 0.15),
        'Linac 3 End/Slice (multi-quad)': ('L3', [0.15,0.15,0.15,0.3,0.3,0.3,]),
        'Laser Heater/Und. off, Projected (multi-quad)': ('LH0', 0.15),
        'Aramis post-undulator/Slice (multi-quad)': ('UNDX', 0.08,),
        }

tilt_quads_dict = {
        'X': {
            'BC1': ['SINBC02.MQUA120', 'SINBC02.MQUA340',],
            'Linac 3 End': ['S10BC02.MQUA120', 'S10BC02.MQUA340',],
            },
        'Y': {
            'BC1': ['SINBC02.MQSK110', 'SINBC02.MQSK350',],
            'Linac 3 End': ['S10BC02.MQSK110', 'S10BC02.MQSK350',],
            },
        }

tilt_sext_dict = {
         'X': {
             'BC1': ['SINBC02.MSEX130', 'SINBC02.MSEX330'],
             'Linac 3 End': ['S10BC02.MSEX130', 'S10BC02.MSEX330',],
             },
         'Y': {
             'BC1': ['None', 'None',],
             'Linac 3 End': ['None', 'None'],
             },
         }

tilt_sext_quad_dict = {}
for dim in ('X', 'Y'):
    tilt_sext_quad_dict[dim] = {}
    for key in tilt_quads_dict[dim]:
        tilt_sext_quad_dict[dim][key] = tilt_quads_dict[dim][key]+tilt_sext_dict[dim][key]
del dim, key

tdc_dict = {
        'BC1': {
            'pv': 'SINDI01-RSYS:SET-ACC-VOLT',
            'pv_phase': 'SINDI01-RSYS:GET-BEAM-PHASE',
            'pv_status': 'SINDI01-RMSM:SM-GET', # 9 is on beam
            'betaY_design': 50,
            'freq': 2.997912e9,
            },
        'Linac 3 End': {
            'pv': 'S30CB14-RSYS:SET-ACC-VOLT',
            'pv_phase': 'S30CB14-RSYS:GET-BEAM-PHASE',
            'pv_status': 'S30CB14-RMSM:SM-GET',
            'betaY_design': 60,
            'freq': 5.712e9, # Design report is wrong
            }
        }

laser_status = OrderedDict([
        ('Aramis', 'SIN-TIMAST-TMA:Bunch-1-OnDelay-Sel'),
        ('Athos', 'SIN-TIMAST-TMA:Bunch-2-OnDelay-Sel'),
        ])

default_misalignment_sig = 1.5

default_tilt_options = {
        'method': 'all',
        'order': 2,
        'w_order': 2,
        'treshold': 0.2,
        }

default_camera_options = {
        'image_good_region/treshold': 0.3,
        'image_good_region/gfscale': 6,
        'image_slices/number_of_slices': 21,
        'image_slices/scale': 5,
        }

bdServerLocations = {
        'Laser Heater': 'LH',
        'BC1': 'BC1',
        'BC2': 'BC2',
        'Linac 3 End': 'ARCOL',
        'Aramis post-undulator': 'ARDUMP',
        'Athos': 'ATHOS',
        }

location_bunches = {
        'Laser Heater': (1, 2),
        'BC1': (1, 2),
        'BC2': (1, 2),
        'Switchyard': (1, 2),
        'Linac 3 End': (1,),
        'Undulator Entrance': (1,),
        'Aramis post-undulator': (1,),
        'Athos': (2,),
        'Athos post-undulator': (2,),
        }

