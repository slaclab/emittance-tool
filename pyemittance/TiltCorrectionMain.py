import os
import time
import itertools
import datetime
import h5py
import numpy as np
import matplotlib.pyplot as plt

from PyQt4 import QtGui
from PyQt4.uic import loadUiType

from epics import caget, caput
#import pyscan
#from cam_server import PipelineClient
#from cam_server.utils import get_host_port_from_stream_address

import beamdynamics
import plot_results
import EmitMeasToolCore
import EmittanceToolConfig
import tilt as tilt_module

Ui_MainWindow, QMainWindow = loadUiType('TiltGUI2.ui')

class startTiltWindow(QMainWindow, Ui_MainWindow): # class to start the application

    maxIterationColumns = 4 # Dont change this value without also changing the UI
    iterationColumnsTotal = 5

    iterationRowsTotal = 12
    # Rows begin at number ...
    nTargetsTable = 0
    nKnobsTable = 4
    nDeltaTable = 8

    time_delay = 1.0 # in seconds, after caput
    MeasType = 'Slice (multi-quad)' # For EmitMeasTool main

    state_MEAS = 'Measure tilt'
    state_CALC = 'Calculate correction'
    state_CORR = 'Correct tilt'

    type44 = '4x4'
    type22lin = '2x2 linear'
    type22quad = '2x2 quadratic'

    dryRunAtBegin = True

    default_analysis_method = 'all'
    default_treshold = 0.2
    default_weighting_order = 2
    default_fit_order = 2

    def __init__(self, location, PM, dimension, main):
        super().__init__()
        self.setupUi(self)

        self.dimension = dimension
        self.DryRunButton.setChecked(self.dryRunAtBegin)
        self.location = location
        self.Location.setText('Location: %s' % location)

        if self.dimension == 'X':
            self.TiltTypeGUI.addItem(self.type22lin)
            self.TiltTypeGUI.addItem(self.type22quad)
            self.TiltTypeGUI.addItem(self.type44)
        elif self.dimension == 'Y':
            self.TiltTypeGUI.addItem(self.type22lin)
        self.TiltTypeGUI.activated.connect(self.updateType)
        self.updateType()


        self.DimensionGUI.setText('Dim: %s' % self.dimension)

        self.main = main
        self.PM = PM
        self.QuadNames = EmittanceToolConfig.MeasurementQuads[self.location+'/'+self.MeasType]

        self.firstMeasurementDone = False

        # SVD user defined percentage initial value

        now = datetime.datetime.now()
        self.filePathGUI.setText('/sf/data/measurements/%i/%02i/%02i/' % (now.year, now.month, now.day))

        self.DryRunButton.toggled.connect(self.selectDryRun)
        self.selectDryRun()

        self.ClearTableButton.clicked.connect(self.clearIterationTable)

        # getting knob names and setting current values if something in the table is touched
        self.knobTableInGUI.currentItemChanged.connect(self.updateTable)
        self.sensitivityTableInGUI.currentItemChanged.connect(self.updateSensitivityMatrixTable)
        self.resultsTableInGUI.currentItemChanged.connect(self.updateResultsTable)

        self.updateTable()
        self.updateSensitivityMatrixTable()
        self.updateResultsTable()

        self.sensitivityMatrixButton.clicked.connect(self.measureSensitivityMatrix)

        self.setIterationNumber(0)
        self.MeasureButton.clicked.connect(self.measureIteration)
        self.CalculateButton.clicked.connect(self.calculateCorrectionIteration)
        self.CorrectButton.clicked.connect(self.correctIteration)
        self.setStateButton(self.state_MEAS)
        self.UseCurrentTiltButton.clicked.connect(self.useCurrentTilt)
        self.ClosePlotsButtonGUI.clicked.connect(lambda: plt.close('all'))

        self.saveSensitivityMatrixButton.clicked.connect(self.saveToFile)
        self.loadSensitivityMatrixButton.clicked.connect(self.loadFromFile)

        for method in tilt_module.TiltAnalyzer.second_order_methods:
            self.TiltMethodGUI.addItem(method)
        self.TiltTresholdGUI.setText('%.2f' % self.default_treshold)
        self.TiltWeightingOrderGUI.setText('%.1f' % self.default_weighting_order)
        self.TiltFitOrderGUI.setText('%i' % self.default_fit_order)

        for col in range(self.iterationRowsDelta):
            self.LastMeasurement.resizeColumnToContents(col)

    def updateType(self):
        print('updateType was called')
        self.correction_type = self.TiltTypeGUI.currentText()
        if self.correction_type == self.type44:
            self.nKnobs = 4
            self.knob0 = 0 # Where is the first knob?
            self.nTargets = 4
            self.iterationRowsTarget = 0
            self.iterationRowsKnobs = 4
            self.iterationRowsDelta = 8

            knob_dict = EmittanceToolConfig.tilt_sext_quad_dict[self.dimension][self.location]
        elif self.correction_type == self.type22lin:
            self.nKnobs = 2
            self.knob0 = 0
            self.nTargets = 2
            self.iterationRowsTarget = 0
            self.iterationRowsKnobs = 4
            self.iterationRowsDelta = 8
            knob_dict = EmittanceToolConfig.tilt_quads_dict[self.dimension][self.location]
        elif self.correction_type == self.type22quad:
            self.nKnobs = 2
            self.knob0 = 2
            self.nTargets = 2
            self.iterationRowsTarget = 2
            self.iterationRowsKnobs = 4
            self.iterationRowsDelta = 8
            knob_dict = EmittanceToolConfig.tilt_sext_dict[self.dimension][self.location]
        else:
            raise ValueError(self.correction_type, 'illegal type')

        self.knob_pvs = [x.replace('.', '-')+':I-READ' for x in knob_dict]

        for pv_ctr, pv in enumerate(self.knob_pvs):
            self.knobTableInGUI.item(pv_ctr,0).setText(pv)
        for ctr in range(pv_ctr+1, 4):
            self.knobTableInGUI.item(ctr,0).setText('None')

        self.plot_currents = {x: [] for x in range(self.nKnobs)}
        self.plot_tilt = []
        self.plot_tiltp = []
        self.plot_tilt_errors = []
        self.plot_tiltp_errors = []

        self.plot_tilt2 = []
        self.plot_tiltp2 = []
        self.plot_tilt2_errors = []
        self.plot_tiltp2_errors = []

        self.clearIterationTable()
        self.updateTable()

        if self.correction_type in (self.type44, self.type22quad) and self.tilt_options['order'] < 2:
            raise ValueError('Order in tilt_options must be at least 2 for this type: %s' % self.correction_type)

    @property
    def second_order_tilt(self):
        second_order_tilt = (self.tilt_options['order'] >= 2)
        return second_order_tilt

    @property
    def show_camera_data(self):
        return self.ShowImageButton.isChecked()

    @property
    def PhaseAdvanceSteps(self):
        return self.main.PhaseAdvanceSteps

    @property
    def tiltAnalysisMethod(self):
        return self.TiltMethodGUI.currentText()

    @property
    def NumberImages(self):
        return self.main.NumberImages

    @property
    def correction_factor(self):
        return float(self.CorrectionFactorGUI.text())

    @property
    def energy_eV(self):
        return self.main.Energy_MeV*1e6

    @property
    def DryRun(self):
        return self.DryRunButton.isChecked()

    @property
    def tilt_options(self):
        return {
                'method': self.TiltMethodGUI.currentText(),
                'order': int(self.TiltFitOrderGUI.text()),
                'w_order': float(self.TiltWeightingOrderGUI.text()),
                'treshold': float(self.TiltTresholdGUI.text()),
                }

    def selectDryRun(self):
        if self.DryRun:
            self.ScreenGUI.setText('simulation')
        else:
            self.ScreenGUI.setText(self.PM)

    @property
    def NoPlots(self):
        return self.NoPlotsButton.isChecked()

    def getIterationColumn(self):
        return min(self.numberOfIterations, self.maxIterationColumns)

    def setIterationNumber(self, number='+1'):
        if number == '+1':
            self.numberOfIterations += 1
        else:
            self.numberOfIterations = number
        self.IterationsLabelGUI.setText('# iterations: %i' % self.numberOfIterations)

    def measureIteration(self):
        self.shiftIterationMatrix()
        result = self.measureTilt()
        self.add_to_plot_lists(result)
        tilt_dict = result['Meta_data']['tilt']
        tilt0, tiltp0 = tilt_dict['tilt'], tilt_dict['tiltp']
        col = self.getIterationColumn()

        self.resultsTableInGUI.item(0, col).setText('%.2e' % tilt0)
        self.resultsTableInGUI.item(1, col).setText('%.2e' % tiltp0)
        if self.second_order_tilt:
            tilt_dict2 = result['Meta_data']['tilt2']
            tilt20, tiltp20 = tilt_dict2['tilt'], tilt_dict['tiltp']
            self.resultsTableInGUI.item(2, col).setText('%.2e' % tilt20)
            self.resultsTableInGUI.item(3, col).setText('%.2e' % tiltp20)
        for x in range(self.nKnobs):
            self.resultsTableInGUI.item(self.iterationRowsKnobs+x, col).setText('%.2e' % self.get_current(x))

        self.setStateButton(self.state_CALC)
        self.plot_results()

    def shiftIterationMatrix(self):
        if self.numberOfIterations <= self.maxIterationColumns:
            print('Iteration %i Not shifting.' % self.numberOfIterations)
            return

        # Shift items by one column, including column headers

        print('Iteration %i Shifting.' % self.numberOfIterations)

        for col in range(2, self.iterationColumnsTotal):
            for row in range(self.iterationRowsTotal):
                text = self.resultsTableInGUI.item(row, col).text()
                self.resultsTableInGUI.item(row, col-1).setText(text)
                #self.resultsTableInGUI.setItem(row, col-1, widget)
            col_header_text = self.resultsTableInGUI.horizontalHeaderItem(col).text()
            new_col_header = QtGui.QTableWidgetItem('%s' % col_header_text)
            self.resultsTableInGUI.setHorizontalHeaderItem(col-1, new_col_header)

        for row in range(self.iterationRowsTotal):
            self.resultsTableInGUI.item(row, col).setText('0')
        new_header = QtGui.QTableWidgetItem('Iteration %i' % self.numberOfIterations)
        self.resultsTableInGUI.setHorizontalHeaderItem(self.maxIterationColumns, new_header)

    def calculateCorrectionIteration(self):
        col = self.getIterationColumn()
        sensitivityMatrixToSave = self.updateSensitivityMatrixTable()
        inverseSensitivityMatrix = np.linalg.inv(sensitivityMatrixToSave)

        if self.correction_type == self.type44:
            currentTiltVector = np.array([self.resultsTableInGUI.item(x, col).text() for x in range(0, 4)], float)

            target_tilt_vector = np.array([
                float(self.Target_mu.text()),
                float(self.Target_mup.text()),
                float(self.Target_mu2.text()),
                float(self.Target_mup2.text()),
                ], float)
        elif self.correction_type == self.type22lin:
            currentTiltVector = np.array([self.resultsTableInGUI.item(x, col).text() for x in range(0, 2)], float)

            target_tilt_vector = np.array([
                float(self.Target_mu.text()),
                float(self.Target_mup.text()),
                ], float)
        elif self.correction_type == self.type22quad:
            currentTiltVector = np.array([self.resultsTableInGUI.item(x, col).text() for x in range(2, 4)], float)

            target_tilt_vector = np.array([
                float(self.Target_mu2.text()),
                float(self.Target_mup2.text()),
                ], float)
        else:
            raise ValueError('self.correction_type', self.correction_type)

        delta_tilt = target_tilt_vector - currentTiltVector

        deltaIList = np.dot(inverseSensitivityMatrix, delta_tilt)*self.correction_factor
        for ctr, deltaI in enumerate(deltaIList):
            row = self.iterationRowsDelta+ctr
            self.resultsTableInGUI.item(row, col).setText('%.2e' % deltaI)
        self.setStateButton(self.state_CORR)

    def correctIteration(self):
        col_old = self.getIterationColumn()

        for knob_ctr in range(self.nKnobs):
            deltaI = float(self.resultsTableInGUI.item(self.iterationRowsDelta + knob_ctr, col_old).text())
            current_old = self.get_current(knob_ctr)
            current_new = current_old + deltaI
            self.set_current(knob_ctr, current_new)
            print('\nknob_ctr, current_old, deltaI, self.get_current(knob_ctr)')
            print(knob_ctr, current_old, deltaI, self.get_current(knob_ctr))

        self.setIterationNumber()
        self.setStateButton(self.state_MEAS)

    def setStateButton(self, new_state):
        assert new_state in (self.state_CALC, self.state_CORR, self.state_MEAS)
        self.state = new_state
        self.StatusLabel.setText('Status:\n%s' % self.state)
        for button in self.CalculateButton, self.MeasureButton, self.CorrectButton:
            button.setStyleSheet('background-color:white')

        if new_state == self.state_CALC:
            self.CalculateButton.setStyleSheet('background-color:red')
        elif new_state == self.state_MEAS:
            self.MeasureButton.setStyleSheet('background-color:red')
        elif new_state == self.state_CORR:
            self.CorrectButton.setStyleSheet('background-color:red')

    def useCurrentTilt(self):
        col = self.getIterationColumn()
        tilt0, tiltp0, tilt20, tiltp20 = self.get_current_tilt()
        tilt0_err, tiltp0_err, tilt20_err, tiltp20_err = self.get_current_tilt_errors()
        self.resultsTableInGUI.item(0, col).setText('%.2e' % tilt0)
        self.resultsTableInGUI.item(1, col).setText('%.2e' % tiltp0)
        if self.second_order_tilt:
            self.resultsTableInGUI.item(2, col).setText('%.2e' % tilt20)
            self.resultsTableInGUI.item(3, col).setText('%.2e' % tiltp20)
        for knob_ctr in range(self.nKnobs):
            self.resultsTableInGUI.item(self.iterationRowsKnobs+knob_ctr, col).setText('%.2e' % self.get_current(knob_ctr))


            data_dictionary = {
                    'Meta_data': {
                        'tilt': [tilt0, tiltp0],
                        'tilt_err': [tilt0_err, tiltp0_err],
                        'tilt2': [tilt20, tiltp20],
                        'tilt2_err': [tilt20_err, tiltp20_err],
                        }
                    }

        self.add_to_plot_lists(data_dictionary)

        self.setStateButton(self.state_CALC)
        col = self.getIterationColumn()
        for ctr in range(self.nKnobs):
            row = self.iterationRowsDelta+ctr
            self.resultsTableInGUI.item(row, col).setText('0')

    def get_knob(self, knob_number):
        knob = self.knobTableInGUI.item(knob_number, 0)
        return knob

    def get_current(self, knob_number):
        knob = self.knob_pvs[knob_number]
        curr = caget(knob)
        self.knobTableInGUI.item(knob_number, 1).setText('%.2e' % curr)
        return curr

    def set_current(self, knob_number, curr):
        self.knobTableInGUI.item(knob_number, 2).setText('%.2e' % curr)

        knob = self.knob_pvs[knob_number]
        if not self.DryRun:
            # This should be the only place where caput is called in this file!
            caput(knob.replace("I-READ","I-SET"), curr)
            time.sleep(self.time_delay)
            curr_new = self.get_current(knob_number)
            print('Knob %i target: %f Is: %f' % (knob_number, curr, curr_new))
        else:
            print('Knob %i target: %f Is: %f (Dry run!)' % (knob_number, curr, curr))

    def get_knob_names(self):
        return [self.knobTableInGUI.item(i,0).text() for i in range(self.nKnobs)]

    def measureTilt(self, show_plot=True):
        if self.NoPlots:
            show_plot = False

        PM = self.ScreenGUI.text()
        Emit_data = EmitMeasToolCore.perform_meas_screen(
                self.location,
                self.MeasType,
                PM,
                self.energy_eV,
                self.PhaseAdvanceSteps,
                self.NumberImages,
                self.QuadNames,
                self.main.instance_config_update,
                EmittanceToolConfig.profile_monitor,
                dimension=self.dimension,
                dry_run=self.DryRun
                )

        Emit_data['Input'].update({
            'tilt_options': self.tilt_options,
            })

        meta_data = beamdynamics.analyzePyscanResult(Emit_data)
        Emit_data['Meta_data'] = meta_data

        if show_plot:
            plot_results.plot_all(Emit_data)

        if self.second_order_tilt:
            tilt2 = meta_data['tilt2']['tilt']
            tiltp2 = meta_data['tilt2']['tiltp']
            tilt2_err = meta_data['tilt2']['tilt_err']
            tiltp2_err = meta_data['tilt2']['tiltp_err']
        else:
            tilt2, tiltp2, tilt2_err, tiltp2_err = [0]*4
        tilt = meta_data['tilt']['tilt']
        tiltp = meta_data['tilt']['tiltp']
        tilt_err = meta_data['tilt']['tilt_err']
        tiltp_err = meta_data['tilt']['tiltp_err']

        self.set_current_tilt(tilt, tiltp, tilt_err, tiltp_err, tilt2, tiltp2, tilt2_err, tiltp2_err)

        for col_ctr, col in enumerate(range(self.iterationRowsTarget, self.iterationRowsTarget+self.nTargets)):
            self.LastMeasurement.item(0, col).setText('%.2e' % self.get_current(col_ctr))
        for col, val in zip(range(self.iterationRowsKnobs, self.iterationRowsKnobs+self.nKnobs), [tilt, tiltp, tilt2, tiltp2]):
            self.LastMeasurement.item(0, col).setText('%.2e' % val)

        for col in range(self.iterationRowsDelta):
            self.LastMeasurement.resizeColumnToContents(col)

        self.firstMeasurementDone = True

        # Possible to use "Save to Elog" button of the Main window
        self.main.Emit_data = Emit_data

        #eps_untilted = self.calculate_untilted_parameters(data_dictionary)
        #eps = data_dictionary['Meta_data']['emittances']['XY'.index(self.dimension)]
        #print('Emittance tilted and untilted:')
        #print(eps, eps_untilted)

        if self.DryRun:
            print('Dry run, not saving data.')
        else:
            # This should save data
            self.main.postMeasurement(Emit_data)

        return Emit_data

    def set_current_tilt(self, tilt, tiltp, tilt_err, tiltp_err, tilt2, tiltp2, tilt2_err, tiltp2_err):
        self.Current_mu.setText('%.2e' % tilt)
        self.Current_mup.setText('%.2e' % tiltp)
        self.Current_mu_err.setText('%.2e' % tilt_err)
        self.Current_mup_err.setText('%.2e' % tiltp_err)

        self.Current_mu2.setText('%.2e' % tilt2)
        self.Current_mup2.setText('%.2e' % tiltp2)
        self.Current_mu2_err.setText('%.2e' % tilt2_err)
        self.Current_mup2_err.setText('%.2e' % tiltp2_err)

    def get_current_tilt(self):
        return float(self.Current_mu.text()), float(self.Current_mup.text()), float(self.Current_mup2.text()), float(self.Current_mu2.text())

    def get_current_tilt_errors(self):
        return float(self.Current_mu_err.text()), float(self.Current_mup_err.text()), float(self.Current_mu2_err.text()), float(self.Current_mup2_err.text())

    def measureSensitivityMatrix(self):
        knobCurrentValues, deltaValues, knobFutureValues, knobNames = self.updateTable()

        if np.any(deltaValues == 0):
            print('Delta values:', deltaValues)
            raise ValueError('Delta values must not be 0.')

        data_dictionary0 = self.measureTilt()
        if self.second_order_tilt:
            tilt2_dict = data_dictionary0['Meta_data']['tilt2']
            tilt20, tiltp20 = tilt2_dict['tilt'], tilt2_dict['tiltp']
            tilt20_err, tiltp20_err = tilt2_dict['tilt_err'], tilt2_dict['tiltp_err']
        else:
            tilt20, tiltp20, tilt20_err, tiltp20_err = [0]*4
        tilt_dict = data_dictionary0['Meta_data']['tilt']
        tilt0, tiltp0 = tilt_dict['tilt'], tilt_dict['tiltp']
        tilt0_err, tiltp0_err = tilt_dict['tilt_err'], tilt_dict['tiltp_err']

        sensitivityMatrix = np.zeros((self.nTargets, self.nKnobs), float)
        sensitivityMatrixErrors = np.zeros_like(sensitivityMatrix)


        for row, col in itertools.product(range(4), range(4)):
            self.sensitivityTableInGUI.item(row,col).setText('0')
            self.sensitivityTableErrorsInGUI.item(row,col).setText('0')

        for knob_ctr, deltaValue in enumerate(deltaValues):
            # Put new quadrupole values, measure tilt, then restore old quad values and display old tilt as "current tilt"
            self.set_current(knob_ctr, knobFutureValues[knob_ctr]) # putting new quad values
            data_dictionary = self.measureTilt(show_plot=True)

            if self.second_order_tilt:
                tilt2_dict = data_dictionary['Meta_data']['tilt2']
                tilt2, tiltp2 = tilt2_dict['tilt'], tilt2_dict['tiltp']
                tilt2_err, tiltp2_err = tilt2_dict['tilt_err'], tilt2_dict['tiltp_err']
            else:
                tilt2, tiltp2, tilt2_err, tiltp2_err = [0.]*4
            tilt_dict = data_dictionary['Meta_data']['tilt']
            tilt, tiltp = tilt_dict['tilt'], tilt_dict['tiltp']
            tilt_err, tiltp_err = tilt_dict['tilt_err'], tilt_dict['tiltp_err']

            self.set_current(knob_ctr, knobCurrentValues[knob_ctr])
            self.set_current_tilt(tilt0, tiltp0, tilt0_err, tiltp0_err, tilt20, tiltp20, tilt20_err, tiltp20_err)

            val_tilt = (tilt - tilt0)/deltaValue
            val_tiltp = (tiltp - tiltp0)/deltaValue
            err_tilt = np.sqrt(tilt_err**2 + tilt0_err**2)/deltaValue
            err_tiltp = np.sqrt(tiltp_err**2 + tiltp0_err**2)/deltaValue

            if self.second_order_tilt:
                val_tilt2 = (tilt2 - tilt20)/deltaValue
                val_tilt2p = (tiltp2 - tiltp20)/deltaValue
                err_tilt2 = np.sqrt(tilt2_err**2 + tilt20_err**2)/deltaValue
                err_tilt2p = np.sqrt(tiltp2_err**2 + tiltp20_err**2)/deltaValue

            if self.correction_type in (self.type22lin, self.type44):
                sensitivityMatrix[0, knob_ctr] = val_tilt
                sensitivityMatrix[1, knob_ctr] = val_tiltp
                sensitivityMatrixErrors[0, knob_ctr] = err_tilt
                sensitivityMatrixErrors[1, knob_ctr] = err_tiltp

                if self.correction_type == self.type44:
                    sensitivityMatrix[2, knob_ctr] = val_tilt2
                    sensitivityMatrix[3, knob_ctr] = val_tilt2p
                    sensitivityMatrixErrors[2, knob_ctr] = err_tilt2
                    sensitivityMatrixErrors[3, knob_ctr] = err_tilt2p

            elif self.correction_type == self.type22quad:
                sensitivityMatrix[0, knob_ctr] = val_tilt2
                sensitivityMatrix[1, knob_ctr] = val_tilt2p
                sensitivityMatrixErrors[0, knob_ctr] = err_tilt2
                sensitivityMatrixErrors[1, knob_ctr] = err_tilt2p
            else:
                raise ValueError('Illegal self.correction_type: %s' % self.correction_type)

        print("\nsensitivityMatrix: ",sensitivityMatrix)

        for mat_row, gui_row in enumerate(range(len(sensitivityMatrix))):
            for mat_col, gui_col in enumerate(range(self.knob0, self.knob0+len(sensitivityMatrix[mat_row]))):
                self.sensitivityTableInGUI.item(gui_row,gui_col).setText('%.2e' % sensitivityMatrix[mat_row,mat_col])
                self.sensitivityTableErrorsInGUI.item(gui_row,gui_col).setText('%.2e' % sensitivityMatrixErrors[mat_row,mat_col])

        self.updateSensitivityMatrixTable()

    def updateTable(self):
        knobNames = self.get_knob_names()

        current_values_list = []
        delta_values_list = []
        for knob_ctr in range(self.nKnobs):
            knobcurrentValue = self.get_current(knob_ctr)
            current_values_list.append(knobcurrentValue)

            delta = float((self.knobTableInGUI.item(knob_ctr,3).text()))
            delta_values_list.append(delta)
        # Clear unused rows
        for knob_ctr in range(self.nKnobs,4):
            self.knobTableInGUI.item(knob_ctr,1).setText('0')
            self.knobTableInGUI.item(knob_ctr,2).setText('0')

        current_values_list = np.array(current_values_list, float)
        delta_values_list = np.array(delta_values_list, float)
        knobFutureValues = current_values_list + delta_values_list

        return current_values_list, delta_values_list, knobFutureValues, knobNames

    def updateSensitivityMatrixTable(self):

        sensitivityMatrixToSave = np.zeros((self.nKnobs, self.nKnobs))

        # Decide which items from the GUI table to use for the sensitivity matrix
        if self.correction_type == self.type44:
            range_row, range_col = range(4), range(4)
        elif self.correction_type == self.type22lin:
            range_row, range_col = range(2), range(2)
        elif self.correction_type == self.type22quad:
            range_row, range_col = range(2), range(2,4)

        for row_ctr, row in enumerate(range_row):
            for col_ctr, col in enumerate(range_col):
                sensitivityMatrixToSave[row_ctr, col_ctr] = float(self.sensitivityTableInGUI.item(row, col).text())

        self.updateResultsTable()
        print("\nsensitivityMatrix: ",sensitivityMatrixToSave)

        return sensitivityMatrixToSave

    def updateResultsTable(self):

        for ii in range(self.maxIterationColumns):
            self.resultsTableInGUI.resizeColumnToContents(ii)

    def add_to_plot_lists(self, result_dict):

        tilt2_dict = result_dict['Meta_data']['tilt2']
        tilt2, tiltp2 = tilt2_dict['tilt'], tilt2_dict['tiltp']
        tilt2_err, tiltp2_err = tilt2_dict['tilt_err'], tilt2_dict['tiltp_err']

        tilt_dict = result_dict['Meta_data']['tilt']
        tilt, tiltp = tilt_dict['tilt'], tilt_dict['tiltp']
        tilt_err, tiltp_err = tilt_dict['tilt_err'], tilt_dict['tiltp_err']

        self.plot_tilt.append(tilt)
        self.plot_tiltp.append(tiltp)
        self.plot_tilt_errors.append(tilt_err)
        self.plot_tiltp_errors.append(tiltp_err)

        self.plot_tilt2.append(tilt2)
        self.plot_tiltp2.append(tiltp2)
        self.plot_tilt2_errors.append(tilt2_err)
        self.plot_tiltp2_errors.append(tiltp2_err)

        for knob_number in range(self.nKnobs):
            current = self.get_current(knob_number)
            self.plot_currents[knob_number].append(current)

    def get_absolute_tilt(self, data_dictionary):
        pass

    def plot_results(self):
        if self.NoPlots:
            return

        fig = plt.figure(figsize=(14,12))
        plt.suptitle('At iteration %i' % self.numberOfIterations)

        sp_tilt = sp = plt.subplot(5,1,1)
        sp.grid(True)
        sp.set_title(r"Tilt $\mu$ and $\mu$'")
        sp.set_ylabel(r'$\mu$')

        sp_tiltp = sp = plt.subplot(5,1,2)
        sp.grid(True)
        sp.set_ylabel(r"$\mu'$")

        sp_tilt2 = sp = plt.subplot(5,1,3)
        sp.grid(True)
        sp.set_title(r"Tilt $\mu_2$ and $\mu_2$'")
        sp.set_ylabel(r"$\mu_2$")

        sp_tiltp2 = sp = plt.subplot(5,1,4)
        sp.grid(True)
        sp.set_ylabel(r"$\mu_2'$")

        xx = np.arange(len(self.plot_tilt))
        sp_tilt.errorbar(xx, self.plot_tilt, yerr=self.plot_tilt_errors, label=r'$\mu$', marker='o')
        sp_tiltp.errorbar(xx, self.plot_tiltp, yerr=self.plot_tiltp_errors, label=r"$\mu'$", marker='o')
        sp_tilt2.errorbar(xx, self.plot_tilt2, yerr=self.plot_tilt2_errors, label=r'$\mu_2$', marker='o')
        sp_tiltp2.errorbar(xx, self.plot_tiltp2, yerr=self.plot_tiltp2_errors, label=r"$\mu_2'$", marker='o')

        sp_tilt.ticklabel_format(style='sci', scilimits=(0,0),axis='y')
        sp_tiltp.ticklabel_format(style='sci', scilimits=(0,0),axis='y')
        sp_tilt2.ticklabel_format(style='sci', scilimits=(0,0),axis='y')
        sp_tiltp2.ticklabel_format(style='sci', scilimits=(0,0),axis='y')


        sp_current = sp = plt.subplot(5,1,5)
        sp_current.grid(True)
        sp.set_title('Currents I')
        sp.set_xlabel('Measurement count')
        sp.set_ylabel('Current [I]')

        for knob_number, yy in self.plot_currents.items():
            try:
                sp_current.plot(xx, yy, label='Knob %i' % knob_number, marker='o')
            except:
                print(xx, yy, knob_number)
                raise

        for sp_ in sp_tilt, sp_tilt2, sp_tiltp, sp_tiltp2, sp_current:
            sp_.set_xlim([xx[0]-1, xx[-1]+1])
            sp_.legend()

        fig.subplots_adjust(hspace=0.35)

        plt.show()

    def clearIterationTable(self):
        for row in range(self.iterationRowsTotal):
            for col in range(self.maxIterationColumns+1):
                self.resultsTableInGUI.item(row, col).setText('0')
        self.setIterationNumber(0)

    def ensureDirectory(self, filePath):
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory):
            os.makedirs(directory)

    #def calculate_untilted_parameters(self, data_dictionary):
    #    return np.nan
    #    beta, alpha = data_dictionary['Meta_data']['Optics_%s_meas' % self.dimension]
    #    eps = data_dictionary['Meta_data']['emittances']['XY'.index(self.dimension)]
    #    if self.second_order_tilt:
    #        mu, mup = data_dictionary['Meta_data']['tilt2']
    #    else:
    #        mu, mup = data_dictionary['Meta_data']['tilt']

    #    # Use arbitrary mu but correct by the streaked beam sizes
    #    # dx/dz == dx/dy * dy/dz
    #    # mu --> mu * (Dy)**2/(Dz)**2
    #    if self.dimension == 'X':
    #        #correction = np.mean(data_dictionary['Raw_data']['Vertical beam sizes'])
    #        print('Not implemented')
    #    elif self.dimension == 'Y':
    #        #correction = np.mean(data_dictionary['Raw_data']['Horizontal beam sizes'])
    #        print('Not implemented')
    #    correction = 1

    #    if self.DryRun:
    #        print('Using bogus numbers because of dryrun')
    #        eps = 1e-11
    #        beta, alpha = 50, 0.2
    #        correction = 1e-6

    #    try:
    #        gamma = (1+alpha**2)/beta

    #        mtilde = (gamma*mu**2 + beta*mup**2 + 2*alpha*mu*mup)/eps*correction**2
    #        print('Mtilde %.2e' % mtilde)
    #        eps_untilted = eps*np.sqrt(1-mtilde)
    #    except Exception as e:
    #        print(e)
    #        eps_untilted = 0.
    #    return eps_untilted

    def saveToFile(self):
        sensitivityMatrixToSave = self.updateSensitivityMatrixTable()

        dir_ = self.filePathGUI.toPlainText().strip()
        filename = self.fileNameGUI.toPlainText().strip()+'.h5'
        full_filename = os.path.join(dir_, filename)
        self.ensureDirectory(full_filename)
        print("path used for saving: %s" % full_filename)
        with h5py.File(full_filename, 'w') as hf:
            hf.create_dataset("SensitivityMatrix", data=sensitivityMatrixToSave)

        print("sensitivityMatrixToSave", sensitivityMatrixToSave)

    def loadFromFile(self):

        with h5py.File((str(self.filePathGUI.toPlainText())+'/'+str(self.fileNameGUI.toPlainText())+'.h5'), 'r') as hf:
            data = hf['SensitivityMatrix'][:]

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.sensitivityTableInGUI.item(i,j).setText('%.2e' % data[i][j])

        print("loaded data: ",data)

#############################################
if __name__ == "__main__":
    print('Start the emittance tool, not the coupling correction directly. Exit.')

