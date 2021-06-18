import math
import os
from subprocess import call
from OMAppTemplate import ApplicationTemplate
from epics import caget
import numpy as np
from time import sleep
import madx
import zmq


import zlib
import pickle

from metaclass_numpy import twiss

try:
    #from OMSwissFELmagnet import *
    pass
except:
    None

print('madx.__file__')
print(madx.__file__)


#--------
# MAD Interface


class dummyClass:
    def __init__(self,inDict):
        self.__dict__.update(inDict)


class MadX(ApplicationTemplate):
    def __init__(self,initialize_mad=42,sessionID='.'):
        ApplicationTemplate.__init__(self)
        self.SessionID=sessionID # global sessionID
        self.RunID=''
        self.path='.'
        self.madxpath='/gpfs/home/reiche/bin/madx'
        self.fid=0
        self.file=''
        self.BRMK={}
        self.switch=0
        self.cc=[]
        if initialize_mad==1:
            raise ValueError('initialize_mad = 1 unsupported')
        elif initialize_mad==42:
            self.switch=42
        else:
            raise ValueError('initialize_mad != 42 unsupported')

        self.bellows=[]


        self.SFBC=None

        #self.flog=open('logmadx.txt','w')
        #self.flog.close()

        self.MADzero=None

        self.matlab=0

    def finish(self):
        self.pmad=None

    def command(self,txt):
        #self.flog=open('logmadx.txt','a')
        #self.flog.write(txt+'\n')
        #self.flog.close()
        self.pmad.command(txt)

    def sendCommand(self,line):
        #self.flog=open('logmadx.txt','a')
        #self.flog.write(line+'\n')
        #self.flog.close()
        if self.matlab:
            self.mcommand.append(line)
            return

        if self.switch==42:
            if line=='execute':
                print('Execute local madx')
                res=madx.execute(self.cc,raw_results=True)
                self.cc=[]
                #with open('./madx_result.pkl', 'wb') as f:
                #    pickle.dump(res, f)
                return res
            else:

                #self.madx.execute(line)
                self.cc.append(line)
                return

        if not self.MADzero:
            self.MADzero=1
            self.zcontext = zmq.Context()
            self.zsocket=self.zcontext.socket(zmq.REQ)
            self.zsocket.RCVTIMEO=10000
            self.zsocket.connect("tcp://sf-dds-02.psi.ch:"+str(self.portNumber))
        if line=='initialize':
            self.zsocket.send_string('status')

            m=self.zsocket.recv().decode()
            if 'Old' in m:
                self.zsocket.send_string('exit')
                m=self.zsocket.recv().decode()
                sleep(1)
            self.zsocket.send_string(line)
            m=self.zsocket.recv().decode()
            return m
        else:
            #self.flog=open('logmadx.txt','a')
            #self.flog.write(line+'\n')
            #self.flog.close()

            self.zsocket.send_string(line)
            try:
                m=self.zsocket.recv()
            except:
                # Need to refresh the connection???SARUN12-UIND030:K_SET.VAL
                self.zcontext = zmq.Context()
                self.zsocket=self.zcontext.socket(zmq.REQ)
                self.zsocket.RCVTIMEO=10000
                self.zsocket.connect("tcp://sf-dds-02.psi.ch:"+str(self.portNumber))

                m=None # In case ZMQ-MAD twiss failed (can happen when SARUN07-UIND030:K_CORRECTION.VALbeta is extremely high)

            try:
                m=m.decode()
            except:
                'm is twiss_table'

            return m



    def twiss_table(self,columns,dictout=0):
        return self.pmad.twiss_table(columns,dictout)


    def switchOutput(self,switch=1):
        self.switch=switch
        if switch=='Memory' or switch=='memory':
            self.switch=1
        elif switch=='File' or switch=='file':
            self.switch=0
        elif switch=='Server' or switch=='server':
            self.switch=2 # MAD-X ZMQ server!


    def demandMapID(self):
        'OMMadx always requests Map ID to Layout manger'
        return 1

    def updateSFBC(self,SF):
        self.SFBC=SF.BC

    def deleteSFBC(self,SF):
        self.SFBC=None




    def openRun(self,RunID='Madx-Run'):
        self.RunID=RunID
        self.path='%s/%s' % (self.SessionID,self.RunID)
        if os.path.exists(self.path)==0:
            os.mkdir(self.path)

    def openStream(self,name='SwissFEL'):
        if self.switch:
            return
        self.file='%s.madx'% name
        filename='%s/%s' % (self.path,self.file)
        print('Opening Madx Stream into File:',filename)
        self.fid=open(filename,'w')

    def closeStream(self):
        print('Closing Madx Stream')
        if self.switch:
            return
        self.fid.close()

    def executeStream(self):
        if self.switch:
            return            # not needed when Madx is shared library
        cwd=os.getcwd()
        os.chdir(self.path)
        call([self.madxpath, self.file])
        os.chdir(cwd)


    def streamFile(self,filename):
        fin=open(filename,'r')
        for line in fin.readlines():
            self.write(line)
        fin.close()

    def write(self,line):
        if isinstance(line,list):
            for l_ in line:
                self.write(l_)
        else:
            if self.switch==1:
                self.command(line)
            elif self.switch==2:
                return self.sendCommand(line)
            elif self.switch==42:
                self.cc.append(line)
            else:
                self.fid.write(line)



    def isType(self,name):
        if (name.find('madx')>-1):
            return 1
        else:
            return 0


    def writeLine(self,line,seq):


        if (len(line.Name)==7):
            SecName=line.Name
            self.write("%s.START: MARKER;\n" % (SecName))
            self.write("%s.END: MARKER;\n" % (SecName))
            self.write("\n%s: SEQUENCE, REFER=centre, L=%f;\n" % (SecName,line.getResLength()))
            self.write("   %s, AT=%f;\n" % (SecName+'.START',0))
            for ele in seq:
                if 'MADshift' in ele.__dict__:
                    spos=line.position(ele)+ele.sRef+ele.getLength()*0.5+ele.MADshift
                else:
                    spos=line.position(ele)+ele.sRef+ele.getLength()*0.5
                if 'Overlap' in ele.__dict__:
                    if ele.Overlap==0:
                        self.write("   %s, AT=%f;\n" % (ele.Name,spos))
                else:
                    firstb=0
                    if self.SFBC:
                        for bc in self.SFBC:
                            if len(bc)==5:
                                if ele.Name==bc[0].Name:
                                    sposb=spos+ele.Length/2+0.05 # Assume that 5 cm downstream of the bend is free space
                                    bell=ele.Name.replace('MBND','BELL')
                                    firstb=1
                                if ele.Name==bc[3].Name:
                                    sposb=spos-ele.Length/2-0.05 # Assume that 5 cm upstream of the bend is free space
                                    bell=ele.Name.replace('MBND','BELL')
                                    self.write("   %s, AT=%f;\n" % (bell,sposb))
                                    if bell not in self.bellows:
                                        self.bellows.append(bell)
                    if ('MQUA' in ele.Name) and ('corx' not in ele.__dict__):
                        self.write("   %s$START, AT=%f;\n" % (ele.Name,spos-ele.getLength()/2.0))
                        self.write("   %s, AT=%f;\n" % (ele.Name,spos))
                        self.write("   %s$END, AT=%f;\n" % (ele.Name,spos+ele.getLength()/2.0))

                    else:
                        # The case applies for most elements.
                        self.write("   %s, AT=%f;\n" % (ele.Name,spos))

                    if firstb==1:
                        self.write("   %s, AT=%f;\n" % (bell,sposb)) # It should be after the bend.
                        if bell not in self.bellows:
                            self.bellows.append(bell)
            self.write("   %s, AT=%f;\n" % (SecName+'.END',line.getResLength()))
            self.write("ENDSEQUENCE;\n\n")
            return
        else:
            #self.MapIndx=None ##################################3 where is self.MapIndex defined???
            # It is defined in OMType... It is not a good implementation, I know... Masa 21.11.2014
            length=0
            for subline in seq:
                length=length+subline['L']
            if not self.MapIndx:  # had to add this to make it work for me
                if self.MapIndx==0:
                    '0 is not None'
                else:
                    self.MapIndx=None
            if self.MapIndx is not None: # Writing out Facility
                SecName='SEQ'+str(abs(self.MapIndx))
                if self.switch:
                    self.write("  %s.START: Marker;\n" % (SecName))
                    self.write("  %s.END: Marker;\n" % (SecName))
                self.write("\n%s: SEQUENCE, REFER=centre, L=%f;\n" % (SecName,length))
            else:
                self.write("\nSWISSFEL: SEQUENCE, REFER=centre, L=%f;\n" % (length))
            tlength=length
            if self.MapIndx and self.switch:
                self.write("  SEQ%s.START, AT=0.0;\n" % (str(abs(self.MapIndx))))
            length=0
            for subline in seq:
                SecName=subline['Name']
                self.write("   %s, AT=%f;\n" % (SecName,length+subline['L']*0.5))
                length=length+subline['L']
            if self.MapIndx is not None and self.switch:
                self.write("  SEQ%s.END, AT=%f;\n" % (str(abs(self.MapIndx)),tlength))
            self.write("ENDSEQUENCE;\n\n")
            self.MapIndx=None
        return


    def writeDrift(self,ele):
        return

    def writeVacuum(self,ele):
        self.writeMarker(ele)
        return

    def writeAlignment(self,ele):
        self.writeMarker(ele)  # this line is needed, no?
        return

    def writeBend(self,ele):
        Lpath=ele.getLength()
        angrad=ele.angle*math.asin(1)/90

        angradcor=angrad
        if 'cor' in ele.__dict__:
            angradcor=angrad+ele.cor

        if self.SFBC:
            for bc in self.SFBC:
                if len(bc)==5:
                    if ele.Name==bc[1].Name or ele.Name==bc[2].Name:
                        angradcor=0.0
                    if ele.Name==bc[3].Name:
                        angradcor=0.0
                        Lpath=ele.Length # Zero-angle length
                        bell=ele.Name.replace('MBND','BELL')
                        self.write("%s: MATRIX, L=0.0, RM11=1.0, RM12=0.0, RM21=0.0, RM22=1.0, RM33=1.0, RM34=0.0, RM43=0.0, RM44=1.0;\n" % (bell))
                    if ele.Name==bc[0].Name:
                        angradcor=0.0
                        Lpath=ele.Length # Zero-angle length
                        bell=ele.Name.replace('MBND','BELL')
                        self.write("%s: MATRIX, L=0.0, RM11=1.0, RM12=0.0, RM21=0.0, RM22=1.0, RM33=1.0, RM34=0.0, RM43=0.0, RM44=1.0;\n" % (bell))
        self.write("%s: SBEND, L=%f, ANGLE:=%f, TILT=%f, E1=%f, E2=%f;\n" % (ele.Name,Lpath,angradcor,ele.Tilt,ele.e1*angrad,ele.e2*angrad))



    def writeQuadrupole(self,ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap==1:
                return
        # MADExclude is replaced by Overlap
        #if ele.__dict__.has_key('MADExclude'):
        #    if ele.MADExclude==1:
        #        self.writeMarker(ele)
        #        return
        if ('corx' in ele.__dict__) or ('cory' in ele.__dict__):
            self.write("%s.k1 := %f;\n" % (ele.Name, ele.k1))
            if 'corx' in ele.__dict__:
                self.write("%s.corx := %f;\n" % (ele.Name, ele.corx))
            if 'cory' in ele.__dict__:
                self.write("%s.cory := %f;\n" % (ele.Name, ele.cory))
            self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name,ele.Length))
            self.write("   %s.q1:  QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f, AT=%f;\n" % (ele.Name,ele.Length*0.5,ele.Name,ele.Tilt,0.25*ele.Length))
            if 'corx' in ele.__dict__:
                #self.write("   %s.cx: HKICKER, L=0, kick:=%s.corx, AT=%f;\n" % (ele.Name,ele.Name,ele.Length*0.5)) # This change ahs to be discussed
                self.write("   %s.cx: HKICKER, L=0, kick:=%s.corx, AT=%f;\n" % (ele.Name,ele.Name.replace('MQUA','MCRX'),ele.Length*0.5))
            if 'cory' in ele.__dict__:
                self.write("   %s.cy: VKICKER, L=0, kick:=%s.cory, AT=%f;\n" % (ele.Name,ele.Name.replace('MQUA','MCRY'),ele.Length*0.5)) # This change ahs to be discussed
            self.write("   %s.q2:  QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f, at=%f;\n" % (ele.Name,ele.Length*0.5,ele.Name,ele.Tilt,0.75*ele.Length))
            self.write("ENDSEQUENCE;\n")
        else:
            self.write("%s$START: MARKER, L=0.0;\n" % (ele.Name))
            self.write("%s.k1 := %f;\n" % (ele.Name, ele.k1))
            self.write("%s: QUADRUPOLE, L=%f, k1:=%s.k1, tilt=%f;\n" % (ele.Name,ele.Length,ele.Name,ele.Tilt))
            self.write("%s$END: MARKER, L=0.0;\n" % (ele.Name))

    def writeCorrector(self,ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap==1:
                return
        #shift=0
        if 'MADshift' in ele.__dict__:
            #shift=ele.MADshift
            pass
        if 'MADthin' in ele.__dict__:
            if ele.MADthin==1:
                Length=0
            else:
                Length=ele.Length
        else:
            Length=ele.Length

        if ('corx' in ele.__dict__) or ('cory' in ele.__dict__):
            if 'corx' in ele.__dict__:
                self.write("%s.corx := %f;\n" % (ele.Name.replace('MCOR','MCRX'), ele.corx))
            if 'cory' in ele.__dict__:
                self.write("%s.cory := %f;\n" % (ele.Name.replace('MCOR','MCRY'), ele.cory))
            if Length>0:
                self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name,ele.LengthRes))
                if ('corx' in ele.__dict__) and ('cory' in ele.__dict__):
                    self.write("   %s.cxy: KICKER, L=%s, hkick:=%s.corx, vkick:=%s.cory, AT=%f;\n" % (ele.Name,ele.Length,ele.Name.replace('MCOR','MCRX'),ele.Name.replace('MCOR','MCRY'),ele.sRef+ele.Length*0.5))
                elif 'corx' in ele.__dict__:
                    self.write("   %s.cx: HKICKER, L=%s, kick:=%s.corx, AT=%f;\n" % (ele.Name,ele.Length,ele.Name.replace('MCOR','MCRX'),ele.sRef+ele.Length*0.5))
                elif 'cory' in ele.__dict__:
                    self.write("   %s.cy: VKICKER, L=%s, kick:=%s.cory, AT=%f;\n" % (ele.Name,ele.Length,ele.Name.replace('MCOR','MCRY'),ele.sRef+ele.Length*0.5))
                self.write("ENDSEQUENCE;\n")
            else:
                if ('corx' in ele.__dict__) and ('cory' in ele.__dict__):
                    self.write("%s: KICKER, L=0, hkick:=%s.corx, vkick:=%s.cory;\n" % (ele.Name,ele.Name.replace('MCOR','MCRX'),ele.Name.replace('MCOR','MCRY')))
                elif 'corx' in ele.__dict__:
                    self.write("%s: HKICKER, L=0, kick:=%s.corx;\n" % (ele.Name,ele.Name.replace('MCOR','MCRX')))
                elif 'cory' in ele.__dict__:
                    self.write("%s: VKICKER, L=0, kick:=%s.cory;\n" % (ele.Name,ele.Name.replace('MCOR','MCRY')))

            return ele.Name


    def writeSextupole(self,ele):
        self.write("%s.k2 := %f;\n" % (ele.Name, ele.k2))
        self.write("%s: SEXTUPOLE, L=%f, k2:=%s.k2, tilt=%f;\n" % (ele.Name,ele.Length,ele.Name,ele.Tilt))

    def writeRF(self,ele):
        p0=ele.p0
        #dP=ele.Gradient/511000*math.sin(ele.Phase*math.asin(1)/90)*ele.Length
        if 'dP' in ele.__dict__:  # ele.dP is used??
            dP=ele.dP
        if ele.Gradient:
            ## p from Energy manager is in units of eV          => MeV since 29.06.2015
            dP=ele.Gradient*math.sin(ele.Phase*math.asin(1)/90)*ele.Length
        else:
            dP=0


        if 'TDS' in ele.Name:
            # This simplified implementation is to compute the beam trajectory only
            # Need to define all the matrix element if used for other purpose...
            m11=1
            m12=ele.Length
            m21=0
            m22=p0/(p0+dP)
            m33=1
            m34=ele.Length
            m43=0
            m44=1
            m45=dP/p0 # and set t=1.0 for the initial condition
        elif dP==0 or ('RGUN' in ele.Name)or p0<=0 or (p0+dP)<0:
            #self.writeMarker(ele)
            #return
            m11=1.0
            m12=ele.Length
            m21=0.0
            m22=1.0
        else:
            m11=1
            m12=p0*ele.Length/dP*math.log((p0+dP)/p0)
            m21=0
            m22=p0/(p0+dP)
            e11=1
            e12=0
            e21=-0.5*dP/p0/ele.Length
            e22=1
            d11=m11*e11+m12*e21
            d12=m11*e12+m12*e22
            d21=m21*e11+m22*e21
            d22=m21*e12+m22*e22
            e21=0.5*dP/(p0+dP)/ele.Length
            m11=e11*d11+e12*d21
            m12=e11*d12+e12*d22
            m21=e21*d11+e22*d21
            m22=e21*d12+e22*d22
        self.write("%s: MATRIX, L=%f,\n" % (ele.Name, ele.Length))
        self.write("   RM11=%f,\n" % (m11))
        self.write("   RM12=%f,\n" % (m12))
        self.write("   RM21=%f,\n" % (m21))
        self.write("   RM22=%f,\n" % (m22))
        if 'TDS' in ele.Name:
            self.write("   RM33=%f,\n" % (m33))
            self.write("   RM34=%f,\n" % (m34))
            self.write("   RM43=%f,\n" % (m43))
            self.write("   RM44=%f;\n" % (m44))
            self.write("   RM45=%f;\n" % (m45))
        else:
            self.write("   RM33=%f,\n" % (m11))
            self.write("   RM34=%f,\n" % (m12))
            self.write("   RM43=%f,\n" % (m21))
            self.write("   RM44=%f;\n" % (m22))


    def writeUndulator(self,ele):
        if 'UDCP' in ele.Name:
            m11=1
            m12=ele.Length
            m21=0
            m22=1
            self.write("%s: MATRIX, L=%f,\n" % (ele.Name, ele.Length))
            self.write("   RM11=%f,\n" % (m11))
            self.write("   RM12=%f,\n" % (m12))
            self.write("   RM21=%f,\n" % (m21))
            self.write("   RM22=%f,\n" % (m22))
            self.write("   RM33=%f,\n" % (m11))
            self.write("   RM34=%f,\n" % (m12))
            self.write("   RM43=%f,\n" % (m21))
            self.write("   RM44=%f;\n" % (m22))
            #print('Warning! UDCP treated as an undulator!')
            return
        p0=ele.p0/0.511
        if ele.kx == 0 and ele.ky == 0:
            kx = ky = 0
        else:
            #p0_mev = caget(ele.Name.replace('.','-') + ':ENERGY-OP')

            #if p0_mev is None:
            #   from PyQt4.QtCore import pyqtRemoveInputHook
            #   from pdb import set_trace
            #   pyqtRemoveInputHook()
            #   set_trace()
            #    raise ValueError("No energy for", ele.Name)
            #p0 = p0_mev* 1e6
            #print(ele.Name, p0)
            #p0=ele.p0/0.511
            kmax=ele.K*ele.ku/p0
            kx=ele.kx*0.5*kmax*kmax
            ky=ele.ky*0.5*kmax*kmax

        if kx>0:
            omg=math.sqrt(kx)*ele.Length
            m11=math.cos(omg)
            m12=math.sin(omg)/math.sqrt(kx)
            m21=-math.sin(omg)*math.sqrt(kx)
            m22=math.cos(omg)
        else:
            if kx<0:
                omg=math.sqrt(kx)*ele.Length
                m11=math.cosh(omg)
                m12=math.sinh(omg)/math.sqrt(kx)
                m21=math.sinh(omg)*math.sqrt(kx)
                m22=math.cosh(omg)
            else:
                m11=1
                m12=ele.Length
                m21=0
                m22=1
        self.write("%s: MATRIX, L=%f,\n" % (ele.Name, ele.Length))
        self.write("   RM11=%f,\n" % (m11))
        self.write("   RM12=%f,\n" % (m12))
        self.write("   RM21=%f,\n" % (m21))
        self.write("   RM22=%f,\n" % (m22))
        if ky>0:
            omg=math.sqrt(ky)*ele.Length
            m11=math.cos(omg)
            m12=math.sin(omg)/math.sqrt(ky)
            m21=-math.sin(omg)*math.sqrt(ky)
            m22=math.cos(omg)
        else:
            if ky<0:
                omg=math.sqrt(ky)*ele.Length
                m11=math.cosh(omg)
                m12=math.sinh(omg)/math.sqrt(ky)
                m21=math.sinh(omg)*math.sqrt(ky)
                m22=math.cosh(omg)
            else:
                m11=1
                m12=ele.Length
                m21=0
                m22=1
        self.write("   RM33=%f,\n" % (m11))
        self.write("   RM34=%f,\n" % (m12))
        self.write("   RM43=%f,\n" % (m21))
        self.write("   RM44=%f;\n" % (m22))

    def writeDiagnostic(self,ele):
        if (ele.enable==0):
            self.writeMarker(ele)
            return
        Seval=ele.Seval
        if (Seval<0):
            Seval=0.5*ele.Length
        self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name,ele.Length))
        self.write("    %s.diag: MONITOR, L=0, AT=%f;\n" %(ele.Name,Seval))
        self.write("ENDSEQUENCE;\n")


    def writeMarker(self,ele):
        Seval=0.5*ele.Length
        if ele.Length>0:
            self.write("%s: SEQUENCE, REFER=centre, L=%f;\n" % (ele.Name,ele.Length))
            self.write("    %s.mark:  MARKER, AT=%f;\n" %(ele.Name,Seval))
            self.write("ENDSEQUENCE;\n")
        else: # Simple marker, zero reserve length
            self.write("    %s:  MARKER;\n" %(ele.Name))


    def writeSolenoid(self,ele):
        if 'Overlap' in ele.__dict__:
            if ele.Overlap==1:
                return
        self.write("%s.ks := %f;\n" % (ele.Name, ele.ks))
        self.write("%s: SOLENOID, L=%f, ks:=%s.ks;\n" % (ele.Name,ele.Length,ele.Name))


    def updateTDSmatrixFromEpics(self,EC=None,EM=None,PhaseOffset=None):
        # Used in Virtual Accelerator but general function

        if not EC:
            return
        if not EM:
            return

        # Possibly TDSs could be in a different group from RFs in OMEpicsChannel... to be discussed
        # For now, it is assumed in the same group to RF

        #dn,Gradient=EC.get('RF:GRADIENT')
        #dn,Phase=EC.get('RF:PHASE')
        #dn,PhaseON=EC.get('RF:PHASE-ONCREST')

        dn=EC.getDeviceList('RF')


        klystron,Status=EC.get('RFsystem:GET-RF-READY-STATUS',0,'int')
        klystron,Mode=EC.get('RFsystem:GET-STATION-MODE')
        klystron,State=EC.get('RFsystem:GET-STATION-STATE')

        klystron,V=EC.get('RFsystem:GET-ACC-VOLT')
        klystron,KPhase=EC.get('RFsystem:GET-VSUM-PHASE')
        klystron,KPhaseON=EC.get('RFsystem:SET-VSUM-PHASE-OFFSET-BASE')
        klystron,KPhaseB=EC.get('RFsystem:GET-BEAM-PHASE')

        # Check if the rf stations are in operation
        kok={}
        for i in range(0,len(klystron)):
            sec=klystron[i].split('.')[0]
            Length=EC.Cavities[klystron[i]][1]
            if State[i]=='RF ON PHAFB' or State[i]=='RF ON AMPFB' or State[i]=='RF ON FB':
                State[i]='RF ON'
            if Mode[i]=='NORMAL' and State[i]=='RF ON' and Status[i]:
                kok[sec]=[V[i]/(len(EC.Cavities[klystron[i]])-2)/Length,KPhase[i],KPhaseON[i],KPhaseB[i]]
            else:
                kok[sec]=[0,KPhase[i],KPhaseON[i],KPhaseB[i]]

        Phase=[0]*len(dn)
        PhaseON=[0]*len(dn)
        PhaseB=[0]*len(dn)
        Gradient=[0]*len(dn)
        for i in range(0,len(dn)):
            sec=dn[i].split('.')[0]
            Gradient[i]=kok[sec][0]
            Phase[i]=kok[sec][1]
            PhaseON[i]=kok[sec][2]
            PhaseB[i]=kok[sec][3]


        TDSindx=[]
        for d in dn:
            if 'TDS' in d:
                TDSindx.append(dn.index(d))
        TDSon=[]
        for i in TDSindx:
            if Gradient[i]>0:
                TDSon.append([dn[i],1])
                p0=EM.Energy[dn[i]][0]
                if PhaseOffset:
                    Phase[i]=Phase[i]+PhaseON[i]-PhaseOffset[i]
                dP=Gradient[i]*math.sin(Phase[i]*math.asin(1)/90)*EM.Energy[dn[i]][2]
                # Approximated implementation to compute only for the beam trajectory
                # Need to define all the matrix element if used for other purpose...
                m45=dP/p0
                self.write("%s->RM45=%f;" % (dn[i],m45))
            else:
                TDSon.append([dn[i],0])
                self.write("%s->RM45=%f;" % (dn[i],0))

        return TDSon

    def updateRFmatrix(self,EM=None):
        # Used in Virtual Accelerator but general function
        if not EM:
            return

        for k in EM.Energy.keys():
            if 'RACC' in k:
                p0=EM.Energy[k][0]
                dP=EM.Energy[k][1]
                L=EM.Energy[k][2]
                if dP==0 or p0<=0 or (p0+dP)<0:
                    m11=1.0
                    m12=L
                    m21=0.0
                    m22=1.0
                else:
                    m11=1
                    m12=p0*L/dP*math.log((p0+dP)/p0)
                    m21=0
                    m22=p0/(p0+dP)
                    e11=1
                    e12=0
                    e21=-0.5*dP/p0/L
                    e22=1
                    d11=m11*e11+m12*e21
                    d12=m11*e12+m12*e22
                    d21=m21*e11+m22*e21
                    d22=m21*e12+m22*e22
                    e21=0.5*dP/(p0+dP)/L
                    m11=e11*d11+e12*d21
                    m12=e11*d12+e12*d22
                    m21=e21*d11+e22*d21
                    m22=e21*d12+e22*d22
                self.write("%s->RM11=%f;" % (k,m11))
                self.write("%s->RM12=%f;" % (k,m12))
                self.write("%s->RM21=%f;" % (k,m21))
                self.write("%s->RM22=%f;" % (k,m22))
                self.write("%s->RM33=%f;" % (k,m11))
                self.write("%s->RM34=%f;" % (k,m12))
                self.write("%s->RM43=%f;" % (k,m21))
                self.write("%s->RM44=%f;" % (k,m22))

    def reflectRFmatrix(self,EM=None):
        if not EM:
            return

        for k in EM.Energy.keys():
            if 'RACC' in k:
                p0=EM.Energy[k][0]+EM.Energy[k][1]
                dP=-EM.Energy[k][1]
                L=EM.Energy[k][2]
                if dP==0 or p0<0 or (p0+dP)<0:
                    m11=1.0
                    m12=L
                    m21=0.0
                    m22=1.0
                else:
                    m11=1
                    m12=p0*L/dP*math.log((p0+dP)/p0)
                    m21=0
                    m22=p0/(p0+dP)
                    e11=1
                    e12=0
                    e21=-0.5*dP/p0/L
                    e22=1
                    d11=m11*e11+m12*e21
                    d12=m11*e12+m12*e22
                    d21=m21*e11+m22*e21
                    d22=m21*e12+m22*e22
                    e21=0.5*dP/(p0+dP)/L
                    m11=e11*d11+e12*d21
                    m12=e11*d12+e12*d22
                    m21=e21*d11+e22*d21
                    m22=e21*d12+e22*d22
                self.write("%s->RM11=%f;" % (k,m11))
                self.write("%s->RM12=%f;" % (k,m12))
                self.write("%s->RM21=%f;" % (k,m21))
                self.write("%s->RM22=%f;" % (k,m22))
                self.write("%s->RM33=%f;" % (k,m11))
                self.write("%s->RM34=%f;" % (k,m12))
                self.write("%s->RM43=%f;" % (k,m21))
                self.write("%s->RM44=%f;" % (k,m22))



    def updateAramisUndulatorfromEpics(self,EC=None,SM=None,SF=None,EM=None,updateMADX=0):
        if EC is None or SM is None:
            return 0

        # Temporaly implementation


        Kval=[]
        for i in range(3,10):
            try:
                Ki=EC.get1('SARUN0'+str(i)+'-UIND030:K_CORRECTION.VAL')
            except:
                return 0
            Kval.append(Ki)
        for i in range(10,16):
            try:
                Ki=EC.get1('SARUN'+str(i)+'-UIND030:K_CORRECTION.VAL')
            except:
                return 0
            Kval.append(Ki)


        for i in range(3,10):
            Und=SF.getElement('SARUN0'+str(i)+'.UIND030')
            Und.K=Kval[i-3]
        for i in range(10,16):
            Und=SF.getElement('SARUN'+str(i)+'.UIND030')
            Und.K=Kval[i-3]

        Stat=EC.get1('SINLH02-UIND230:MVPOS-X')
        if Stat=='In':
            try:
                Kval=EC.get1('SINLH02-UIND230:K')
            except:
                0
        else:
            Kval=0

        Und=SF.getElement('SINLH02.UIND230')
        Und.K=Kval

        if updateMADX:
            'This is not implemented (but it may not be necessary)'

        return 1



    def updateQuadKfromEpics(self,EC=None,SM=None,SF=None,EM=None,updateMADX=0,PScheck=1):
        # Used in Virtual Accelerator but general function
        # updateSF=-1: update only madx, updateSF=0: update only SF, updateSF=1 or other number: update madx and SF,
        if EC is None or SM is None:
            return 0

        dn,Mode,Summary,slist=EC.get('Quad:PS-MODE',1) # With the second argument=1, Status of cafe.groupGet is returned
        # For the incomplete machine, I had to turn off this check...
        #if Summary!=1:
        #    return 0 # Update was not successful

        if EM:
            # If EM is given, compute KL from I based on the energy info stored
            dn,I,Summary,slist=EC.get('Quad:I-SET',1)
            KL=SM.QuadrupoleI2KL(dn,I,EM)
        else:
            dn,KL,Summary,slist=EC.get('Quad:KL',1)

        # The following can be enabled should the KL calculation of the on-line model stop working. (September 2020 - Philipp Dijkstal and Sven Reiche)
        #KL = []
        #for name in dn:
        #    if name in ('SATMA01.MQUA300', 'SATMA01.MQUA310', 'SATMA01.MQUA320', 'SATUN05.MQUA420'):
        #        KL.append(0.)
        #    elif 'MQUA' in name:
        #        KL.append(caget(name.replace('.','-')+':K1L-SET'))
        #    else:
        #        KL.append(0.)
        #print(KL)

        #if Summary!=1:
        #    return 0

        QuadKL=[]
        for i in range(0,len(dn)):
            if Mode[i]=='On':
                QuadKL.append(KL[i])
            else:
                if PScheck:
                    QuadKL.append(0.0)
                else:
                    QuadKL.append(KL[i])


        QuadK=SM.QuadrupoleKL2K(dn,QuadKL)


        if updateMADX:
            for i in range(0,len(dn)):
                d=dn[i]
                k=QuadK[i]
                self.write(d+'.k1:='+str(k)+';')
                #print(d+'.k1:='+str(k)+';')

        SF.setGroup(dn,'k1',QuadK)

        return 1

    def updateBendAngleFromEpics(self,EC=None,SM=None,SF=None,EM=None,updateMADX=0,PScheck=1):
        # Used in Virtual Accelerator but general function
        # if updateSF==1, ele.Angle is also updated
        if EC is None or SM is None or SF is None:
            return 0

        dn,Mode,Summary,slist=EC.get('Bend:PS-MODE',1) # With the second argument=1, Status of cafe.groupGet is returned
        #if Summary!=1:
        #    return 0 # Update was not successful

        # Hard coded for hot fix
        ILH=dn.index('SINLH02.MBND100')
        IBC1=dn.index('SINBC02.MBND100')
        IBC2=dn.index('S10BC02.MBND100')
        ICL=dn.index('SARCL02.MBND100')

        for i in range(0,len(dn)):
            d=dn[i]
            if ('SINLH' in d) and ('MBND100' not in d):
                Mode[i]=Mode[ILH]
            if ('SINBC' in d) and ('MBND100' not in d):
                Mode[i]=Mode[IBC1]
            if ('S10BC' in d) and ('MBND100' not in d):
                Mode[i]=Mode[IBC2]
            if ('SARCL' in d) and ('MBND100' not in d):
                Mode[i]=Mode[ICL]


        if EM:
            # If EM is given, compute Angle from I based on the energy info stored
            dn,I,Summary,slist=EC.get('Bend:I-SET',1)
            ILH=dn.index('SINLH02.MBND100')
            IBC1=dn.index('SINBC02.MBND100')
            IBC2=dn.index('S10BC02.MBND100')
            ICL=dn.index('SARCL02.MBND100')
            for i in range(0,len(dn)):
                d=dn[i]
                if ('SINLH' in d) and ('MBND100' not in d):
                    I[i]=I[ILH]
                if ('SINBC' in d) and ('MBND100' not in d):
                    I[i]=I[IBC1]
                if ('S10BC' in d) and ('MBND100' not in d):
                    I[i]=I[IBC2]
                if ('SARCL' in d) and ('MBND100' not in d):
                    I[i]=I[ICL]
            Angle=SM.BendI2Angle(dn,I,EM)
        else:
            dn,Angle,Summary,slit=EC.get('Bend:ANGLE',1)

        ### The following can be enabled should the on-line model stop working for the angles. (September 2020 - Philipp Dijkstal and Sven Reiche)

        #Angle = []
        #for name in dn:
        #    name = name.replace('.','-')
        #    if "SARUN09" in name or 'MBNP' in name or 'SATUN' in name or 'SINEG' in name or 'SATBD01' in name:
        #        Angle.append(0.)
        #    elif ('SINBC' in name or 'S10BC' in name or 'SINLH' in name) and name[-7:-3] == 'MBND':
        #        name = name[:-3] + '100'
        #        Angle.append(caget(name+':ANGLE-CALC'))
        #    else:
        #        if 'SARCL' in name or 'SATCL' in name or 'SATSY02' in name:
        #            name = name[:-3] + '100'
        #        Angle.append(caget(name+':BEND-ANGLE'))

        #print('Angle from epics', Angle)



        #if Summary!=1:
        #    return 0 # Update was not successful

        for i in range(0,len(Angle)):
            if Mode[i]=='On':
                PSon=1.0
            else:
                PSon=0.0
            Angle[i]=Angle[i]*EC.Bendp[i]*PSon


        if updateMADX:
            for i in range(0,len(dn)):
                d=dn[i]
                ang=Angle[i]*math.pi/180.0 # Angle is in units of degree while in units of radian in madx
                self.write(d+'->ANGLE:='+str(ang)+';')
                ele=SF.getElement(d)
                if ele.e1!=0:
                    ang_e1=ang*ele.e1
                    self.write(d+'->e1:='+str(ang_e1)+';')
                if ele.e2!=0:
                    ang_e2=ang*ele.e2
                    self.write(d+'->e2:='+str(ang_e2)+';')


        SF.setGroup(dn,'angle',Angle)


        return 1

    def updateCorrectorKickFromEpics(self,EC=None,SM=None,SF=None,EM=None,updateMADX=0,PScheck=1):
        # Used in Virtual Accelerator but general function
        if EC is None:
            return 0

        dn,Mode,Summary,slist=EC.get('Corrector:PS-MODE',1) # With the second argument=1, Status of cafe.groupGet is returned
        if Summary!=1:
            return 0 # Update was not successful

        if EM:
            # If EM is given, compute Kick from I
            dn, current =EC.get('Corrector:I-SET')
            Kick=SM.CorrectorI2Kick(dn, current, EM)
        else:
            dn,Kick=EC.get('Corrector:KICK')

        if Summary!=1:
            return 0

        CorrKick=[]
        for i in range(0,len(dn)):
            if Mode[i]=='On':
                CorrKick.append(Kick[i])
            else:
                CorrKick.append(0.0)


        for i in range(0,len(dn)):
            d=dn[i]
            k=CorrKick[i]
            if 'MCRX' in d:
                self.write(d+'.corx:='+str(k)+';')
            elif 'MCRY' in d:
                self.write(d+'.cory:='+str(k)+';')

        #if updateSF and SF!=None:
        #    SF.setGroup(dn,***,CorrKick)
        # This is not straightforward because most correctors are integrated into quad or bend, and they dont appear explicitly in the layout...

        return 1

    def zeroCorrectorKick(self,EC=None):
        # Used in Virtual Accelerator but general function
        if EC is None:
            return

        dn=EC.getDeviceList('Corrector')

        for i in range(0,len(dn)):
            d=dn[i]
            if 'MCRX' in d:
                self.write(d+'.corx:=0.0;')
            elif 'MCRY' in d:
                self.write(d+'.cory:=0.0;')



    def updatePQuadKfromEpics(self,EC=None,SM=None,SF=None,EM=None,updateMADX=0):
        # Used in Virtual Accelerator but general function
        if EC is None or SM is None:
            return

        if EM:
            # If EM is given, compute KL from I based on the energy info stored
            dn=EC.getDeviceList('PQuad')
            PQuadKL=SM.PQuadrupoleKL(dn,EM)
        else:
            dn,PQuadKL=EC.get('PQuad:KL')

        PQuadK=SM.QuadrupoleKL2K(dn,PQuadKL) # This method is valid also for PQuad

        dnp,State=EC.get('PQuadMotor:X')

        if updateMADX:
            for i in range(0,len(dn)):
                if not State[i]: # X==0 is 'out'
                    PQuadK[i]=0
                d=dn[i]
                k=PQuadK[i]
                self.write(d+'.k1:='+str(k)+';')

        SF.setGroup(dn,'k1',PQuadK)



    def SequenceFromEpics(self,SF=None,EC=None,SM=None, EM=None):
        # Method for Virtual Accelerator
        if SF is None or EC is None or SM is None or EM is None:
            return

        Trace=SM.BeamPathFromEpics(EC,SF,EM)

        if Trace[0][1]==1:
            # Injector dump is on, and thus no beam for madx (simulator for high-energy part, that is after SB02)
            return []

        deadend=0
        first=1
        params,values=EC.get('SINLH03.EXIT')
        EX=values[4] # this field is for the geometrical emittance, but EXN and EYN are not available in twiss table...
        EY=values[5] # so, let's use it...
        charge=values[6]
        self.command('Beam,particle=electron,bcurrent='+str(charge)+',EX='+str(EX)+',EY='+str(EY)+';')
        seqs=[]
        for i in range(0,len(Trace)):
            SID=str(Trace[i][0])
            self.command('use,sequence=SEQ'+SID+';')
            self.command('select, flag=twiss, clear;')
            if Trace[i][1]==-1 and deadend==0:
                if first:
                    self.command('seqedit, sequence=SEQ'+SID+';')
                    self.command('flatten;')
                    self.command('extract,sequence=SEQ'+SID+',from=SINLH03$END,to=SEQ'+SID+'.END,newname=SEQ'+SID+'N;')
                    self.command('endedit;')
                    seqs.append('SEQ'+SID+'N')
                    first=0
                else:
                    seqs.append('SEQ'+SID)
            elif deadend==0: # Cheking branch bend excitation
                ele=SF.getElement(Trace[i][3])
                angle=Trace[i][4]
                dangle=ele.design_angle
                if dangle<0:
                    angle=-angle
                L=ele.Length
                x=L/math.sin(dangle*math.pi/180)*(1-math.cos(dangle*math.pi/180))*(1.0-abs(angle/dangle))
                xp=math.sin(dangle*math.pi/180)*(1.0-abs(angle/dangle))
                #x=L/math.sin(dangle*math.pi/180)*(1-math.cos(dangle*math.pi/180))-L/math.sin(angle*math.pi/180)*(1-math.cos(angle*math.pi/180))
                #xp=(angle-dangle)*math.pi/180


                if abs(x)>0.01: # more than 1 cm mismatch to the next beam line
                    deadend=1

                self.command('seqedit, sequence=SEQ'+SID+';')
                self.command('flatten;')
                if first:
                    self.command('extract,sequence=SEQ'+SID+',from=SINLH03$END,to='+Trace[i][2]+',newname=SEQ'+SID+'N;')
                    first=0
                else:
                    self.command('extract,sequence=SEQ'+SID+',from=SEQ'+SID+'$START,to='+Trace[i][2]+',newname=SEQ'+SID+'N;')
                self.command('endedit;')

                self.command('use,sequence=SEQ'+SID+'N;')
                self.command(Trace[i][3]+'->ANGLE:='+str(Trace[i][4]*math.pi/180)+';') # Setting angle without changing the dipole length...
                if angle==dangle:
                    seqs.append('SEQ'+SID+'N')
                else:
                    seqs.append(['SEQ'+SID+'N',x,xp]) # position and angle error at the exit
        return seqs,Trace

    def concatenateTwiss(self,tws):
        # Method for Virtual Accelerator
        betx_max=0.0
        bety_max=0.0
        dx_max=0.0
        dx_rms=[]
        dy_max=0.0
        dy_rms=[]

        x_max=0.0
        x_rms=[]
        y_max=0.0
        y_rms=[]

        length=0.0
        Q1=0.0
        dQ1=0.0
        Q2=0.0
        dQ2=0.0



        indict={}
        indict['indx']={}
        nelem=0
        for tw in tws:
            memberAll=dir(tw)
            member=[x for x in memberAll if '__' not in x] # Beauty of Python!!!
            for m in sorted(member,reverse=True): # the sorting is to have LENGTH after S
                a=tw.__dict__[m]
                if m=='BETXMAX' and a>betx_max:
                    betx_max=a
                if m=='BETYMAX' and a>bety_max:
                    bety_max=a
                if m=='DXMAX' and a>dx_max:
                    dx_max=a
                if m=='DYMAX' and a>dy_max:
                    dy_max=a
                if m=='XMAX' and a>x_max:
                    x_max=a
                if m=='YMAX' and a>y_max:
                    y_max=a
                if m=='Q1':
                    Q1=Q1+a
                    dQ1=a
                if m=='Q2':
                    Q2=Q2+a
                    dQ2=a
                if m not in indict.keys():
                    if isinstance(a,list):
                        indict[m]=[]
                    elif m!='indx':
                        indict[m]=a
                if m=='S':
                    for i in range(0,len(a)):
                        a[i]=a[i]+length
                if m=='LENGTH':
                    length=length+a
                if m=='MUX':
                    for i in range(0,len(a)):
                        a[i]=a[i]+(Q1-dQ1)
                    indict[m]=indict[m]+a
                elif m=='MUY':
                    for i in range(0,len(a)):
                        a[i]=a[i]+(Q2-dQ2)
                    indict[m]=indict[m]+a
                elif isinstance(a,list):
                    indict[m]=indict[m]+a
                    if m=='DX':
                        dx_rms=dx_rms+a
                    elif m=='DY':
                        dy_rms=dy_rms+a
                    elif m=='X':
                        x_rms=x_rms+a
                    elif m=='Y':
                        y_rms=y_rms+a


                if m=='indx':
                    for n in tw.NAME:
                        indict['indx'][n]=a[n]+nelem
                    nelem=nelem+len(tw.NAME)

        dx_rms=np.array(dx_rms)
        dx_rms=dx_rms.std()
        dy_rms=np.array(dy_rms)
        dy_rms=dy_rms.std()
        indict['DXRMS']=dx_rms
        indict['DYRMS']=dy_rms

        x_rms=np.array(dx_rms)
        x_rms=dx_rms.std()
        y_rms=np.array(dy_rms)
        y_rms=dy_rms.std()
        indict['XRMS']=x_rms
        indict['YRMS']=y_rms

        indict['Q1']=Q1
        indict['Q2']=Q2
        indict['BETXMAX']=betx_max
        indict['BETYMAX']=bety_max
        indict['DXMAX']=dx_max
        indict['DYMAX']=dy_max
        indict['XMAX']=x_max
        indict['YMAX']=y_max


        indict.pop('__init__',None)
        indict.pop('__doc__',None)
        indict.pop('__module__',None)




        return dummyClass(indict)




    def runSequences(self,seqs,initialCondition,misalign=None,betacheck=0):
        # Method for Virtual Accelerator
        # format for initialCondition={'BETX':10.0,'ALFX':0.0,'BETY':10.0,'ALFY':0.0}
        # format for misalign={'SARUN03.MQUA100':[dx,dy],...}
        # Need to run the sequence without misalignments and correctors tocheck if the beta is not too large
        # otherwise the Twiss command fails and a fatal error occurs because pythonmadx extract Twiss table directly from memory...
        # betacheck=1, flat run to check the beta function
        # betacheck=[seq_name,endelem], run


        terminate=[] # [sequence,element] The beta function (x or y) is larger than 3000 m at the element in the sequence. Found from the flat run.
        tws=[]
        for s in seqs:
            try:
                betx=initialCondition['BETX']
            except:
                betx=10.0
            try:
                alfx=initialCondition['ALFX']
            except:
                alfx=0.0
            try:
                bety=initialCondition['BETY']
            except:
                bety=10.0
            try:
                alfy=initialCondition['ALFY']
            except:
                alfy=0.0
            try:
                dx=initialCondition['DX']
            except:
                dx=0.0
            try:
                dpx=initialCondition['DPX']
            except:
                dpx=0.0
            try:
                dy=initialCondition['DY']
            except:
                dy=0.0
            try:
                dpy=initialCondition['DPY']
            except:
                dpy=0.0
            try:
                x=initialCondition['X']
            except:
                x=0.0
            try:
                px=initialCondition['PX']
            except:
                px=0.0
            try:
                y=initialCondition['Y']
            except:
                y=0.0
            try:
                py=initialCondition['PY']
            except:
                py=0.0


            if isinstance(s,list): # Bending magnet is not set to the design angle
                seq=s[0]
            else:
                seq=s

            Range='#s/#e'
            if betacheck==1:
                x=0
                px=0
                y=0
                py=0
                misalign=None
            elif isinstance(betacheck,list):
                if seq==betacheck[0]:
                    Range='#s/'+betacheck[1]



            iniC='range='+Range+', t=1.0, betx='+str(betx)+', alfx='+str(alfx)+', bety='+str(bety)+', alfy='+str(alfy)+', x='+str(x)+', px='+str(px) \
                +', y='+str(y)+', py='+str(py)+', dx='+str(dx)+', dpx='+str(dpx)+', dy='+str(dy)+', dpy='+str(dpy)


            self.command('use, sequence='+seq+';')
            self.command('select, flag=error, clear;') # Clean up if any error set
            self.command('select, flag=twiss, clear;')
            #self.command('select, flag=twiss, pattern="^s";') # This does not work since pythonMad is accessing to the table in the memory directly...
            comm='twiss, sequence='+seq+','+iniC+';'
            self.command(comm)
            tw=self.twiss_table(['NAME','S','BETX','ALFX','BETY','ALFY','X','PX','Y','PY','DX','DPX','DY','DPY','MUX','MUY','ANGLE','E1','E2','K1L'])

            if betacheck==1:
                for n in tw.NAME:
                    if (tw.BETX[tw.indx[n]]>3000 or tw.BETY[tw.indx[n]]>3000) and ('DRIFT' not in n) and len(terminate)==0:
                        terminate=[seq,n]
                        #sys.exit()
                        break

            if misalign:
                #find elements in the sequence
                ee=[]
                for e in misalign.keys():
                    for etw in tw.NAME:
                        if e in etw:
                            if ('$START' not in etw) and ('$END' not in etw) and ('CX' not in etw) and ('CY' not in etw):
                                tl=misalign[e]+[etw]
                                ee.append(tl)

                if len(ee):
                    # clean up any misalignment set
                    self.command('select, flag=error, clear;')
                    # and then assign the misalignments
                    self.command('eoption,add=true;')

                    for i in range(0,len(ee)-1):
                        dx=ee[i][0]-ee[i+1][0]
                        dy=ee[i][1]-ee[i+1][1]
                        ename=ee[i][2]
                        #if ('DBPM' in ename) or ('DSCR' in ename):
                        #    ename=ename+'.mark'
                        comm='select,flag=error,range='+ename+', pattern='+ename+';'
                        self.command(comm)
                        comm='ealign, dx='+str(dx)+', dy='+str(dy)+';'
                        self.command(comm)
                    dx=ee[-1][0]
                    dy=ee[-1][1]
                    ename=ee[-1][2]
                    #if ('DBPM' in ename) or ('DSCR' in ename):
                    #        ename=ename+'.mark'
                    comm='select,flag=error,range='+ename+', pattern='+ename+';'
                    self.command(comm)
                    comm='ealign, dx='+str(dx)+', dy='+str(dy)+';'
                    self.command(comm)

                    #repeat twiss with misalignment
                    #self.command('use, sequence='+seq+';') # N.B. This command eliminates the introduced misalignments!!!!!!!!!!!!!!!!!
                    self.command('select, flag=twiss, clear;')
                    comm='twiss, sequence='+seq+','+iniC+';'
                    self.command(comm)
                    tw=self.twiss_table(['NAME','S','BETX','ALFX','BETY','ALFY','X','PX','Y','PY','DX','DPX','DY','DPY','MUX','MUY'])
                    for e in ee:
                        if 'DBPM' in e[2]:
                            # N.B. misalignment, DX/DY, is not taken into account for monitor!
                            # therefore it is applied here
                            tw.X[tw.indx[e[2]]]=tw.X[tw.indx[e[2]]]-e[0]
                            tw.Y[tw.indx[e[2]]]=tw.Y[tw.indx[e[2]]]-e[1]



            initialCondition['BETX']=tw.BETX[len(tw.BETX)-1]
            initialCondition['ALFX']=tw.ALFX[len(tw.ALFX)-1]
            initialCondition['BETY']=tw.BETY[len(tw.BETY)-1]
            initialCondition['ALFY']=tw.ALFY[len(tw.ALFY)-1]
            initialCondition['X']=tw.X[len(tw.X)-1]
            initialCondition['PX']=tw.PX[len(tw.PX)-1]
            initialCondition['Y']=tw.Y[len(tw.Y)-1]
            initialCondition['PY']=tw.PY[len(tw.PY)-1]
            initialCondition['DX']=tw.DX[len(tw.DX)-1]
            initialCondition['DPX']=tw.DPX[len(tw.DPX)-1]
            initialCondition['DY']=tw.DY[len(tw.DY)-1]
            initialCondition['DPY']=tw.DPY[len(tw.DPY)-1]
            if isinstance(s,list): # Bending magnet is not set to the design angle
                initialCondition['X']=initialCondition['X']+s[1]
                initialCondition['PX']=initialCondition['PX']+s[2]
            tws.append(tw)

        if betacheck==1:
            if len(terminate)==0:
                return 0
            else:
                return terminate
        else:
            return self.concatenateTwiss(tws)


    def adjustBellowsFromEpics(self,EC=None):
        # Used in Virtual Accelerator but general function
        if EC is None:
            return


        for bc in EC.Chicane:
            dn,values=EC.get(bc)
            sdn=dn[0].split(':')[0].split('-')
            sec=sdn[len(sdn)-2]
            arm=None
            for bcm in self.SFBC:
                if sec in bcm[0].Name:
                    arm=bcm[4]
            for bell in self.bellows:
                if sec in bell:
                    pos=values[1]
                    anglerad=math.atan(pos/1000/arm)
                    dl=arm*(1.0/math.cos(anglerad)-1.0)
                    self.write(bell+'->R12='+str(dl)+';\n')  # N.B. This implementation does not change the length of BC in Twiss (or 'S') while the optic paramters will be varied properly.

    def adjustBellows(self,EC=None):
        # Used in Virtual Accelerator but general function
        # Input is from SF (through shallow copy of the bc bending magnet, self.SFBC)
        if EC is None:
            return

        for bc in EC.Chicane:
            dn=EC.getDeviceList(bc)
            sdn=dn[0].split(':')[0].split('-')
            sec=sdn[len(sdn)-2]
            arm=None
            for bcm in self.SFBC:
                if sec in bcm[0].Name:
                    arm=bcm[4]
                    angle=bcm[0].angle
            for bell in self.bellows:
                if sec in bell:
                    anglerad=angle*math.pi/180
                    dl=arm*(1.0/math.cos(anglerad)-1.0)
                    self.write(bell+'->R12='+str(dl)+';\n')



    def getPropagation(self,SF,EM,EC,SM,indict,matlab=0):

        if 'InitialCondition' not in indict.keys():
            return None
        if 'Start' not in indict.keys():
            return None
        if 'End' not in indict.keys():
            return None



        if matlab:
            self.matlab=1
        elif self.switch==42:
            pass
        else:
            # getPropagation uses ZMQ MAD sever unless MADX bugs are fixed.
            # for matlab, this method returns a list of madx command
            self.switchOutput(2)
            self.matlab=0
            self.write('initialize') # Use always fresh MADX
        self.mcommand=[]


        # Energy from the machine
        # This will also set RF from the machine to SF
        # However, the matricies for the rf cavities are computed in 2 steps:
        # 1) Compute the energy at the entrance of the cavity and the enegy gain
        # 2) Then, compute matrix elements based on these values
        # EnergyFromMachine does Step 1
        # Therefore Step 2 has to be followed whenever Step1 is invoked.
        # Otherwise, Energy and Cavity focusing will be inconsistent.
        #try:
        if 'EnergyFromMachine' in indict:
            if indict['EnergyFromMachine']:
                EM.updateEnergyFromEpics(SF,EC) # step1
                self.updateRFmatrix(EM) # step2


        if 'EnergyFromLayout' in indict:
            if indict['EnergyFromLayout']:
                SF.writeFacility(EM) # EM.Energy will be updated.
                self.updateRFmatrix(EM)


        if 'InitialEnergy' in indict:
            if indict['InitialEnergy']:
                elename=indict['InitialElement']
                Ei=indict['InitialEnergyValue']
                EM.forceInitialCondition(SF,elename,Ei)
                self.updateRFmatrix(EM)

        RFchanged=0
        if 'DeviceNameRF' in indict.keys():
            for i in range(0,len(indict['DeviceNameRF'])):
                d=indict['DeviceNameRF'][i]
                try:
                    if 'RACC' in d:
                        #ele.Gradient=indict['Parameter'][2*i]
                        #ele.Phase=indict['Parameter'][2*i+1]
                        RFchanged=1
                except:
                    #'Fail to set parameter(s) to ',k
                    pass


        if RFchanged:
            SF.writeFacility(EM)
            self.updateRFmatrix(EM)



        # Build up the required sequence
        Start=indict['Start']
        End=indict['End']
        s_ele=SF.getElement(indict['Start'])
        e_ele=SF.getElement(indict['End'])

        if ('MQUA' in Start) and s_ele:
            if ('cor' in s_ele.__dict__) or ('corx' in s_ele.__dict__) or ('cory' in s_ele.__dict__):
                Start=Start+'.Q1'
        if ('MQUA' in End) and e_ele:
            if ('cor' in e_ele.__dict__) or ('corx' in e_ele.__dict__) or ('cory' in e_ele.__dict__):
                End=End+'.Q2'

        if s_ele and ('enable' in s_ele.__dict__):
            if s_ele.enable:
                Start=Start+'.diag'
            else:
                Start=Start+'.mark'
        if e_ele and ('enable' in e_ele.__dict__):
            if e_ele.enable:
                End=End+'.diag'
            else:
                End=End+'.mark'


        '''
        if 'END' in End.upper():
            section=End.split('.')
            sec=SF.getSection(section[0])
            path=sec.mapping
        else:
            path=e_ele.mapping[0]
        '''


        section=End.split('.')
        sec=SF.getSection(section[0])

        #print(End,section)
        path=sec.mapping

        line=SF.BeamPath(path)
        line.writeLattice(self,EM)
        #from PyQt4.QtCore import pyqtRemoveInputHook
        #from pdb import set_trace
        #pyqtRemoveInputHook()
        #set_trace()

        # Quad from the machine
        #try:

        if 'PScheck' in indict:
            PScheck=indict['PScheck']
        else:
            PScheck=0

        try:
            if indict['QuadFromMachine']:
                #print('QuadFromMachine')
                self.updateQuadKfromEpics(EC,SM,SF,EM,0,PScheck)
                self.updatePQuadKfromEpics(EC,SM,SF,EM,0)
        except:
            'something wrong Bend from Machine is not given'

        #except:
        #    'something wrong or Quad from Machine is not given'

        # Bend from the machine
        try:
            if indict['BendFromMachine']:
                self.updateBendAngleFromEpics(EC,SM,SF,EM,0)
        except:
            'something wrong Bend from Machine is not given'

        # Corrector from the machine
        try:
            if indict['CorrectorFromMachine']:
                self.updateCorrectorKickFromEpics(EC,SM,SF,EM,0)
        except:
            #self.zeroCorrectorKick(EC)
            'something wrong Bend from Machine is not given'

        # Change parameters if indict['DeviceName'] is given
        if 'DeviceName' in indict.keys():
            Qdn=[]
            QKL=[]
            for i in range(0,len(indict['DeviceName'])):
                d=indict['DeviceName'][i]
                try:

                    ele=SF.getElement(d)
                    if 'MQUA' in d:

                        #ele.k1=indict['Parameter'][i]
                        Qdn.append(d)
                        QKL.append(indict['Parameter'][i])
                    if 'MBND' in d:
                        ele.angle=indict['Parameter'][i]
                except:
                    'Fail to set parameter(s) to ',d
            if Qdn:
                QK=SM.QuadrupoleKL2K(Qdn,QKL)
                #SF.setGroup(Qdn,'k1',QK)
                for i in range(0,len(Qdn)):
                    d=Qdn[i]
                    k=QK[i]
                    self.sendCommand(d+'.k1:='+str(k)+';')
        # Invert the sequence if a backward propagation is required
        # And compute twiss

        if len(indict['InitialCondition'])==4:
            [bx,ax,by,ay]=indict['InitialCondition']
            dx=0
            dpx=0
            dy=0
            dpy=0
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==8:
            [bx,ax,by,ay,dx,dpx,dy,dpy]=indict['InitialCondition']
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==12:
            [bx,ax,by,ay,dx,dpx,dy,dpy,x,py,y,py]=indict['InitialCondition']


        try:
            b=indict['Direction']
            if b<0:
                b=-1
            else:
                b=1
        except:
            b=1

        iniC='betx='+str(bx)+', alfx='+str(b*ax) \
            +', bety='+str(by)+', alfy='+str(b*ay) +',x='+str(x) \
            +', px='+str(px)+', y='+str(y)+', py='+str(py)+', dx='+str(dx) \
            +', dpx='+str(dpx)+', dy='+str(dy)+', dpy='+str(dpy)

        self.sendCommand('beam, particle=electron, energy=100;') # Need high energu to set beta=1

        if b==-1:
            #self.sendCommand('getpropinv: line=(-getprop);\n'); # this results in fatal error...
            self.sendCommand('use, sequence=swissfel;')
            self.sendCommand('seqedit, sequence=swissfel;')
            self.sendCommand('flatten;')
            self.sendCommand('reflect;')
            self.sendCommand('endedit;')
            self.reflectRFmatrix(EM)
            Start,End=End,Start

        seq='swissfel'

        self.sendCommand('use, sequence='+seq+';\n')


        #self.sendCommand('select, flag=error, clear;')
        #self.sendCommand('select, flag=twiss, clear;') # This line causes Mad fatal error!!! Why!!!
        if self.matlab:
            self.sendCommand('select, flag=twiss, column=NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE;')
        elif self.switch==42:
            self.sendCommand('select, flag=twiss, clear;\n')
            self.sendCommand('select, flag=twiss, column=NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE;\n')
        else:
            self.sendCommand('column:NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE')



        comm='twiss, range='+Start+'/'+End+', sequence='+seq+','+iniC+';'


        #tw=self.twiss_table(['NAME','S','BETX','ALFX','BETY','ALFY','X','PX','Y','PY','DX','DPX','DY','DPY','MUX','MUY'])
        if self.matlab:
            return self.mcommand
        elif self.switch==42:
            comm='twiss, range='+Start+'/'+End+', sequence='+seq+','+iniC+',file="twiss";\n'
            self.sendCommand(comm)
            self.sendCommand('exit;')
            z=self.sendCommand('execute')

            try:
                temp_file = '/tmp/twiss_temp'
                with open(temp_file, 'w') as f:
                    # z.data contains the raw lines of the twiss file
                    f.writelines([x+'\n' for x in z.data])
                tw=twiss(temp_file)
            except Exception as e:
                print('Found following exception')
                print(e)
                print('Madx result (z) errors:')
                print(z.errors)
                raise
            finally:
                if os.path.isfile(temp_file):
                    os.remove(temp_file)

            return tw
        else:
            z=self.sendCommand(comm)
            p = zlib.decompress(z)
            tw=pickle.loads(p)

            # This is not needed when using MADX-ZERO server
            #if b==-1:
            #    self.updateRFmatrix(EM) # Don't forget to restore the normal rf matrix after the reflecting!
            try:
                indict['Log']
            except:
                indict['Log']=0

            lg=[]
            if 'Log' in indict.keys():
                if indict['Log']:
                    z=self.sendCommand('log')
                    p = zlib.decompress(z)
                    lg=pickle.loads(p)
            lg = [x for x in lg if x != '\n']
            tw.__dict__.update({'MADlog':lg})


            self.sendCommand('exit')
            sleep(1.0)



            return tw


    def getMatching(self,SF,EM,EC,SM,indict,matlab=0,limit_current=False, method='SIMPLEX'):


        if 'InitialCondition' not in indict.keys():
            return None
        if 'Start' not in indict.keys():
            return None
        if 'End' not in indict.keys():
            return None




        if matlab:
            self.matlab=1
        elif self.switch==42:
            pass
        else:
            # getMatching uses ZMQ MAD sever unless MADX bugs are fixed.
            # for matlab, this method returns a list of MADX commands
            self.switchOutput(2)
            self.matlab=0
            self.write('initialize') # Use always fresh MADX
        self.mcommand=[]



        # Energy from the machine
        # This will also set RF from the machine to SF
        # However, the matricies for the rf cavities are computed in 2 steps:
        # 1) Compute the energy at the entrance of the cavity and the enegy gain
        # 2) Then, compute matrix elements based on these values
        # EnergyFromMachine does Step 1
        # Therefore Step 2 has to be followed whenever Step1 is invoked.
        # Otherwise, Energy and Cavity focusing will be inconsistent.
        #try:
        if 'EnergyFromMachine' in indict:
            if indict['EnergyFromMachine']:
                EM.updateEnergyFromEpics(SF,EC) # step1
                self.updateRFmatrix(EM) # step2


        if 'EnergyFromLayout' in indict:
            if indict['EnergyFromLayout']:
                SF.writeFacility(EM) # EM.Energy will be updated.
                self.updateRFmatrix(EM)


        if 'InitialEnergy' in indict:
            if indict['InitialEnergy']:
                elename=indict['InitialElement']
                Ei=indict['InitialEnergyValue']
                EM.forceInitialCondition(SF,elename,Ei)
                self.updateRFmatrix(EM)

        RFchanged=0
        if 'DeviceNameRF' in indict.keys():
            for i in range(0,len(indict['DeviceNameRF'])):
                d=indict['DeviceNameRF'][i]
                try:
                    if 'RACC' in d:
                        #ele.Gradient=indict['Parameter'][2*i]
                        #ele.Phase=indict['Parameter'][2*i+1]
                        RFchanged=1
                except:
                    #'Fail to set parameter(s) to ',k
                    pass


        if RFchanged:
            SF.writeFacility(EM)
            self.updateRFmatrix(EM)




        # Build up the required sequence
        Start=indict['Start']
        End=indict['End']
        s_ele=SF.getElement(indict['Start'])
        e_ele=SF.getElement(indict['End'])



        if ('MQUA' in Start) and s_ele:
            if ('cor' in s_ele.__dict__) or ('corx' in s_ele.__dict__) or ('cory'in s_ele.__dict__):
                Start=Start+'.Q1'
        if ('MQUA' in End) and e_ele:
            if ('cor' in e_ele.__dict__) or ('corx' in e_ele.__dict__) or ('cory' in e_ele.__dict__):
                End=End+'.Q2'

        if s_ele and ('enable' in s_ele.__dict__):
            if s_ele.enable:
                Start=Start+'.diag'
            else:
                Start=Start+'.mark'
        if e_ele and ('enable' in e_ele.__dict__):
            if e_ele.enable:
                End=End+'.diag'
            else:
                End=End+'.mark'

        '''
        if 'END' in End.upper():
            section=End.split('.')
            sec=SF.getSection(section[0])
            path=sec.mapping
        else:
            path=e_ele.mapping[0]
        '''

        section=End.split('.')
        sec=SF.getSection(section[0])
        path=sec.mapping

        Range=Start+'/'+End

        line=SF.BeamPath(path)
        line.writeLattice(self,EM)

        # Quad from the machine
        try:
            if indict['QuadFromMachine']:
                #print('QuadFromMachine')
                self.updateQuadKfromEpics(EC,SM,SF,EM,0)
                self.updatePQuadKfromEpics(EC,SM,SF,EM,0)
        except:
            'something wrong or Quad from Machine is not given'

        # Bend from the machine
        try:
            if indict['BendFromMachine']:
                self.updateBendAngleFromEpics(EC,SM,SF,EM,0)
        except:
            'something wrong Bend from Machine is not given'

        # Corrector from the machine
        try:
            if indict['CorrectorFromMachine']:
                self.updateCorrectorKickFromEpics(EC,SM,SF,EM,0)
        except:
            #self.zeroCorrectorKick(EC)
            'something wrong Bend from Machine is not given'

        # Change parameters if indict['DeviceName'] is given
        if 'DeviceName' in indict.keys():
            Qdn=[]
            QKL=[]
            for i in range(0,len(indict['DeviceName'])):
                d=indict['DeviceName'][i]
                try:

                    ele=SF.getElement(d)
                    if 'MQUA' in d:

                        #ele.k1=indict['Parameter'][i]
                        Qdn.append(d)
                        QKL.append(indict['Parameter'][i])
                    if 'MBND' in d:
                        ele.angle=indict['Parameter'][i]
                except:
                    'Fail to set parameter(s) to ',d
            if Qdn:
                QK=SM.QuadrupoleKL2K(Qdn,QKL)
                #SF.setGroup(Qdn,'k1',QK)
                for i in range(0,len(Qdn)):
                    d=Qdn[i]
                    k=QK[i]
                    self.sendCommand(d+'.k1:='+str(k)+';')


        if len(indict['InitialCondition'])==4:
            [bx,ax,by,ay]=indict['InitialCondition']
            dx=0
            dpx=0
            dy=0
            dpy=0
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==8:
            [bx,ax,by,ay,dx,dpy,dy,dpy]=indict['InitialCondition']
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==12:
            [bx,ax,by,ay,dx,dpy,dy,dpy,x,py,y,py]=indict['InitialCondition']

        try:
            b=indict['Direction']
            if b<0:
                b=-1
            else:
                b=1
        except:
            b=1
        # Assume that no backward matching
        #b=1

        iniC=', t=1.0, betx='+str(bx)+', alfx='+str(b*ax) \
            +', bety='+str(by)+', alfy='+str(b*ay) +',x='+str(x) \
            +', px='+str(px)+', y='+str(y)+', py='+str(py)+', dx='+str(dx) \
            +', dpx='+str(dpx)+', dy='+str(dy)+', dpy='+str(dpy)



        qknobs=indict['QuadKnobs']
        cons=indict['Constraints']
        e_target=indict['TargetLocation']

        self.sendCommand('beam, particle=electron, energy=100;')

        if b==-1:
            #self.sendCommand('getpropinv: line=(-getprop);\n'); # this results in fatal error...
            self.sendCommand('use, sequence=swissfel;')
            self.sendCommand('seqedit, sequence=swissfel;')
            self.sendCommand('flatten;')
            self.sendCommand('reflect;')
            self.sendCommand('endedit;')
            self.reflectRFmatrix(EM)
            Start,End=End,Start
            Range=Start+'/'+End


        self.sendCommand('use, sequence=swissfel;\n')
        #self.sendCommand('select, flag=error, clear;')
        #self.sendCommand('select, flag=twiss, clear;')

        comm='MATCH,SEQUENCE=swissfel,RANGE='+Range \
            +iniC+';\n'
