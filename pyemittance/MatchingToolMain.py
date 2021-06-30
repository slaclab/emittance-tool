import sys
import logging
from PyQt4 import QtGui
from PyQt4.uic import loadUiType
import matplotlib.pyplot as plt
import numpy as np

from epics import caget

from OMMadx2020 import MadX
import EmittanceToolConfig
from EmitMeasToolCore import EC, SF, EM, SM


madx_local = MadX(42)

Ui_MatchWindow, QMatchWindow = loadUiType('MatchingToolGUI.ui')

# To obtain debug messages from the madx module.
do_logging = False

if do_logging:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

def printOptics(Emit_data, print_=True):
    if Emit_data is None:
        print("No measurement was done. Cannot prinout!")
        return

    string = ''

    md = Emit_data['Meta_data']

    string += '\nMeasured projected optics Beta\tAlpha\tEmittance\n'
    for dim in ['X', 'Y']:
        try:
            proj_dict = md['proj_emittance_%s' % dim]
            string += '%s:\t%.4f m\t%.4f\t%.4f nm\n' % (dim, proj_dict['beta'], proj_dict['alpha'], proj_dict['normalized_emittance']*1e9)
        except KeyError:
            pass

    added_slice_title = False
    for dim in ['X', 'Y']:
        try:
            slice_dict = md['slice_emittance_%s' % dim]

            if not added_slice_title:
                string += '\nMeasured slice optics Beta\tAlpha\tEmittance\n'
                added_slice_title = True

            beta_arr, alpha_arr, emit_arr = slice_dict['beta'], slice_dict['alpha'], slice_dict['normalized_emittance']
            for slice_ctr, (beta, alpha, emit) in enumerate(zip(beta_arr, alpha_arr, emit_arr)):
                string += 'Slice %i:\t%.4f m\t%.4f\t%.4f nm\n' % (slice_ctr, beta, alpha, emit*1e9)
        except KeyError:
            pass

    if print_:
        print(string)
    return string

