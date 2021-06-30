import math
from OMAppTemplate import ApplicationTemplate
from epics import caget
import numpy as np

#--------
# Energy Manager Interface

class EnergyManager(ApplicationTemplate):
    def __init__(self):
        ApplicationTemplate.__init__(self)
        self.p0=0
        self.p=0
        self.Energy={}


    def update(self,p0):
        self.p0=p0


    def writeLine(self,line,seq):

        'Nothing to do?'


    def register(self,ele,Egain=0.0):
        if (self.MapIndx!=self.MapIndxSave): # New line comes
            self.p=0
            self.MapIndxSave=self.MapIndx
        self.Energy[ele.Name]=[self.p,Egain]
        if ('cor' in ele.__dict__) or ('corx' in ele.__dict__):
            name=ele.Name.replace('MQUA','MCRX').replace('MBND','MCRX').replace('UIND','MCRX').replace('MCOR','MCRX')
            self.Energy[name]=[self.p,Egain]
        if 'cory' in ele.__dict__:
            name=ele.Name.replace('MQUA','MCRY').replace('MBND','MCRY').replace('UIND','MCRY').replace('MCOR','MCRY')
            self.Energy[name]=[self.p,Egain]

            # Double registration for later convenience
            # ... 07.08.2015 Removed. After gaining some experience, it turns out inconvenient rather than useful.
            #self.Energy[EpicsName]=[self.p,Egain]

        return


    def writeVacuum(self,ele):
        self.writeMarker(ele)
        return

    def writeAlignment(self,ele):
        self.writeMarker(ele)
        return


    def writeBend(self,ele):
        # Here, it is possible to implement Egain (loss) from CSR
        # EgainCSR=***
        # self.Energy[ele.Name]=[self.p,EgainCSR]
        self.register(ele)

    def writeQuadrupole(self,ele):
        self.register(ele)

    def writeCorrector(self,ele):
        self.register(ele)

    def writeSextupole(self,ele):
        self.register(ele)

    def writeRF(self,ele):
        if (self.MapIndx!=self.MapIndxSave): # New line comes
            self.p=0
            self.MapIndxSave=self.MapIndx
        if ('Gradient' in ele.__dict__) and ('Phase' in ele.__dict__):   # needs a check for TDS to not give energy gain
            if 'TDS' in ele.Name:
                Egain=0.0
            else:
                E=ele.Gradient
                V=E*ele.Length
                phase=ele.Phase*math.pi/180.0
                Egain=V*math.sin(phase)
        else:
            Egain=0.0
        self.Energy[ele.Name]=[self.p,Egain,ele.Length]
        self.p=self.p+Egain
        #print('WriteRF', ele.Name, Egain/1e6)
        #import pdb; pdb.set_trace()

    def writeUndulator(self,ele):
        self.register(ele)

    def writeDiagnostic(self,ele):
        self.register(ele)

    def writeSolenoid(self,ele):
        self.register(ele)

    def writeMarker(self,ele):
        self.register(ele)


    def updateEnergyFromEpics(self,SF=None,EC=None,PhaseOffset=None,inCallBack=0,GunNominal=1):
        # Used in Virtual Accelerator but general function
        if not SF:  # FacilityContainer instance
            raise ValueError('Need SF')
        if not EC:  # EpicsChannel
            raise ValueError('Need EC')


        #dn,Phase=EC.get('RF:PHASE') # Assuming that the PHASE-ONCREST is mesaured and set
        #dn,Gradient=EC.get('RF:GRADIENT')

        dn=EC.getDeviceList('RF')

        # Philipp Dijkstal Sep 2020: I removed inCallBack stuff

        #if inCallBack==1: # Note that "get" does not work in callbacks...
        #    klystron=EC.getDeviceList('RFsystem')

        #    Status,s,sl=EC.cafe.getGroupCache('RFsystem:GET-RF-READY-STATUS',dt='int')
        #    Mode,s,sl=EC.cafe.getGroupCache('RFsystem:GET-STATION-MODE')
        #    State,s,sl=EC.cafe.getGroupCache('RFsystem:GET-STATION-STATE')

        #    V,s,sl=EC.cafe.getGroupCache('RFsystem:SET-ACC-VOLT')
        #    KPhase,s,sl=EC.cafe.getGroupCache('RFsystem:SET-VSUM-PHASE')
        #    KPhaseB,s,sl=EC.cafe.getGroupCache('RFsystem:SET-BEAM-PHASE')
        #elif inCallBack==2: # Monitor is assigned to individual channel...
        #    klystron=EC.getDeviceList('RFsystem')

        #    Status=[]
        #    Mode=[]
        #    State=[]
        #    V=[]
        #    KPhase=[]
        #    KPhaseB=[]
        #    for r in klystron:
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':GET-RF-READY-STATUS',dt='int')
        #        Status.append(c.value[0])
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':GET-STATION-MODE')
        #        Mode.append(c.value[0])
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':GET-STATION-STATE')
        #        State.append(c.value[0])
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':SET-ACC-VOLT')
        #        V.append(c.value[0])
        #        if 'S10CB02' in r:
        #            print('Voltage in OMEnergy',c.value[0])
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':SET-VSUM-PHASE')
        #        KPhase.append(c.value[0])
        #        c=EC.cafe.getPVCache(EC.prefix+r.replace('.','-')+':SET-BEAM-PHASE')
        #        KPhaseB.append(c.value[0])


        klystron,Status=EC.get('RFsystem:GET-RF-READY-STATUS',0,'int')
        klystron,Mode=EC.get('RFsystem:GET-STATION-MODE')
        #klystron,State=EC.get('RFsystem:GET-STATION-STATE') # does not work any more
        # fix it like this :(
        State = []
        for kly in klystron:
            if kly.startswith('SATCB') or kly.startswith('SATXB'):
                State.append('OFF')
                print('Warning, setting %s to OFF' % kly)
            else:
                pv = kly.replace('.', '-').replace('RSYS', 'RMSM') + ':SM-GET'
                State.append(caget(pv, as_string=True))


        klystron,V=EC.get('RFsystem:SET-ACC-VOLT')
        klystron,KPhase=EC.get('RFsystem:SET-VSUM-PHASE')
        #klystron,KPhaseON=EC.get('RFsystem:ON-CREST-VSUM-PHASE')
        klystron,KPhaseB=EC.get('RFsystem:SET-BEAM-PHASE')

        # Check if the rf stations are in operation
        kok={}
        for i in range(0,len(klystron)):
            sec=klystron[i].split('.')[0]
            ele=SF.getElement(EC.Cavities[klystron[i]][2])
            if State[i] in ['RF ON','RF ON PHAFB','RF ON AMPFB','RF ON FB','MPS DELAY', 'RF on beam']:
                State[i]='RF ON'
            if Mode[i]=='CONDITIONING':
                Mode[i]='NORMAL'
            if Mode[i]=='NORMAL' and State[i]=='RF ON' and Status[i]:
                #kok[sec]=[V[i]/(len(EC.Cavities[klystron[i]])-2)/ele.Length,KPhase[i],KPhaseON[i],KPhaseB[i]]

                if PhaseOffset:
                    kok[sec]=[V[i]/(len(EC.Cavities[klystron[i]])-2)/ele.Length,KPhase[i],KPhaseB[i],PhaseOffset[i]]
                else:
                    kok[sec]=[V[i]/(len(EC.Cavities[klystron[i]])-2)/ele.Length,KPhase[i],KPhaseB[i],0]
            else:

                if PhaseOffset:
                    #kok[sec]=[0,KPhase[i],KPhaseON[i],KPhaseB[i]]
                    kok[sec]=[0,KPhase[i],KPhaseB[i],PhaseOffset[i]]
                else:
                    kok[sec]=[0,KPhase[i],KPhaseB[i],0]

        # RF:PHASE and RF:GRADIENT should be constructed from RFsystem:**-PHASE and RFsystem:**-VOLT/POWER in Virtual accelerator
        # This is not yet done. Taking into account calibration constants is not straightforward, and SET-ACC-VOLT is used for both real and virtual machine at this moment. 2016.06.24


        Phase=[0]*len(dn)
        #PhaseON=[0]*len(dn)
        PhaseB=[0]*len(dn)
        PhaseOffsetRF=[0]*len(dn)
        Gradient=[0]*len(dn)
        for i in range(0,len(dn)):
            sec=dn[i].split('.')[0]
            Gradient[i]=kok[sec][0]
            Phase[i]=kok[sec][1]
            #PhaseON[i]=kok[sec][2]
            #PhaseB[i]=kok[sec][3]
            PhaseB[i]=kok[sec][2]
            PhaseOffsetRF[i]=kok[sec][3]

        if PhaseOffset:
            # For virtual accelerator, where PHASE-ONCREST is known exactly

            # First, find the phase delay dut to BC
            # assuming that the BC mechanical angle is adjusted for the right beam energy.
            # Otherwise, it is necessary to compute the beam energy several times:
            # compute the beam energy at the first bc, compute the phase delay and then recompute the beam energy taking into account the phase delay...
            delay=[]
            for bc in SF.BC:
                if isinstance(bc[-1],float) and ('SAR' not in bc[0].Name) and ('SAT' not in bc[0].Name):
                    hName=bc[0].Name.split('.')[0]
                    if 'BC' in hName:
                        hName=hName+'.BC'
                    elif 'LH' in hName:
                        hName=hName+'.LH'
                    chicane,val=EC.get(hName)
                    pos=val[1]
                    anglerad=math.atan(pos/1000/bc[4])
                    dL=2*bc[4]*(1.0/math.cos(anglerad)-1.0)
                    delay.append([bc[0].Name,dL])

            dph=[0]*len(dn)
            for i in range(0,len(dn)):
                for d in delay:
                    if SF.isUpstream(d[0],dn[i]):
                        ele=SF.getElement(dn[i]) # RF element
                        dph[i]=dph[i]+360*ele.Frequency*d[1]/3e8 # in units of degree

            # The on-crest phase is just a soft channel to connect KPhaseB and KPhase: KPhaseB=KPhase-KPhaseON+90
            # Therefore the 'real' beam phase is determined independently from KPhaseON.
            PhaseBeam=(np.array(Phase)+np.array(dph)-np.array(PhaseOffsetRF))+90
        else:
            # Otherwise (Energy manager in the operation) it should be from RFsystem:GET-BEAM-PHASE with Energy daemon running
            PhaseBeam=PhaseB

        #print('=======',PhaseB)
        for i in range(0,len(PhaseB)):
            if PhaseB[i] is None:
                PhaseB[i]=0
        for i in range(0,len(Gradient)):
            if Gradient[i] is None:
                Gradient[i]=0

        SF.setGroup(dn,'Phase',PhaseBeam)
        SF.setGroup(dn,'Gradient',Gradient)
        #print('[[[[[[[[[[[]]]]]]]]]]]',Gradient)
        #print('[[[[[[[[[[[]]]]]]]]]]]',PhaseBeam)
        #print('[[[]]]]',KPhaseB)
        #print('[[[]]]]',V)

        if GunNominal:
            Gun=SF.getElement('SINEG01.RGUN100')
            #Gun.Gradient=33.0
            Gun.Gradient=35.5 # Equivalent to 7.1 MeV total energy
            Gun.Phase=90
        SF.writeFacility(self) # Re-compute the energy at all the elements

        return

    def forceInitialCondition(self,SF,elename,Ei):


        if Ei<0:
            # The initial energy should be positive
            return False # Return zero

        # First compute the energy with the present gradient and phase
        # Note that the energy at the elements upstream of the given initial element is not touched.
        SF.writeFacility(self)

        try:
            # Check if elename exists
            E0=self.Energy[elename][0]
            dE=Ei-E0
            self.Energy[elename][0]=Ei
        except:
            return False


        for k in self.Energy.keys():
            if '.' in k:
                if SF.isUpstream(elename,k):
                    if len(self.Energy[k])==2:
                        self.Energy[k]=[self.Energy[k][0]+dE,self.Energy[k][1]]
                    elif len(self.Energy[k])==3:
                        self.Energy[k]=[self.Energy[k][0]+dE,self.Energy[k][1],self.Energy[k][2]]

        return True

    def writeEnergy2Epics(self,EC,inCallBack=0):
        # Used in Virtual Accelerator but general function
        if not EC:
            return

        dn=EC.getDeviceList('Energy')
        E=[]
        for ch in dn:
            E.append(self.Energy[ch][0])

        if inCallBack:
            hlist=EC.cafe.getHandlesFromWithinGroup('Energy')
            EC.cafe.setScalarList(hlist,E)
        else:
            EC.put('Energy',E)


    def writeRF2Epics(self,SF=None,EC=None):
        # Used in Virtual Accelerator but general function
        if not EC:
            return

        if not SF:
            return
        # First, get list of RFs
        #dn=EC.getDeviceList('RF')
        RFsystem=EC.getDeviceList('RFsystem')

        KPhase=[0]*len(RFsystem)
        KVoltage=[0]*len(RFsystem)
        for k in EC.Cavities.keys():
            c=EC.Cavities[k]
            ele=SF.getElement(c[2])
            KPhase[RFsystem.index(k)]=ele.Phase
            KVoltage[RFsystem.index(k)]=ele.Gradient*ele.Length*(len(c)-2)


        EC.put('RFsystem:SET-ACC-VOLT',KVoltage)
        EC.put('RFsystem:SET-BEAM-PHASE',KPhase)


    def demandMapID(self):
        'Energy manager always requests Map ID to Layout manger'
        return 1


    def EnergyAt(self,ele):
        if isinstance(ele,str):
            name=ele
        else:
            name=ele.Name
        if name in self.Energy.keys():
            return self.Energy[name]
        else:
            print(name+' is not found in Energy manager!')
            print('Configure energy manager first if your application need energy-info!')
            return [0.0,0.0]