#             +',betx='+str(bx)+',alfx='+str(ax)+',bety='+str(by)+',alfy='+str(ay)+';\n'

        self.sendCommand(comm)

        for q in qknobs:
            if limit_current:
                pv = q.replace('.', '-').replace('.Q1','').replace('.Q2','')
                i_min = caget(pv + ':I-MIN')
                i_max = caget(pv + ':I-MAX')
                limits = []
                for i_ in i_min, i_max:
                    k1l = SM.QuadrupoleI2KL(q, i_, EM)
                    k1 = SM.QuadrupoleKL2K([q], [k1l], 'M')[0]
                    limits.append(k1)
                #len1 = k1l/k1
                #len2 = caget(pv + ':L-EFF')
                #print(q, limits[0]*len1, limits[1]*len1, len1, len2)

                comm = 'VARY,NAME='+q+'.k1,STEP=0.0001,LOWER=%.8f,UPPER=%.8f;\n' % (limits[0], limits[1])
            else:
                comm = 'VARY,NAME='+q+'.k1,STEP=0.0001;\n'
            #print(comm)
            self.sendCommand(comm)

        for c in cons:
            self.sendCommand('CONSTRAINT,SEQUENCE=swissfel,RANGE='+e_target+','+c+';\n')


        #self.sendCommand('LMDIF,CALLS=1000,TOLERANCE=1e-20;\n')
        self.sendCommand('%s,CALLS=5000,TOLERANCE=1e-18;\n' % method)

        self.sendCommand('ENDMATCH;\n')
        self.sendCommand('VAL_MATCH = TAR;\n')



        if self.matlab:
            self.sendCommand('select, flag=twiss, column=NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE;')
        elif self.switch==42:
            self.sendCommand('select, flag=twiss, clear;\n')
            self.sendCommand('select, flag=twiss, column=NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE;\n') # \n is necessary!!!!!!!!
        else:
            self.sendCommand('column:NAME,S,BETX,ALFX,BETY,ALFY,X,PX,Y,PY,DX,DPX,DY,DPY,MUX,MUY,K1L,ANGLE')



        comm='twiss, range='+Start+'/'+End+', sequence=swissfel'+iniC+';'

        if self.matlab:
            return self.mcommand
        elif self.switch==42:
            comm='twiss, range='+Start+'/'+End+', sequence=swissfel'+iniC+',file="twiss";\n'
            self.sendCommand(comm)
            self.sendCommand('exit;')
            z=self.sendCommand('execute')
            try:
                temp_file = '/tmp/twiss_temp'
                with open(temp_file, 'w') as f:
                    # z.data contains the raw lines of the twiss file
                    f.writelines([x+'\n' for x in z.data])
                tw=twiss(temp_file)
            finally:
                if os.path.isfile(temp_file):
                    os.remove(temp_file)

            QKL=[]
            for q in qknobs:
                try:
                    val = tw.K1L[tw.indx[q]]
                except:
                    val = 2.0*tw.K1L[tw.indx[q+'.Q1']]
                QKL.append(val)

                #i_ = SM.QuadrupoleKL2I(q, val, EM)
                #l_ = caget(q.replace('.', '-')+':L-EFF')
                #print(q, val, i_, val/l_)

            #with open('./debug_madx.pkl', 'wb') as f:
            #    import pickle
            #    pickle.dump(tw, f)
            #    print('Dumped pkl')
                #if 'MQUA020' in q:
                #    from PyQt4.QtCore import pyqtRemoveInputHook
                #    from pdb import set_trace
                #    pyqtRemoveInputHook()
                #    set_trace()

            return tw,QKL
        else:
            z=self.sendCommand(comm)
            p = zlib.decompress(z)
            tw=pickle.loads(p)


            QKL=[]
            for q in qknobs:
                try:
                    QKL.append(tw.K1L[tw.indx[q]])
                except:
                    QKL.append(2.0*tw.K1L[tw.indx[q+'.Q1']])

            lg=[]
            if 'Log' in indict.keys():
                if indict['Log']:
                    z=self.sendCommand('log')
                    p = zlib.decompress(z)
                    lg=pickle.loads(p)
                    lg = [x for x in lg if x != '\n']
                    tw.__dict__.update({'MADlog':lg})

            self.sendCommand('exit')
            sleep(1.0)


            return tw,QKL

    def SimpleMatching(self,indict):

        # Only execute a matching command.
        # Sequence needs to be defined outside.

        if 'InitialCondition' not in indict.keys():
            return
        if 'Knobs' not in indict.keys():
            return
        if 'Constraints' not in indict.keys():
            return
        if 'TargetLocation' not in indict.keys():
            return
        if 'Sequence' not in indict.keys():
            seq='swissfel'
        else:
            seq=indict['Sequence']

        if 'Start' not in indict.keys():
            Start='#s'
        if 'End' not in indict.keys():
            End='#s'

        Start=indict['Start']
        End=indict['End']

        Range=Start+'/'+End


        if len(indict['InitialCondition'])==4:
            [bx,ax,by,ay]=indict['InitialCondition']
            dx=0
            dpx=0
            dy=0
            dpy=0
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==8:
            [bx,ax,by,ay,dx,dpy,dy,dpy]=indict['InitialCondition']
            x=0
            px=0
            y=0
            py=0
        elif len(indict['InitialCondition'])==12:
            [bx,ax,by,ay,dx,dpy,dy,dpy,x,py,y,py]=indict['InitialCondition']


        iniC=', betx='+str(bx)+', alfx='+str(ax) \
            +', bety='+str(by)+', alfy='+str(ay) +',x='+str(x) \
            +', px='+str(px)+', y='+str(y)+', py='+str(py)+', dx='+str(dx) \
            +', dpx='+str(dpx)+', dy='+str(dy)+', dpy='+str(dpy)



        knobs=indict['Knobs']
        cons=indict['Constraints']
        target=indict['TargetLocation']



        #self.write('select, flag=error, clear;')
        #self.write('select, flag=twiss, clear;')

        comm='MATCH,SEQUENCE='+seq+',RANGE='+Range+iniC+';\n'
        self.write(comm)

        for i in range(0,len(knobs)):
            k=knobs[i]
            c=cons[i]
            t=target[i]

            self.write('VARY,NAME='+k+',STEP=0.0001;\n')
            self.write('CONSTRAINT,SEQUENCE=swissfel,RANGE='+t+','+c+';\n')


        self.write('LMDIF,CALLS=1000,TOLERANCE=1e-20;\n')
        self.write('ENDMATCH;\n')
        self.write('VAL_MATCH = TAR;\n')


        if 'Column' in indict.keys():
            col=indict['Column']
        else:
            col=['NAME','S','BETX','ALFX','BETY','ALFY','X','PX','Y','PY','DX','DPX','DY','DPY','MUX','MUY','K1L']



        comm='twiss, range='+Start+'/'+End+', sequence='+seq+iniC+';'
        self.write(comm)

        tw=self.twiss_table(col)

        return tw



    def getMatrix(self,SF,EM,EC,SM,indict,matlab=0):

        indict['InitialCondition']=[10,0,10,0]

        tw=self.getPropagation(SF,EM,EC,SM,indict,matlab)

        Start=indict['Start']
        End=indict['End']
        s_ele=SF.getElement(indict['Start'])
        e_ele=SF.getElement(indict['End'])

        if ('MQUA' in Start) and s_ele:
            if ('cor' in s_ele.__dict__) or ('corx' in s_ele.__dict__) or ('cory' in s_ele.__dict__):
                Start=Start+'.Q1'
        if ('MQUA' in End) and e_ele:
            if ('cor' in e_ele.__dict__) or ('corx' in e_ele.__dict__) or ('cory' in e_ele.__dict__):
                End=End+'.Q2'

        if s_ele and ('enable' in s_ele.__dict__):
            if s_ele.enable:
                Start=Start+'.DIAG'
            else:
                Start=Start+'.MARK'
        if e_ele and ('enable' in e_ele.__dict__):
            if e_ele.enable:
                End=End+'.DIAG'
            else:
                End=End+'.MARK'

        S=Start
        E=End

        BETXs=tw.BETX[tw.indx[S]]
        ALFXs=tw.ALFX[tw.indx[S]]
        MUXs =tw.MUX[tw.indx[S]]
        BETYs=tw.BETY[tw.indx[S]]
        ALFYs=tw.ALFY[tw.indx[S]]
        MUYs =tw.MUY[tw.indx[S]]

        BETXe=tw.BETX[tw.indx[E]]
        ALFXe=tw.ALFX[tw.indx[E]]
        MUXe =tw.MUX[tw.indx[E]]
        BETYe=tw.BETY[tw.indx[E]]
        ALFYe=tw.ALFY[tw.indx[E]]
        MUYe =tw.MUY[tw.indx[E]]

        phx=2*math.pi*(MUXe-MUXs)
        phy=2*math.pi*(MUYe-MUYs)

        R11=math.sqrt(BETXe/BETXs)*(math.cos(phx)+ALFXs*math.sin(phx))
        R12=math.sqrt(BETXe*BETXs)*math.sin(phx)
        R21=-(1.0+ALFXe*ALFXs)/math.sqrt(BETXe*BETXs)*math.sin(phx)+(ALFXs-ALFXe)/math.sqrt(BETXe*BETXs)*math.cos(phx)
        R22=math.sqrt(BETXs/BETXe)*(math.cos(phx)-ALFXe*math.sin(phx))

        R33=math.sqrt(BETYe/BETYs)*(math.cos(phy)+ALFYs*math.sin(phy))
        R34=math.sqrt(BETYe*BETYs)*math.sin(phy)
        R43=-(1.0+ALFYe*ALFYs)/math.sqrt(BETYe*BETYs)*math.sin(phy)+(ALFYs-ALFYe)/math.sqrt(BETYe*BETYs)*math.cos(phy)
        R44=math.sqrt(BETYs/BETYe)*(math.cos(phy)-ALFYe*math.sin(phy))

        return [R11,R12,R21,R22,R33,R34,R43,R44]


    def crushMadx(self):
        try:
            self.command('m1: marker;')
            self.command('m2: marker;')
            self.command('ts: sequence, refer=centre, l=10.0;')
            self.command('m1, at=2;')
            self.command('endsequence;')
            self.command('ts2: sequence, refer=centre, l=30.0;')
            self.command('ts, at=5;')
            self.command('m2, at=12;')
            self.command('endsequence;')
            self.command('seqedit, sequence=ts2;')
            self.command('flatten;')
            self.command('extract,sequence=ts2,from=m1,to=m2,newname=te;')
            self.command('endedit;')
            self.command('ts: sequence, refer=centre, l=10.0;')
            self.command('m1, at=2;')
            self.command('endsequence;')
            self.command('ts2: sequence, refer=centre, l=30.0;')
            self.command('ts, at=5;')
        except:
            'Done'