class StartMatch(QMatchWindow, Ui_MatchWindow):

    methods = ['LMDIF', 'SIMPLEX']
    limit_current_dict = {'LMDIF': True, 'SIMPLEX': False}

    def __init__(self, SM, Emit_data, Location, measType, bxM, axM, byM, ayM):
        super(StartMatch, self).__init__()
        self.setupUi(self)

        self.CalcMatching.clicked.connect(self.evCalcMatching)
        self.DoMatching.clicked.connect(self.evDoMatching)
        self.Restore.clicked.connect(self.evRestore)
        self.PrintOptics.clicked.connect(self.printOptics)
        self.SM = SM
        self.Emit_data = Emit_data

        self.Location = Location
        self.BxM.setText("%f" % bxM)
        self.AxM.setText("%f" % axM)
        self.ByM.setText("%f" % byM)
        self.AyM.setText("%f" % ayM)
        self.BxD.setText("%f" % EmittanceToolConfig.bxD[Location+'/'+measType])
        self.AxD.setText("%f" % EmittanceToolConfig.axD[Location+'/'+measType])
        self.ByD.setText("%f" % EmittanceToolConfig.byD[Location+'/'+measType])
        self.AyD.setText("%f" % EmittanceToolConfig.ayD[Location+'/'+measType])
        self.MatchingPoint.setText(EmittanceToolConfig.RP[Location+'/'+measType][0])

        self.quads = EmittanceToolConfig.MatchingQuads[self.Location]
        self.updateQuads()

        for method in self.methods:
            self.MadxMethodGUI.addItem(method)

        self.QuadIM = None
        self.QuadIP = None

    @property
    def DryRun(self):
        return self.DryRunButton.isChecked()

    @property
    def madx_method(self):
        return self.MadxMethodGUI.currentText()

    def printOptics(self):
        return printOptics(self.Emit_data)

    def updateQuads(self):
        # writing the matching quads and their initial current
        quads = self.quads
        quadsIch = []
        quadsKL = []
        for i in range(0,len(quads)):
            quadsIch.append(quads[i].replace('.','-')+':I-SET')

        QuadI = []
        for quad in quads:
            QuadI.append(caget(quad.replace('.','-')+':I-READ'))

        energies = [caget(q.replace('.','-')+':ENERGY-OP') for q in quads]
        quadsKL = self.SM.QuadrupoleI2KL(quads,QuadI,energies)

        for i in range(0,len(quads)):
            self.MQ.setItem(i,0,QtGui.QTableWidgetItem())
            self.MQ.item(i,0).setText(quads[i])
            self.MQ.setItem(i,1,QtGui.QTableWidgetItem())
            self.MQ.item(i,1).setText(str(round(quadsKL[i],6)))
            self.MQ.resizeColumnToContents(0)

    def evCalcMatching(self):
        iniKL = []
        quads = self.quads
        for i in range(0,len(quads)):
            iniKL.append(float(self.MQ.item(i,1).text()))

        bxm = float(str(self.BxM.text()))
        bym = float(str(self.ByM.text()))

        if bxm <= 0 or bym <= 0:
            raise ValueError('Measured betaX or betaY must be positive!')

        self.QuadIP, self.QuadIM = calcMatching(
                quads,
                float(str(self.BxM.text())),
                float(str(self.AxM.text())),
                float(str(self.ByM.text())),
                float(str(self.AyM.text())),
                float(str(self.BxD.text())),
                float(str(self.AxD.text())),
                float(str(self.ByD.text())),
                float(str(self.AyD.text())),
                str(self.MatchingPoint.text()),
                iniKL,
                self.limit_current_dict[self.madx_method],
                self.madx_method)


    def evDoMatching(self):

        if not self.DryRun and self.Emit_data is None:
            print("No measurement was done. Cannot match!")
            return

        # set calculated currents to matching quadrupoles (cycling is missing!)

        if self.QuadIP is None:
            print('Must calculate matching first!')
            return

        quads = self.quads

        QuadIPch = []
        for i in range(0, len(quads)):
            QuadIPch.append(quads[i].replace('.', '-') + ':I-SET')

        if self.DryRun:
            print('I would set these quads:')
            print(QuadIPch)
            print(self.QuadIP)
        else:
            EC.addGroup('QuadIP', QuadIPch)
            EC.put('QuadIP', self.QuadIP)
            EC.cafe.groupClose('QuadIP')

    def evRestore(self):
        if self.QuadIM is None:
            print('Nothing to restore')
            return
        quads = self.quads

        QuadIMch = []
        for i in range(0, len(quads)):
            QuadIMch.append(quads[i].replace('.', '-') + ':I-SET')

        if self.DryRun:
            print('I would set these quads:')
            print(QuadIMch)
            print(self.QuadIM)
        else:
            EC.addGroup('QuadIM', QuadIMch)
            EC.put('QuadIM', self.QuadIM)
            EC.cafe.groupClose('QuadIM')

def calcMatching(quads, bxM, axM, byM, ayM, bxD, axD, byD, ayD, RP, iniKL, limit_current, madx_method, show_plot=True):
    # calculate matching

    #print(quads)

    indict = {}
    indict['Direction'] = -1
    indict['Start'] = quads[0] + '$START'
    indict['InitialElement'] = quads[0]
#        indict['InitialEnergy'] = 0
#        indict['InitialEnergyValue'] = Energy
    indict['End'] = RP + '$START'
    indict['InitialCondition'] = [bxM, axM, byM, ayM]
    indict['Log'] = 0
