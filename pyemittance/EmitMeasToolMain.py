import sys
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PyQt4 import QtGui
from PyQt4.uic import loadUiType

import elog
from OMEpicsChannel import EpicsChannel
from epics import caget, caput

from pyemittance.MatchingToolMain import StartMatch, printOptics
from pyemittance.TiltCorrectionMain import startTiltWindow
from h5_storage import saveH5Recursive, loadH5Recursive
from pyemittance import EmittanceToolConfig
from pyemittance import beamdynamics
from pyemittance import EmitMeasToolCore
from pyemittance import plot_results


#TODO
#- Qt5 and python3.7
#- Better separation of daq, analysis and plotting
#- Separate daq function for wire scanner and screen measurement
#- Warnings when conditions are not fulfilled
#    - TDC must be on for slice meas
#    - Certain RF stations must be off under some circumstances
#    - Measurement screen must be inserted
#- Integrated plots instead of new windows
#- Daq in a thread, non-blocking (I might have to ask Sven for help here)

Ui_MainWindow, QMainWindow = loadUiType('EmitMeasToolGUI.ui')

class StartMain(QMainWindow, Ui_MainWindow):

    saveStatusNone, saveStatusSaved, saveStatusNotSaved = 'Status:\nNo measurement yet', 'Status:\nData saved as h5', 'Status:\nData not saved as h5'
    dryRunAtBegin = False

    def __init__(self):
        super(StartMain, self).__init__()
        self.setupUi(self)

        # initiate connection to EPICS system
        self.EC = EpicsChannel()

        # definition of functions when the user does something in the GUI
        self.MeasLocationGUI.activated.connect(self.SelectLocation)
        self.DimensionGUI.activated.connect(self.SelectDimension)
        self.MeasTypeGUI.activated.connect(self.SelectType)
        self.MeasDeviceGUI.activated.connect(self.SelectPM)
        self.EnergySelect.activated.connect(self.SelectEnergy)
        self.EnergyManual.editingFinished.connect(self.UpdateManualEnergy)
        self.DoMeasurement.clicked.connect(self.StartMeasurement)
        self.PrintOpticsGUI.clicked.connect(self.printOptics)
        self.SaveData.clicked.connect(self.SaveElogAndH5)
        self.SaveDataH5Only.clicked.connect(self.SaveH5)
        self.LoadData.clicked.connect(self.LoadH5)
        self.startPlotClientGUI.clicked.connect(self.startPlotClient)
        self.DoMatching.clicked.connect(self.StartMatching)
        self.RestoreMeasQuadsGUIInitial.clicked.connect(self.RestoreMeasQuadsInitial)
        self.DryRunButton.setChecked(self.dryRunAtBegin)
        self.PushResultsButton.clicked.connect(self.push_results)
        self.ClosePlotsGUI.clicked.connect(lambda: plt.close('all'))

        self.Energy_MeV = float(str(self.EnergyDisplay.text()))
        self.CouplingGUI.toggled.connect(self.SelectCoupling)
        self.SelectCoupling()

        # initial variables
        self.MeasType = str(self.MeasTypeGUI.itemText(0))

        for key in EmittanceToolConfig.available_measurementTypes.keys():
            self.MeasLocationGUI.addItem(key)
        self.Dimension = 'X' # will be overridden later

        # If you select the location, a few things need to be updated.
        # - first the measurement type. Then the measurement device. Then the Profile Monitor
        self.SelectLocation()

        self.QuadNames = EmittanceToolConfig.MeasurementQuads[self.MeasLocation + '/' + self.MeasType]

        self.openTiltCorrectionInGUI.clicked.connect(self.openTiltWindow)

        self.StatusSaveGUI.setText(self.saveStatusNone)
        self.StatusSaveGUI.setStyleSheet('background-color:green')

        self.Emit_data = None

        self.igr_tresholdGUI.setText('%.2f' % EmittanceToolConfig.default_camera_options['image_good_region/treshold'])
        self.igr_gfscaleGUI.setText('%.2f' % EmittanceToolConfig.default_camera_options['image_good_region/gfscale'])
        self.is_number_of_slicesGUI.setText('%i' % EmittanceToolConfig.default_camera_options['image_slices/number_of_slices'])
        self.is_scaleGUI.setText('%.2f' % EmittanceToolConfig.default_camera_options['image_slices/scale'])

        self.WS_velocity.setText('%i' % EmittanceToolConfig.default_WS_velocity)


        # initialization of "global" variables
        # Only needed for matching tool
        self.bxM = 10
        self.axM = 0
        self.byM = 10
        self.ayM = 0
        self.En = 150

    def printOptics(self):
        if self.Emit_data is not None:
            return printOptics(self.Emit_data)

    def SelectDimension(self):
        self.Dimension = str(self.DimensionGUI.currentText())
        self.SelectPM()

    def SelectCoupling(self):
        if self.CouplingGUI.isChecked():
            self.Coupling = 1
        else:
            self.Coupling = 0

    @property
    def MeasLocation(self):
        return self.MeasLocationGUI.currentText()

    @property
    def DryRun(self):
        return self.DryRunButton.isChecked()

    @property
    def PhaseAdvanceSteps(self):
        return int(self.PhaseAdvance.text())

    @property
    def NumberImages(self):
        return int(str(self.NumImages.text()))

    def startPlotClient(self):
        cmd_str = 'java -cp /opt/gfa/pshell/testing ch.psi.pshell.plotter.View &'
        print(cmd_str)
        os.system(cmd_str)

    @property
    def ws_config(self):
        return {
                'n_points': int(self.WS_velocity.text()),
                'dimension': str(self.DimensionGUI_WS.currentText()),
                }

    @property
    def plot_tilt(self):
        return self.PlotTiltGUI.isChecked()

    @property
    def plot_misplacement(self):
        return self.PlotMisplacementGUI.isChecked()

    @property
    def plot_options(self):
        return {
                'plot_tilt': self.plot_tilt,
                'plot_misplacement': self.plot_misplacement,
                }

    def SelectPM(self):
        device = self.MeasurementDevice
        if device in (EmittanceToolConfig.wire_scanner, EmittanceToolConfig.ws_bdserver):
            self.MeasProfMon = EmittanceToolConfig.wireScanDict[self.MeasLocation+'/'+self.MeasType]
        elif device == EmittanceToolConfig.profile_monitor:
            if self.Dimension == 'Y' and self.MeasType == 'Slice (multi-quad)':
                self.MeasProfMon = EmittanceToolConfig.PM[self.MeasLocation+'_Yslice']
            elif self.Dimension == 'X' and self.MeasType == 'Slice (multi-quad)':
                if self.MeasLocation+'_Xslice' in EmittanceToolConfig.PM:
                    self.MeasProfMon = EmittanceToolConfig.PM[self.MeasLocation+'_Xslice']
                else:
                    self.MeasProfMon = EmittanceToolConfig.PM[self.MeasLocation]
            else:
                self.MeasProfMon = EmittanceToolConfig.PM[self.MeasLocation]
        else:
            raise ValueError('Illegal MeasurementDevice: %s' % device)

        self.PMGUI.setText(self.MeasProfMon)

    @property
    def instance_config_update(self):
        return {
                'image_good_region': {
                    'treshold': float(self.igr_tresholdGUI.text()),
                    'gfscale': float(self.igr_gfscaleGUI.text()),
                    },
                'image_slices': {
                    # Must be an integer, else range raises an error.
                    'number_of_slices': int(self.is_number_of_slicesGUI.text()),
                    'scale': float(self.is_scaleGUI.text()),
                    }
                }

    @property
    def screen_resolution(self):
        return float(self.SubtractResolutionGUI.text())*1e-6

    def SelectLocation(self):
        MeasLocation = self.MeasLocation
        self.MeasTypeGUI.clear()

        for item in EmittanceToolConfig.available_measurementTypes[MeasLocation]:
            self.MeasTypeGUI.addItem(item)

        self.MeasType = self.MeasTypeGUI.currentText()
        self.QuadNames = EmittanceToolConfig.MeasurementQuads[MeasLocation + '/' + self.MeasType]
        self.MeasQuads.setText(str(self.QuadNames))

        # reading initial measurement quads currents
        self.QuadI0 = []
        QuadIMch = []
        for i in range(0, len(self.QuadNames)):
            QuadIMch.append(self.QuadNames[i].replace('.', '-') + ':I-SET')

        self.EC.addGroup('QuadIM', QuadIMch)
        temp = self.EC.get('QuadIM')
        self.QuadI0 = temp[1]
        self.EC.cafe.groupClose('QuadIM')

        # Set new energy from energy server when location is changed!
        self.SelectEnergy()
        self.SelectType()

        #self.SelectPM()


    def SelectDevice(self):
        self.MeasDeviceGUI.clear()
        for i in EmittanceToolConfig.type_dict[self.MeasLocation + '/' + self.MeasType]:
            self.MeasDeviceGUI.addItem(i)
        self.SelectPM()

    @property
    def MeasurementDevice(self):
        device = self.MeasDeviceGUI.currentText()
        if not device:
            device = EmittanceToolConfig.profile_monitor
        return device


    def SelectType(self):
        self.MeasType = self.MeasTypeGUI.currentText()
        self.QuadNames = EmittanceToolConfig.MeasurementQuads[self.MeasLocation + '/' + self.MeasType]
        self.MeasQuads.setText(str(self.QuadNames))

        # reading initial measurement quads currents
        self.QuadI0 = []
        QuadIMch = []
        for i in range(0, len(self.QuadNames)):
            QuadIMch.append(self.QuadNames[i].replace('.', '-') + ':I-SET')

        self.EC.addGroup('QuadIM', QuadIMch)
        temp = self.EC.get('QuadIM')
        self.QuadI0 = temp[1]
        self.EC.cafe.groupClose('QuadIM')

        self.SelectDevice()

    def SelectEnergy(self):
        SelectEnergy = self.EnergySelect.currentIndex()
        if SelectEnergy == 1:
            self.EnergyManual.setEnabled(True)
        else:
            self.EnergyManual.setEnabled(False)
            pv = self.MeasProfMon.replace('.', '-') + ':ENERGY-OP'
            self.Energy_MeV = caget(pv)
            self.EnergyDisplay.setText(str(round(self.Energy_MeV,2)))

    def UpdateManualEnergy(self):
        self.Energy_MeV = float(str(self.EnergyManual.text()))
        self.EnergyDisplay.setText(str(self.Energy_MeV))

    def StartMeasurement(self):
        tilt_options = {
                'method': startTiltWindow.default_analysis_method,
                'order': startTiltWindow.default_fit_order,
                'w_order': startTiltWindow.default_weighting_order,
                'treshold': startTiltWindow.default_treshold,
                }

        if self.screen_resolution != 0:
            raise NotImplementedError('Screen resolution != 0 not supported!')

        Emit_data = EmitMeasToolCore.perform_meas_screen(
                self.MeasLocation,
                self.MeasType,
                self.PMGUI.text(),
                self.Energy_MeV*1e6,
                self.PhaseAdvanceSteps,
                self.NumberImages,
                self.QuadNames,
                self.instance_config_update,
                self.MeasurementDevice,
                dimension=self.Dimension,
                dry_run=self.DryRun,
                )
        Emit_data['Input'].update({
            'tilt_options': tilt_options,
            'plot_options': self.plot_options,
            'screen_resolution': self.screen_resolution,
            })

        print('Analyze pyscan result...')
        meta_data = beamdynamics.analyzePyscanResult(Emit_data)
        Emit_data['Meta_data'] = meta_data
        print('Pyscan result analyzed')

        print('Showing plots')
        plot_results.plot_all(Emit_data, **self.plot_options)

        Emit_data['Meta_data'] = meta_data
        # For matching tool. Only set optics when all necessary results are there
        try:
            self.bxM, self.axM = meta_data['proj_emittance_X']['beta'], meta_data['proj_emittance_X']['alpha']
            print('Projected X optics set for matching')
        except (KeyError, IndexError):
            print('No projected X optics')
        try:
            self.byM, self.ayM = meta_data['proj_emittance_Y']['beta'], meta_data['proj_emittance_Y']['alpha']
            print('Projected Y optics set for matching')
        except (KeyError, IndexError):
            print('No projected Y optics')

        self.Emit_data = Emit_data

        print('Post measurement called')
        self.postMeasurement(Emit_data)
        print('Done. Return Emit_data')
        return Emit_data

    def postMeasurement(self, Emit_data, nosave=False):
        self.Emit_data = Emit_data
        self.StatusSaveGUI.setText(self.saveStatusNotSaved)

        if not nosave and self.AlwaysSaveButton.isChecked():
            if self.DryRun:
                print('Not saving dry run data')
            else:
                self.SaveH5()

    def h5_filename(self):
        gui_text = os.path.expanduser(self.h5PathSave.text().strip())
        if gui_text == 'default':
            date = datetime.now()
            return date.strftime('/sf/data/measurements/%Y/%m/%d/%Y%m%d_%H%M%S_EmittanceTool.h5')
        elif gui_text.endswith('.h5'):
            return gui_text
        else:
            return gui_text+'.h5'

    def SaveElogAndH5(self):

        if self.StatusSaveGUI.text() == self.saveStatusNotSaved or self.h5PathSave.text() != 'default':
            self.SaveH5()
        else:
            print('h5 data already saved')

        image_number = int(self.MatplotlibNumberGUI.text())
        if image_number != self.last_fignum:
            self.SaveFigure()

        h5_filename, jpg_filename = self.last_h5_filename, self.last_jpg_filename
        logbook = elog.open('https://elog-gfa.psi.ch/SwissFEL+commissioning+data/')
        text = 'Measurement location: %s' % self.Emit_data['Input']['Measurement location']
        text += '\nMeasureement type: %s' % self.Emit_data['Input']['Measurement type']
        text += '\nData saved in ' + h5_filename
        text += '\nAramis laser status: %s' % self.Emit_data['Laser_data']['Aramis']
        text += '\nAthos laser status: %s' % self.Emit_data['Laser_data']['Athos']
        text += printOptics(self.Emit_data, print_=False)
        if self.elogCommentGUI.text():
            text += '\n%s' % self.elogCommentGUI.text()
        dict_att = {'Author': 'Application: Emittance Tool', 'Category': 'Measurement', 'Title':'Emittance measurement'}
        logbook.post(text, attributes=dict_att,attachments=[jpg_filename])

        print('\nFigure was saved in ELOG')

    def SaveFigure(self):
        h5_filename = self.h5_filename()
        jpg_filename = h5_filename.replace('.h5', '.jpg')
        image_number = int(self.MatplotlibNumberGUI.text())
        if image_number == -1:
            num = plt.get_fignums()[-1]
        else:
            num = image_number
        fig = plt.figure(num)
        fig.savefig(jpg_filename)
        self.last_fignum = num
        self.last_jpg_filename = jpg_filename

    def SaveH5(self):

        h5_filename = self.h5_filename()
        self.activateWindow()
        self.SaveFigure()

        saveH5Recursive(h5_filename, self.Emit_data)

        print('Data saved in file %s' % h5_filename)
        self.StatusSaveGUI.setText(self.saveStatusSaved)

        self.last_h5_filename = h5_filename

    def LoadH5(self):
        h5_filename = os.path.expanduser(self.h5PathLoad.text().strip())
        if not os.path.isfile(h5_filename):
            raise ValueError('No file here: %s' % h5_filename)
        self.Emit_data = loadH5Recursive(h5_filename)
        plot_results.plot_all(self.Emit_data)

    def push_results(self):
        Emit_data = self.Emit_data
        if Emit_data is None:
            print('No data saved. Cannot push results!')
            return

        location = Emit_data['Input']['Measurement location']
        loc_string = EmittanceToolConfig.bdServerLocations[location]


        if loc_string is None:
            print('No EPICS channel available for this measurement location: %s' % location)
            return

        # What bunch was measured? When it was at a location where both bunches pass through,
        # we need to find out which laser was the only one that was turnded on.
        available_bunches = EmittanceToolConfig.location_bunches[location]
        if len(available_bunches) == 1:
            use_bunch_num = available_bunches[0]
        else:
            laser_data = Emit_data['Laser_data']
            bunch_nums = []
            for bunch_num, beamline in enumerate(EmittanceToolConfig.laser_status.keys(), 1):
                if laser_data[beamline] == 'On beam':
                    bunch_nums.append(bunch_num)

            if len(bunch_nums) == 1:
                use_bunch_num = bunch_nums[0]
            else:
                raise ValueError('Expect only one valid bunch number. But there are %i: %s' % (len(bunch_nums), bunch_nums))

        bunch_string = 'BUNCH%i' % use_bunch_num
        epics_data = Emit_data['Meta_data']['sfbd_epics_data']
        for key, value in epics_data.items():
            # Sven is responsible for these channels
            pv_name = 'SFBD-MEAS:%s-%s-%s' % (key, loc_string, bunch_string)
            if self.DryRun:
                print('I would caput %s %s' % (pv_name, value))
            else:
                print('caput %s %s' % (pv_name, value))
                caput(pv_name, value)
        print('Results were pushed to EPICS channels')

    def StartMatching(self):
        self.Matching = StartMatch(EmitMeasToolCore.SM, self.Emit_data, self.MeasLocation, self.MeasType, self.bxM, self.axM, self.byM, self.ayM)
        self.Matching.show()

    def RestoreMeasQuadsInitial(self):
        quads = self.QuadNames

        QuadIch, QuadI0 = [], self.QuadI0
        for i in range(0, len(quads)):
            QuadIch.append(quads[i].replace('.', '-') + ':I-SET')

        if self.DryRun:
            print('I would set %s to %s' % (quads, QuadI0))
        else:
            self.EC.addGroup('QuadI', QuadIch)
            self.EC.put('QuadI', QuadI0)
            self.EC.cafe.groupClose('QuadI')
            print('Measurement Quads have been restored!')

    def openTiltWindow(self):
        self.tiltCorrection = startTiltWindow(self.MeasLocation, self.MeasProfMon, self.Dimension, self)
        self.tiltCorrection.show()


#########################################################################

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    myapp = StartMain()

    myapp.show()
    sys.exit(app.exec_())

