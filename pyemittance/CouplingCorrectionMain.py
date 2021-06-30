import os
import datetime
import h5py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from PyQt4 import QtGui
from PyQt4.uic import loadUiType

from epics import caget, caput

Ui_MainWindow, QMainWindow = loadUiType('CouplingCorrectionGUI.ui')

class startCouplingCorrectionWindow(QMainWindow, Ui_MainWindow): # class to start the application

    maxIterations = 4 # Dont change this value without also changing the UI
    nColumns = 4

    def __init__(self, EmitMeasTool, MeasLocation, MeasType, PM, Energy,PhaseAdvanceSteps, NumberImages, Coupling):
        super(startCouplingCorrectionWindow, self).__init__()
        self.setupUi(self)

        self.MeasLocation = MeasLocation
        self.EmitMeasTool = EmitMeasTool
        self.MeasType = MeasType
        self.PM = PM
        self.Energy = Energy
        self.PhaseAdvanceSteps = PhaseAdvanceSteps
        self.NumberImages = NumberImages
        self.Coupling = Coupling

        self.coup_xy = 0
        self.coup_xpy = 0
        self.coup_xyp = 0
        self.coup_xpyp = 0

        # SVD user defined percentage initial value
        #self.SVDpercentage=self.SVDpercentageGUI.text()
        self.SVDpercentage = self.getSVDpercentage()
        self.SVDpercentageGUI.editingFinished.connect(self.getSVDpercentage)

        now = datetime.datetime.now()
        self.filePathGUI.setText('/afs/psi.ch/intranet/SF/data/%i/%02i/%02i' % (now.year, now.month, now.day))

        # getting knob names and setting current values if something in the table is touched
        self.knobTableInGUI.currentItemChanged.connect(self.updateTable)
        self.sensitivityTableInGUI.currentItemChanged.connect(self.updateSensitivityMatrixTable)
        self.resultsTableInGUI.currentItemChanged.connect(self.updateResultsTable)

        # initially updating table values
        self.updateTable()
        self.updateSensitivityMatrixTable()
        self.updateResultsTable()

        # connect buttons to functions
        self.sensitivityMatrixButton.clicked.connect(self.calculateSensitivityMatrix)
        self.sensitivityMatrixButtonRow1.clicked.connect(self.sensitivityMatrixRow1)
        self.sensitivityMatrixButtonRow2.clicked.connect(self.sensitivityMatrixRow2)
        self.sensitivityMatrixButtonRow3.clicked.connect(self.sensitivityMatrixRow3)
        self.sensitivityMatrixButtonRow4.clicked.connect(self.sensitivityMatrixRow4)

        self.measureCouplingButton.clicked.connect(self.measureCouplingFunction)
        self.calculateCorrectionButton.clicked.connect(self.calculateCorrectionFunction)
        self.applyCorrectionButton.clicked.connect(self.applyCorrectionFunction)

        # save/load the sensitivity matrixfile
        self.saveSensitivityMatrixButton.clicked.connect(self.saveToFile)
        self.loadSensitivityMatrixButton.clicked.connect(self.loadFromFile)

        # number of itterations count
        self.numberOfItterations = 0

        # start btteration button to function
        self.startItterationButton.clicked.connect(self.startItteration)

        self.DryRunButton.toggled.connect(self.selectDryRun)
        self.selectDryRun()
        print('Warning: Override Dryrun to true')
        self.DryRun = True


        # making empty plots
        self.fig1 = plt.figure(facecolor='None')
        self.subplot1 = self.fig1.add_subplot(211)
        self.subplot2 = self.fig1.add_subplot(212)

        # plot variables
        self.y = []
        self.couplingConributionList = np.ones(4)*np.nan

        self.canvas = FigureCanvas(self.fig1)
        QtGui.QVBoxLayout(self.plot1inGUI).addWidget(self.canvas)
        self.nav = NavigationToolbar(self.canvas,self.frameForNavigationToolbar)

    def measureCouplingFunction(self):
        pass

    def calculateCorrectionFunction(self):
        pass

    def applyCorrectionFunction(self):
        pass

    def selectDryRun(self):
        self.DryRun = self.DryRunButton.isChecked()
        print('Dry run: %s' % self.DryRun)

    def getSVDpercentage(self):
        SVDpercentageTxt = self.SVDpercentageGUI.text()
        self.SVDpercentage = float(SVDpercentageTxt)/100.
        print("\nSVDpercentage: ",self.SVDpercentage*100," %")

    def startItteration(self):

        i = self.numberOfItterations
        print("i",i)
        sensitivityMatrixToSave = self.updateSensitivityMatrixTable()

        # QQ What about SVD?
        inverseSensitivityMatrix = np.linalg.inv(sensitivityMatrixToSave)
        print("\ninverseSensitivityMatrix: ", inverseSensitivityMatrix)

        defaultCouplingVector = [self.coup_xy, self.coup_xpy, self.coup_xyp, self.coup_xpyp]

        deltaIList = np.dot(inverseSensitivityMatrix,defaultCouplingVector)
        print("\ndeltaIList: ", deltaIList)

        # working with results table
        for ii in range(self.maxIterations):
            self.resultsTableInGUI.item(ii,i).setText(str('{:.4g}').format(defaultCouplingVector[ii]))
            self.resultsTableInGUI.item(self.maxIterations+ii,i).setText(str('{:.4g}').format(deltaIList[ii]))
            # applying correction
            self.knobTableInGUI.item(ii,2).setText(str('{:.4g}').format(deltaIList[ii]))

        # collect variables for the plot
        self.plot_xy = float(self.resultsTableInGUI.item(0,i).text())
        self.plot_xpy = float(self.resultsTableInGUI.item(1,i).text())
        self.plot_xyp = float(self.resultsTableInGUI.item(2,i).text())
        self.plot_xpyp = float(self.resultsTableInGUI.item(3,i).text())

        # plot 1
        self.subplot1.clear()
        self.subplot1.set_title("Coupling terms with different iterations",size=11)
        x1 = [1,2,3,4]
        xlabels1 = ["<xy>","<x'y>","<xy'>","<x'y'>"]

        self.y.append((self.plot_xy,self.plot_xpy,self.plot_xyp,self.plot_xpyp))

        for ii, style in zip(range(i+1), ['g*', 'b*', 'r*', 'k*',]):
            self.subplot1.plot(x1, self.y[ii], style, label="iteration %i" % (ii+1))

        self.subplot1.set_xticks(x1, minor=False)
        self.subplot1.set_xticklabels(xlabels1, fontdict=None, minor=False)
        self.subplot1.margins(0.2)
        self.subplot1.legend(loc="best",fontsize="smaller")
        self.canvas.draw()

        # plot 2
        self.subplot2.clear()
        self.subplot2.set_title("Coupling contribution depending on iteration",size=11)
        self.subplot2.set_xlabel('iteration number')
        self.subplot2.set_ylabel('percentage [%]')
        x2 = [1,2,3,4]
        xlabels2 = [1,2,3,4]
        self.subplot2.plot(x2,self.couplingConributionList,'g*',label="coupling contribution")
        self.subplot2.set_xticks(x2, minor=False)
        self.subplot2.set_xticklabels(xlabels2, fontdict=None, minor=False)
        self.subplot2.margins(0.2)
        self.subplot2.legend(loc="best",fontsize="smaller")
        self.canvas.draw()
        plt.tight_layout()

        self.updateResultsTable()

        # measure sigma matrix again
        # TODO uncomment (this comment is from Matas, I have uncommented the following line (Philipp))
        self.calculateSensitivityMatrix()

        i += 1
        self.numbeOfItterationsInGUI.setText(str(i))

        i %= 4
        self.numberOfItterations = i

    def sensitivityMatrixRow(self,rowNumberVariable):

        # calculate initial coupling values if there is none
        if self.coup_xy != 0 or self.coup_xpy != 0 or self.coup_xyp != 0 or self.coup_xpyp != 0:

            # first measurement on default values
            dataDictionary = self.PerformMeas()

            # putting default values
            self.coup_xy, self.coupxpy, self.coup_xyp, self.coup_xpyp = dataDictionary["poptCoupling"]

            # coupling contribution 1 iteration
            self.couplingConributionList[0] = dataDictionary["couplingContribution"]

        # second measurement
        knobCurrentValues,deltaValues,knobFutureValues,knobNames = self.updateTable()

        # putting new values to quads
        knobNamesToChange = knobNames[rowNumberVariable].replace("READ","SET")
        self.caput(knobNamesToChange,knobFutureValues[rowNumberVariable])

        dataDictionary = self.PerformMeas()

        # putting back initial values to quads
        self.caput(knobNamesToChange,knobCurrentValues[rowNumberVariable])

        # coupling contribution i iteration
        self.couplingConributionList[rowNumberVariable] = dataDictionary["couplingContribution"]

        coup_xy, coup_xpy, coup_xyp, coup_xpyp = dataDictionary["poptCoupling"]

        sensitivityRow = [(coup_xy-self.coup_xy)/deltaValues[rowNumberVariable], (coup_xpy-self.coup_xpy)/deltaValues[rowNumberVariable], (coup_xyp-self.coup_xyp)/deltaValues[rowNumberVariable], (coup_xpyp-self.coup_xpyp)/deltaValues[rowNumberVariable]]

        # putting values into the table
        for i in range(len(sensitivityRow)):
            self.sensitivityTableInGUI.item(rowNumberVariable,i).setText(str(sensitivityRow[i]))

    def PerformMeas(self):
        QuadNames = self.EmitMeasTool.MeasurementQuads[self.MeasLocation+'/'+self.MeasType]
        return self.EmitMeasTool.PerformMeas(self.MeasLocation, self.MeasType, self.PM, self.Energy,self.PhaseAdvanceSteps, self.NumberImages, self.Coupling, QuadNames, dry_run=self.DryRun)[0]['Coupling']

    def caput(self, *args, **kwargs):
        if self.DryRun:
            pass
        else:
            caput(*args, **kwargs)


    def sensitivityMatrixRow1(self):

        self.sensitivityMatrixRow(0)

    def sensitivityMatrixRow2(self):

        self.sensitivityMatrixRow(1)

    def sensitivityMatrixRow3(self):

        self.sensitivityMatrixRow(2)

    def sensitivityMatrixRow4(self):

        self.sensitivityMatrixRow(3)

    def calculateSensitivityMatrix(self):

        knobCurrentValues,deltaValues,knobFutureValues,knobNames = self.updateTable()

        print("returning current,delta,future,names: ",knobCurrentValues,deltaValues,knobFutureValues,knobNames)

        coup_xy = []
        coup_xpy = []
        coup_xyp = []
        coup_xpyp = []

        for i in range(5):
            if i > 0:
                j = i-1
                self.caput(knobNames[j].replace("READ","SET"),knobFutureValues[j]) # putting new quad values

                print("knobNames.replace: ",knobNames[j].replace("READ","SET"))
            dataDictionary = self.PerformMeas()

            coup_xy.append(dataDictionary["poptCoupling"][0])
            coup_xpy.append(dataDictionary["poptCoupling"][1])
            coup_xyp.append(dataDictionary["poptCoupling"][2])
            coup_xpyp.append(dataDictionary["poptCoupling"][3])

            # coupling contribution i iteration
            #j=i
            self.couplingConributionList = dataDictionary["couplingContribution"]

            if i > 0:
                j = i-1
                self.caput(knobNames[j].replace("READ","SET"),knobCurrentValues[j]) # putting old quad values

            print("MeasLocation",self.MeasLocation)

        sensitivityMatrix = [[(coup_xy[1]-coup_xy[0])/deltaValues[0], (coup_xpy[1]-coup_xpy[0])/deltaValues[0], (coup_xyp[1]-coup_xyp[0])/deltaValues[0], (coup_xpyp[1]-coup_xpyp[0])/deltaValues[0]],
                           [(coup_xy[2]-coup_xy[0])/deltaValues[1], (coup_xpy[2]-coup_xpy[0])/deltaValues[1], (coup_xyp[2]-coup_xyp[0])/deltaValues[1], (coup_xpyp[2]-coup_xpyp[0])/deltaValues[1]],
                           [(coup_xy[3]-coup_xy[0])/deltaValues[2], (coup_xpy[3]-coup_xpy[0])/deltaValues[2], (coup_xyp[3]-coup_xyp[0])/deltaValues[2], (coup_xpyp[3]-coup_xpyp[0])/deltaValues[2]],
                           [(coup_xy[4]-coup_xy[0])/deltaValues[3], (coup_xpy[4]-coup_xpy[0])/deltaValues[3], (coup_xyp[4]-coup_xyp[0])/deltaValues[3], (coup_xpyp[4]-coup_xpyp[0])/deltaValues[3]]]

        print("\nsensitivityMatrix: ",sensitivityMatrix)

        for i in range(len(sensitivityMatrix)):
            for j in range(len(sensitivityMatrix[0])):
                self.sensitivityTableInGUI.item(i,j).setText(str(sensitivityMatrix[i][j]))

        self.updateSensitivityMatrixTable()

        # putting default values
        self.coup_xy = coup_xy[0]
        self.coup_xpy = coup_xpy[0]
        self.coup_xyp = coup_xyp[0]
        self.coup_xpyp = coup_xpyp[0]

        #self.startItteration()

        print("coup_xy[0]: ",coup_xy[0],"; coup_xpy[0]: ",coup_xpy[0],"; coup_xyp[0]: ",coup_xyp[0],"; coup_xpyp[0]: ",coup_xpyp[0])

    def updateTable(self):
        # getting knob names
        knob1 = self.knobTableInGUI.item(0,0).text()
        knob2 = self.knobTableInGUI.item(1,0).text()
        knob3 = self.knobTableInGUI.item(2,0).text()
        knob4 = self.knobTableInGUI.item(3,0).text()
        knobNames = [knob1,knob2,knob3,knob4]
        self.knobTableInGUI.resizeColumnToContents(0)

        # setting knob values
        knob1currentValue = caget(knob1)
        self.knobTableInGUI.item(0,1).setText(str('{:.4g}').format(knob1currentValue))
        #try:
        #    self.knobTableInGUI.item(0,1).setText(str('{:.4g}').format(knob1currentValue))
        #except:
        #    from PyQt4.QtCore import pyqtRemoveInputHook
        #    from pdb import set_trace
        #    pyqtRemoveInputHook()
        #    set_trace()


        knob2currentValue = caget(knob2)
        self.knobTableInGUI.item(1,1).setText(str('{:.4g}').format(knob2currentValue))

        knob3currentValue = caget(knob3)
        self.knobTableInGUI.item(2,1).setText(str('{:.4g}').format(knob3currentValue))

        knob4currentValue = caget(knob4)
        self.knobTableInGUI.item(3,1).setText(str('{:.4g}').format(knob4currentValue))

        knobCurrentValues = [knob1currentValue,knob2currentValue,knob3currentValue,knob4currentValue]
        self.knobTableInGUI.resizeColumnToContents(1)

        # setting delta change values
        delta1 = float((self.knobTableInGUI.item(0,2).text()))
        delta2 = float((self.knobTableInGUI.item(1,2).text()))
        delta3 = float((self.knobTableInGUI.item(2,2).text()))
        delta4 = float((self.knobTableInGUI.item(3,2).text()))
        deltaValues = [delta1, delta2, delta3, delta4]
        self.knobTableInGUI.resizeColumnToContents(2)

        # future knob values
        knob1futureValue = float(knob1currentValue) + delta1
        knob2futureValue = float(knob2currentValue) + delta2
        knob3futureValue = float(knob3currentValue) + delta3
        knob4futureValue = float(knob4currentValue) + delta4
        knobFutureValues = [knob1futureValue,knob2futureValue,knob3futureValue,knob4futureValue]

        return knobCurrentValues,deltaValues,knobFutureValues,knobNames

    def updateSensitivityMatrixTable(self):

        sensitivityMatrixToSave = np.zeros((4,4))
        for row in range(4):
            for col in range(4):
                sensitivityMatrixToSave[row, col] = float(self.sensitivityTableInGUI.item(row, col).text())

        self.updateResultsTable()
        print("\nsensitivityMatrix: ",sensitivityMatrixToSave)

        return sensitivityMatrixToSave

    def updateResultsTable(self):

        for ii in range(self.nColumns):
            self.resultsTableInGUI.resizeColumnToContents(ii)

    def ensureDirectory(self,filePath):
        directory = os.path.dirname(filePath)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def saveToFile(self):
        # QQ This always overwrites the same h5 for one day!

        sensitivityMatrixToSave = self.updateSensitivityMatrixTable()

        self.ensureDirectory((self.filePathGUI.toPlainText()+'/'+self.fileNameGUI.toPlainText()+'.h5'))
        print("\npath used for saving: ",(self.filePathGUI.toPlainText()+'/'+self.fileNameGUI.toPlainText()+'.h5'))
        with h5py.File((self.filePathGUI.toPlainText()+'/'+self.fileNameGUI.toPlainText()+'.h5'), 'w') as hf:
            hf.create_dataset("SensitivityMatrix", data=sensitivityMatrixToSave)

        print("sensitivityMatrixToSave", sensitivityMatrixToSave)

    def loadFromFile(self):

        with h5py.File((str(self.filePathGUI.toPlainText())+'/'+str(self.fileNameGUI.toPlainText())+'.h5'), 'r') as hf:
            data = hf['SensitivityMatrix'][:]

        for i in range(len(data)):
            for j in range(len(data[0])):
                self.sensitivityTableInGUI.item(i,j).setText(str(data[i][j]))

        print("loaded data: ",data)


#############################################
if __name__ == "__main__":
    print('Start the emittance tool, not the coupling correction directly')
    #app = QtGui.QApplication(sys.argv)
    #myapp = startCouplingCorrectionWindow()
    #myapp.show()
    #app.exec_()