#        indict['EnergyFromMachine'] = 0
#        indict['EnergyFromLayout'] = 0

    # getting undulator modules K
    #success = 0
    #while not success:
    #    success = madx.updateAramisUndulatorfromEpics(EC,self.SM,SF,EM,1)

    #Und = SF.getElement('SINLH02.UIND230')
    #print('undulator k-value:', Und.K)

    EM.updateEnergyFromEpics(SF,EC) # new sept. 18
    madx_local.updateBendAngleFromEpics(EC,SM,SF,EM,1)
    madx_local.updateQuadKfromEpics(EC,SM,SF,EM,1)

    energy_quad = []
    for q in quads:
        #print(q,EM.EnergyAt(q))
        #energy_quad.append(EM.EnergyAt(q))
        energy_quad.append(caget(q.replace('.','-')+':ENERGY-OP'))

    # print (Und.K)
    #dipo1 = SF.getElement('SINBC02.MBND100')
    #dipo2 = SF.getElement('SINBC02.MBND200')
    #dipo3 = SF.getElement('SINBC02.MBND300')
    #dipo4 = SF.getElement('SINBC02.MBND400')

    #print(dipo1.angle)
    #print(dipo2.angle)
    #print(dipo3.angle)
    #print(dipo4.angle)
    #print(dipo1.design_angle)

    # backpropagate measured optics
    twiss = madx_local.getPropagation(SF, EM, EC, SM, indict)

    NameM = []
    SM2 = []
    BetaxM = []
    BetayM = []
    AlphaxM = []
    AlphayM = []
    k1LM = []
    totk1LP = []
    angle = []
    for n in twiss.NAME:
        if 'DRIFT' not in n:
            NameM.append(twiss.NAME[twiss.indx[n]])
            SM2.append(twiss.S[twiss.indx[n]])
            BetaxM.append(twiss.BETX[twiss.indx[n]])
            BetayM.append(twiss.BETY[twiss.indx[n]])
            AlphaxM.append(twiss.ALFX[twiss.indx[n]])
            AlphayM.append(twiss.ALFY[twiss.indx[n]])
            totk1LP.append(twiss.K1L[twiss.indx[n]])
            angle.append(twiss.ANGLE[twiss.indx[n]])

    # getting the kl value of the matching quads
    for q in quads:
        ele = SF.getElement(q)
        if 'corx' in ele.__dict__:
            n = q + '.Q1'
            Qmult = 2.0
        else:
            n = q
            Qmult = 1.0
        k1LM.append(Qmult * twiss.K1L[twiss.indx[n]])

    #print(k1LM)

    # calculate matching
    indict2 = {}
    indict2['Direction'] = 1
    indict2['Start'] = quads[0] + '$START'
    indict2['InitialElement'] = quads[0]
#        indict2['InitialEnergy'] = 1
#        indict2['InitialEnergyValue'] = Energy
    indict2['End'] = RP + '$START'
    indict2['InitialCondition'] = [BetaxM[-1], -AlphaxM[-1], BetayM[-1], -AlphayM[-1]]
    indict2['Log'] = 0
#        indict2['EnergyFromMachine'] = 0
    indict2['QuadKnobs'] = quads
    indict2['Constraints'] = ['betx=%f' % bxD, 'bety=%f' % byD, 'alfx=%f' % axD, 'alfy=%f' % ayD, 'x=0', 'y=0']
    indict2['TargetLocation'] = RP + '$START'
    indict2['DeviceName'] = quads
    indict2['Parameter'] = iniKL
    #print(quads, iniKL)

    #print([BetaxM[-1], -AlphaxM[-1], BetayM[-1], -AlphayM[-1]])

    [twiss2, QuadMatchKL] = madx_local.getMatching(SF, EM, EC, SM, indict2, limit_current=limit_current, method=madx_method)
    # In case you want to do just propagation again
    # twiss2 = madx.getPropagation(SF,EM,EC,SM,indict2)
    # QuadMatchKL = [0.0,0.0,0.0,0.0,0.0]

    # print ('Energy',EM.EnergyAt('SINLH01.MQUA020'))

    NameP = []
    SP = []
    BetaxP = []
    BetayP = []
    AlphaxP = []
    AlphayP = []
    k1LP = []
    totk1LM = []
    for n in twiss2.NAME:
        if 'DRIFT' not in n:
            NameP.append(twiss2.NAME[twiss2.indx[n]])
            SP.append(twiss2.S[twiss2.indx[n]])
            BetaxP.append(twiss2.BETX[twiss2.indx[n]])
            BetayP.append(twiss2.BETY[twiss2.indx[n]])
            AlphaxP.append(twiss2.ALFX[twiss2.indx[n]])
            AlphayP.append(twiss2.ALFY[twiss2.indx[n]])
            totk1LM.append(twiss2.K1L[twiss2.indx[n]])

        if 'SATDI01.MQUA250$START' in n:
            print('SATDI01.MQUA250$START')
            print('betax', BetaxP[-1])
            print('alphax', AlphaxP[-1])
            print('betay', BetayP[-1])
            print('alphay', AlphayP[-1])


    # print(totk1LP, totk1LM)
    # print(NameM, NameP)

    # getting the kl value of the matching quads
    for q in quads:
        ele = SF.getElement(q)
        if 'corx' in ele.__dict__:
            n = q + '.Q1'
            Qmult = 2.0
        else:
            n = q
            Qmult = 1.0
        k1LP.append(Qmult * twiss2.K1L[twiss2.indx[n]])

    #print(QuadMatchKL)
    #print(k1LP)
    #print(k1LM)
    # getting the predicted optics at the reconstruction point
    bxP = twiss2.BETX[twiss2.indx[RP + '$START']]
    axP = twiss2.ALFX[twiss2.indx[RP + '$START']]
    byP = twiss2.BETY[twiss2.indx[RP + '$START']]
    ayP = twiss2.ALFY[twiss2.indx[RP + '$START']]

    # getting the right direction for SM
    smax = max(SM2)
    SM2 = smax - np.array(SM2) + SP[0]

    # get currents
    QuadIP, QuadIM = [], []
    for q_ctr, q in enumerate(quads):
        QuadIP.append(SM.QuadrupoleKL2I([q], [k1LP[q_ctr]], energy_quad[q_ctr])[0])
        QuadIM.append(SM.QuadrupoleKL2I([q], [k1LM[q_ctr]], energy_quad[q_ctr])[0])


    # calculation of mismatch parameters
    gxD = (1 + axD * axD) / bxD
    gyD = (1 + ayD * ayD) / byD

    gxM = (1 + axM * axM) / bxM
    gyM = (1 + ayM * ayM) / byM

    gxP = (1 + axP * axP) / bxP
    gyP = (1 + ayP * ayP) / byP

    MxM = 0.5 * (bxM * gxD - 2 * axM * axD + gxM * bxD)
    MyM = 0.5 * (byM * gyD - 2 * ayM * ayD + gyM * byD)

    MxP = 0.5 * (bxP * gxD - 2 * axP * axD + gxP * bxD)
    MyP = 0.5 * (byP * gyD - 2 * ayP * ayD + gyP * byD)

    #print(MxM, MyM)
    #print(MxP, MyP)

    #print(quads)
    #print(bxM, axM, byM, ayM, bxD, axD, byD, ayD)
    #print(RP)
    #print(iniKL)

    #bending = SF.getElement('SINBC02.MBND100')
    #print(bending['angle'])

    #print([BetaxM[-1], -AlphaxM[-1], BetayM[-1], -AlphayM[-1]])



    # plotting
    if show_plot:
        plt.figure(figsize=(15, 10))
        plt.subplot(3, 1, 1)
        plt.hold(True)
        plt.plot(SM2, BetaxM, '.b-', label='Measurement, Mx = ' + str(round(MxM, 2)))
        plt.plot(SP, BetaxP, '*r-', label='Prediction, Mx = ' + str(round(MxP, 2)))
        # plt.plot(SM2,totk1LP,'*r-', label = 'Prediction, Mx = ' + str(round(MxP,2)))
        plt.xlabel('s(m)')
        plt.ylabel('Beta X (m)')
        plt.legend(loc='best')

        plt.subplot(3, 1, 2)
        plt.hold(True)
        plt.plot(SM2, BetayM, '.b-', label='Measurement, My = ' + str(round(MyM, 2)))
        plt.plot(SP, BetayP, '*r-', label='Prediction, My = ' + str(round(MyP, 2)))
        plt.xlabel('s(m)')
        plt.ylabel('Beta Y (m)')
        plt.legend(loc='best')

        y_pos = np.arange(len(QuadIM))
        plt.subplot(3, 1, 3)
        plt.hold(True)
        plt.bar(y_pos - 0.2, QuadIM, 0.38, align='center', color='b', label='Present values')
        plt.bar(y_pos + 0.2, QuadIP, 0.38, align='center', color='r', label='New values')
        plt.xticks(y_pos, quads)
        plt.legend(loc='best')
        plt.ylabel('Current (A)')


        plt.show()

    return QuadIP, QuadIM


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle('cleanlooks')
    if len(sys.argv) > 1:
        prefix = sys.argv[1]
    else:
        prefix = ''
    myapp = StartMatch(prefix)
    myapp.show()
    sys.exit(app.exec_())

