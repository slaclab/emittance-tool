import OMType
import math
# 7) Aramis Undulator end correctors have two channels (DCR - R. Ganter)
# 8) Minor modification along the maching to get space for bellows (Email L. Schulz, 7.5.2014)
# 9) Screen added in the straigh ahead section of the final beam dumps

# Layout 8.4.1
# 1) Solenoids around Gun got correct Baugruppe (WFG and WFB)
# 2) Quadrupole in Injector spectrometer arm (S10BD01) changed to QFA type
# 3) Change Baugruppe of DHVS (Slit) to DHVS-SLIT
# 4) Apply Changes from Lothas Schult and Adriano Zandonello (email: 21.7.2014)
# 5) Cameras in Athos line have only their vacuum part installed except for one camera which is an overview camera
# 6) Change moving vacuum parts (e.g. collimator) to diagnostics group
# 7) Move Wire Scanner into Linac 3 cells 1,5,9, and 13 to separate from collimator in Linac 3
# 8) BAMs before Injector BC and in Athos line are not fully equiped and only the pick up (vacuum parts) is installed
# 9) Beam stopper after linac bunch compressor changed to type AFBC1 with corrector coil
# 10) AFDL is now 1 m long and has no tilted pole faces
# 11) Cameras in the photon beamline after the dump dipole are of type Overview
# 12) Snchrotron radiation port DSRP changed to DSRM (Synchrotron radiation monitor) and DBCM (Bunch compression monitor)
# 13) Added a synchrotron radiation monitor port after the first dipole of SATCL01
# 14) Added two coherent diffraction radiation ports (vacuum components only)

# Layout 8.5.1
# 1) Apply changes from Lothar Schulz (email 20.8.2014) 
# 2) Dumps and Stopper are in the Safety group
# 3) Adjusted ALignment Ports and Outcoupling Ports for BC1 and 2. Effective Length set to 0 cm but reserved length is 10 cm (email A. Zandonella 14.8.2014)
# 4) Removed Coherent Diffraction Radiator because position and usefulness is not clear

# Layout 8.5.2
# 1) Added Alignment LAser Ports in Athos and Aramis.
# 2) Changed section layout of beam dumps. The spectrometer dipole now belongs to the straight ahead section, e.g. SARBD01
# 3) Final Screens in SARBD01/SATBD01 are of type OV38 (changed from OV16)

# Layout 8.6.1
# 1) Implementation of multiple beamlines (Phase 1 and Phase 2)
# 2) Removal of various parts in Athos Switchyard for Phase 1 (e.g. Vert Collimator, SRM, BCM)
# 3) Self/Seeding Chicane of Aramis is now Phase 2. In Phase 1 the section is instrumented with an Undulator module
# 4) Change of the Sextupoles in BC2 10 mm upstream for the first and downstream for the second (email F. Loehl 17.10)
# 5) Indexing of SATUN22 now consistant with other undulator cells  
# 6) Added the chicane information and branching point (moved from SwissFELmagnets.py)
# 7) Branching dipoles have now the addition key 'branch' set to true
# 8) Chicanes magnets have now the common field entry 'BC' to mark them into a group
# 9) Move BAMs in SARBD01 and SATDI01 according to email by R. Ganter 16.1.2015 
# 10) Move WSC from S10MA01 to S20CB01
# 11) Move Last camera in S10MA01 30cm upstream (email. Bruno Zandonella, 5.2.15)
# 12) New Position of CDR (vacuum only thus phase 2) according to email by Bruno Zandonella, 10.2.15)

# Layout 8.7.1
# 1) Change that OMLayout is alwazs delivering one set of beamlines. With a argument in the access function build the routine
#    can implement alternative designs
# 2) Change SINEG01.MCOR220 from type SFDD to SFD1
# 3) Complete new redistributions of ICTs according to DCR50 (email M. Pedrozzi, 28.4.2015)
# 4) Correcting a 200 micron longitudinal offset for S20SY02-MBND200
# 5) Changing BAMs after Aramis and Athos to type DBAM-FS8 (formerly DBAM-FS16). Email: R. Ganter 2.6.15
# 6) Applying changes from layout optimization (email. A. Zandonella 3.6.15)
# 7) Correcting the residual transverse offset of a few nanometer in the Aramis undulator line
# 8) Changing the Wirescanner in SARUN20 to type 38mm vacuum chamber
# 9) Applying changes from A. Zandonella (email: 26.6.2015) e.g. shift of energy collimator 20 cm down stream

# Layout 8.8.1
# 1) Adjust the element in the gun section SINEG01-####190, 20 and 210 in position to get space for faraday cup
# 2) Add faraday cup as SINEG01-DFCP185
# 3) Coherent Diffraction radiation monitor DCDR are now implemented in phase 1  
# 4) Adjust TAU Monitor Position according to change in Holy List (Report from Website on 9.11.2015) 
# 5) Add vertical mover with slits into cxollimator section SARCL02-DSFV282
# 6) Adding shielding element SLOS in the Front End of Aramis

# Layout 9.0.1
# 1) Define new Athos layout with shorter undulator modules and period length of 38 mm
# 2) Define Laser acceleration in Phase 1 (Injector and Athos Switchyard)
# 3) Add Slits in Athos Switchyard for slicing at SATSY01 for phase 2
# 4) Add Gun Laser incoupling port
# 5) Rename Aramis and Athos radiation Shielding
# 6) Change Athos spectrometer magnet to same type as Aramis
# 7) Add Camera in SATCL01 for phase 1
# 8) adjust position of ICTs in SARBD01 and SARMA01 according to email by Zandonella 1.3.16) 
# 9) changed last decirper to two individual ones of 1 meter length for horizontal and vertical plane. Responsibility is now in the undulator group.
#10) Some wire scanners have a new Baugruppe, indicating an additional AL foil for beam loss measurements.
#11) Adjusting second RF cavity in SINSB03 and SINSB04 according to email by Alessandro Citterio 2.3.16

# Layout 9.0.2 (email: Adriano 4.7.2016)
# 1) Correct the Baugruppen of the Lasser Acceleration Box
# 2) Correct the WSC with AL foil in SINDI01 and s10DI01
# 3) Shift WSC in SARUN20 downstream by 30 mm for phase 1
# 4) Correct the assignment of the 1m dechirper to insertion device group


# Layout 9.1.1
# 1) Repositioning the ICTs in SARBD01 and SARMA01 (see point 8 of 9.0.1)
# 2) Adjust length of laser acceleration chamber and shift to new position (email by Silke Pfinninger, 18.8.2016)
# 3) SATCB01 and SATCB02 have no elements in phase 1 (BPMs and Quads removed)
# 4) Adjust elements around Athos dump (email by Silke Pfinninger, 18.8.2016)
# 5) Add first design of post undulator TDS (email. E. Prat, 20.7.16)
# 6) Removal of C-Band TDS in Athos line

# Layout 9.2.1
# 1) Correct the spacing in SATUN01-SATUN05 for having the same periodicity as the following sections
# 2) Shift X-bad TDS downstream to allocate space for possible ACHIP experiment.

# Layout 9.3.1
# 1) Eliminate BC alignment ports DALA150 in both bunch compressors
# 2) Move OFC quadrupole for the gun spectrometer at position z=1.6653 and new index 212 (before 310)
# 3) ACHIP Chamber in SATSY03 is now installed from phase 1 on.
# 4) Wirescanner in SARUN20 in all phases changed to type C8 type
# 5) Position correction of SARBD01-DICT030, SARMA01-DICT090 and SARUN20-DWSC010
# 6) correct position of X-band deflector to avoid conflict of overlap
# 7) Move dechirper into Athos straight section. 2m elements into formerly SATCB02 now SATCL01, 1 m long elements into the space of the former C-band deflector in SATDI01 and one 2 m element before SATCB01
# 8) Camera before Athos beam stopper is now HR in final phase 
# 9) Replace QFD at SATSY01-MQUA020/280 with QFM + Corrector magnets
#10) Remove two ICTs and one BAM from Athos beam line for the final phase
#11) Moved SFUE correctors 3 mm away from undulator (email A. Zandonella from 20.12.2016)
#12) Added ICT back into SATDI01
#13) Correction according to vacuum group (email. S.Pfinninger, 30.1.)
#14) Adding Wirescanner in SATBD01
#15) Adding Wirescanner in SATSY03 (emal. A.Zandonella, 20.1.2017)
#16) Correction of various position in Phase 1 (email. A. Zandonella: 19.1.2017)

# Layout 9.3.2
# 1) Applied some fine correction (email A. Zandonella, 8.2.2017)

# Layout 10.0.1
# 1) Omitting phase 1. Now only the final phase is given for elements where funding exists.
# 2) New Layout for chicane for two color operation in Athos and Aramis.
# 3) Chicane magnets AFSS are 30 cm long now (formerly 36 cm)
# 4) change index of SATDI wirescanner to 65

# Layout 10.1.1
# 1) Reintroducing different phases: alt=0 is current state, alt=1 is a near future state/possible modification, alt=2 is the final layout
# 2) Change correctors from SINLH03-DQUA040/080 to 030/060
# 3) Change naming of permanent and skew magnets: MQUA->MQUP, MBND -> MBNP and MQUA -> MQSK
# 4) Move two color chicane in ARAMIS from SARUN08 to SARUN09
# 5) Change number of correctors of UE38 from 1 to 2
# 6) Add some fine correction in the ATHOS undulator cells and tow color chicane positions

# Layout 10.1.2
# Synchronization of the holy list with Adriano/Hubert (email 4.6.18)
# 1) Change energy collimator from DCOL to VCOL
# 2) Temporary installation of the variable gap dechirper in SINSB05 with some change in quadrupole and BPM position in SINSB05 and SINSB04
# 3) Correction of the beam stopper dump in SATBD01, which should be after the permanent dipole magnet (index change from 205 to 305)
# 4) Reduce number of X-band deflector station to one, and shift it (and space for the other) by 22 cm against the beam (upstream): email R. Ganter 23.1.18 and confirmation by  D. Hauenstein
# 5) Place 6 dechirper into Athos line, 4 in the SATCL02 section and 2 more in SATMA01

# Layout 10.1.3
# 1) Remove SATDI01-MQUA310 and SATDI-DBPM320 to SATDI01-MQUA300 and SAT-DBPM310
# 2) Take out Athos ACHIP Box in current version (alt=0)

# Layout 10.2.1
# 1) Moving planned layout (alt=1) to current
# 2) Move first QFM magnet in SATSY01 35 mm upstream
# 3) Correct for wrong calculation of the SINSB04 cell
# 4) Enables the ict in SATDI01-DICT020 for all phases
# 5) Added Athos ACHIP in 'Phase planned' (installation november shutdown 2018)
# 6) added two slit dechirper in SARUN16 (finanzed by CROSS proposal)
# 7) Move of SINDI01-DSCR080, replacing SINDI02-MQUA070
# 8) Move of SINLH03 screen to SINSB05 after the dechirper
# 9) Correct septum length from 1 m to 0.76 m

# Layout 10.2.2
# 1) pushed the two screen changes and ACHIP box from planned to current
# 2) Fine correction of the changed screen of change in 10.2.1 according to D. Hauensteins email (28.11)
# 3) Changes of BPM position in SATMA02 (email D>Hauenstein 28.11)
# 4) Added a C16 BAM to Athos in SATBD01
# 5) Placed X-band deflector in Athos in new section SATXB01

# Layout 10.2.3
# 1) Screen SINLH03-DSCR070 removed in phase current since it was move to SINSB05
# 2) Change correct length of 8 mm BAM to 100 mm
# 3) Replace BAM in SAT from 16 mm to 8 mm
# 4) Correct dechirper position in Athos according to input from Silke Pfiffinger
# 5) Correct Wire Scanner Position in final phase in SARUN09
# 6) Moved dechirpers after Aramis undulator from SARUN16 to SARUN18 after input from E. PRat
# 7) Added dechirpers from CROSS proposal in S30CB15
# 8) Possition changes of sextupoles and wirescanner in SARCL02 according to email D. Hauenstein 26.3
# 9) First implementation of seeding for the HERO project. This applies mostly to a reconfiguration of SATDI01 and the addition of a second two color chicane in SATUN05

# Layout 10.3.1
# 1) Moved final layout of Athos into planned layout
# 2) Included in the final layout of Athos HERO and EEHG first iteration.
# 3) Renamed XBAND cavity in Athos back to section SARMA02 (email by Romain, April 19)
# 4) Change in Dechirper position in SARUN18 (email D. HAuenstein 17th April 19)

# Layout 10.3.2
# 1) Add Athos beam dump SATBD02 to all phases
# 2) Verschiebung der Dechirper in S30CB15 (email. S. Pfinninger, 14.10.19)
# 3) Verschiebung der TDS in SATMA02 by 6 cm downstream (email. S. Pfinninger, 14.10.19)
# 4) Verschiebung des BAMS in SATBD01 by a small margin upstream (email. S. Pfinninger, 14.10.19)
# 5) Change Dipole type in the large EEHG chicane to AFBC3 to get maximum R56 of 12 mm for an angle of 2.3 degree
# 6) Added a power supply channel to the Athos CHIC-chicanes.
# 7) The phase final of SATDI01 will be copied over to phase planned
# 8) In the current phase there will be only 4 Athos undulator modules installed
# 9) Increase apeture from the large Athos chicane to the end of the modulator to 16 mm (before the undulator) and 8 mm after before going back to 5 mm.
# 10) Removed last sextupole in SATCL01 and moved DALA upstream
# 11) Move the periodic lattice after Athos stopper by 50 cm downstream and compensate for shorter triplet structures.
# 12) Second dechirper girder in SATCL02 moved into 'phase current', first in SATCL02 and the one in SATMA01 in 'phase planned'
# 13) Dechirper in SARUN18 comes in 'phase current'
# 14) phase current: LAst 4 Undulators and phase shifter, 'phase planned' last 8 undulators but all phase shifter in SATUN
# 15) X-Band TCAV only in phase planned and higher.
# 16) Shift of BMP sin S20SY03 and the placement of a screen, latter only from phase planned on
# 17) Remove SATDI01-DWSC290 out of phase current and planed (email R. Ganter 29.10.2019)

# Layout 10.4.2
# 1) Adding undulator SATUN12 to SATUN18 up till sep 2020
# 2) Adding back again the second RF structure for the X-band deflector in Athos
# 3) Adding CDR Monitor in SATSY02 for 'phase final'
# 4) Adding CDR Monitor in S20SY03 for 'phase final'
# 5) Adding BPM and Quadrupole before SATCL02-UDCP300
# 6) Adding Dechirper in SATMA02
# 7) Increase number of periods of bother modulator from 8 to 9
# 8) Increase length of EEHG chicane in SAT by 4 cm (last dipole shifts by 4 cm, the inner by 2 cm)
# 9) Change order of BPMs and Quads around EEHG chicane to allow for the vacuum chamber and 9 period modulator
# 10) Reduced spacing of 3 quadrupoles between EEHG chicane and modulator in SATMA01 to accomidate 9 periods
# 11) Correct position of SATDI01-DBAM
# 12) Correct the position of SARMA01-DBCM030 which is build  before the correct 020. Idex swapped.
# 13) Added Dechirper 100 and 200 in SATCL02 


# Layout 10.4.3
# 1) Remove Dechirper in SINSB05
# 2) Add Dechirper in S30CB15
# 3) Add Dechirper in SATMA01
# 4) Add Undulator in SATUN10
# 5) Renamed quadrupole and BPM in SATUN05 to 410 and 420 indec respectively

class SwissFEL:
    def __init__(self,alt=0):
        self.alt=alt
        self.Version='10.4.3'

    def Types(self,TM):
# type definitions for the SwissFEL lattice        
        
        #define common Undulator
        indict={'Type':'Undulator','Length':4,'K':1.2,'ku':4*math.asin(1)/0.015,'cor':0,'Baugruppe':'U15'}
        TM.define('U15',indict)
        indict={'Type':'Undulator','Length':2,'K':1.5,'ku':4*math.asin(1)/0.04,'corx':0,'cory':0,'Baugruppe':'UE38'}
        TM.define('UE38',indict)  
        indict={'Type':'Undulator','Length':0.06,'Tag':'UPHS','Baugruppe':'U15-PS'}
        TM.define('PSU15',indict)
        indict={'Type':'Undulator','Length':0.20,'Tag':'UDLY','Baugruppe':'UE38-DELAY'}
        TM.define('PSUE38',indict)
        indict={'Type':'Undulator','Length':0.20,'K':25, 'ku':4*math.asin(1)/0.2, 'Tag':'UMOD','Baugruppe':'U200'}
        TM.define('UMOD',indict)
        indict={'Type':'Undulator','Length':0.4,'K':2.27,'ku':4*math.asin(1)/0.05,'Baugruppe':'U50','Power':20e3,'Waist':400e-6}
        TM.define('U50',indict)


        # define common quadrupole38
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'corx':0,'cory':0,'Baugruppe':'QFD'}
        TM.define('QFD',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'corx':0,'cory':0,'Baugruppe':'QFDM'}       
        TM.define('QFDM',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.15,'corx':0,'cory':0,'Baugruppe':'QFDM'}       
        TM.define('QFDM-short',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'Baugruppe':'QFD'}
        TM.define('QFD-noCor',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'Baugruppe':'QFDM'}
        TM.define('QFDM-noCor',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'Tilt':math.asin(1)/2,'Tag':'MQSK','Baugruppe':'QFD-SKEW'}  
        TM.define('QFS',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'Baugruppe':'QFA'}
        TM.define('QFA',indict)
        indict={'Type':'Quadrupole','Length':0.3,'LengthRes':0.7,'Baugruppe':'QFM'}
        TM.define('QFM',indict)
        indict={'Type':'Quadrupole','Length':0.3,'LengthRes':0.5,'Baugruppe':'QFM'}
        TM.define('QFM-short',indict)
        indict={'Type':'Quadrupole','Length':0.3,'LengthRes':0.3,'Baugruppe':'QFM'}
        TM.define('QFM-veryshort',indict)
        indict={'Type':'Quadrupole','Length':0.15,'LengthRes':0.25,'Tilt':math.asin(1)/2,'Tag':'MQSK','Baugruppe':'QFA-SKEW'}  
        TM.define('QFAS',indict)
        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.08,'corx':0,'cory':0,'Baugruppe':'QFF'}
        TM.define('QFF',indict)
#        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.08,'corx':0,'cory':0,'Baugruppe':'QFG'}
#        TM.define('QFG',indict)
        indict={'Type':'Quadrupole','Length':0.04,'LengthRes':0.04,'Tag':'MQUP','Baugruppe':'QFU','Overlap':1}
        TM.define('QFU',indict)
        indict={'Type':'Quadrupole','Length':0.015,'LengthRes':0.03,'Tag':'MQUP','Baugruppe':'QFUE'}   
        TM.define('QFUE',indict)
        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.10,'Baugruppe':'QFC'}
        TM.define('QFC',indict) 
        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.10,'Tilt':math.asin(1)/2,'Tag':'MQSK','Baugruppe':'QFC-SKEW'} 
        TM.define('QFCS',indict)
        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.10,'Baugruppe':'QFB'}
        TM.define('QFB',indict)
        indict={'Type':'Quadrupole','Length':0.08,'LengthRes':0.10,'Tilt':math.asin(1)/2,'Tag':'MQSK','Baugruppe':'QFB-SKEW'} 
        TM.define('QFBS',indict)
        indict={'Type':'Quadrupole','Length':0.16,'LengthRes':0.16,'Baugruppe':'QFCOR'}
        TM.define('QFCOR',indict)
        indict={'Type':'Quadrupole','Length':0.16,'LengthRes':0.16,'Tilt':math.asin(1)/2,'Tag':'MQSK','Baugruppe':'QFCOR-SKEW'} 
        TM.define('QFCORS',indict)
        indict={'Type':'Quadrupole','Length':0.1,'LengthRes':0.1,'Baugruppe':'QPM1'}
        TM.define('QPM1',indict)
        indict={'Type':'Quadrupole','Length':0.1,'LengthRes':0.1,'Baugruppe':'QPM2'}
        TM.define('QPM2',indict)

        
        indict={'Type':'Sextupole','Length':0.08,'LengthRes':0.10,'Baugruppe':'HFA'}
        TM.define('HFA',indict)
        indict={'Type':'Sextupole','Length':0.08,'LengthRes':0.10,'Baugruppe':'HFB'}
        TM.define('HFB',indict)
        
        indict={'Type':'Solenoid','Length':0.75,'Baugruppe':'WFS'}
        TM.define('WFS',indict)
        indict={'Type':'Solenoid','Length':0.03,'Baugruppe':'WFB'}
        TM.define('WFB',indict)
        indict={'Type':'Solenoid','Length':0.26,'Baugruppe':'WFG'}
        TM.define('WFG',indict)
 
        
        # define common dipoles
        indict={'Type':'Dipole','Length':0.25,'Baugruppe':'SHA'}
        TM.define('SHA',indict)
        indict={'Type':'Dipole','Length':0.12,'cor':0,'Baugruppe':'AFL'}
        TM.define('AFL',indict)
        indict={'Type':'Dipole','Length':0.25,'cor':0,'Baugruppe':'AFBC1'}
        TM.define('AFBC1',indict)
        indict={'Type':'Dipole','Length':0.5,'cor':0,'Baugruppe':'AFBC3'}
        TM.define('AFBC3',indict)
        indict={'Type':'Dipole','Length':0.5,'Baugruppe':'AFBC3'}
        TM.define('AFBC3-noCor',indict)
        indict={'Type':'Dipole','Length':0.76,'Baugruppe':'AFS'}
        TM.define('AFS',indict)
        indict={'Type':'Dipole','Length':0.3,'cor':0,'Baugruppe':'AFSS'}
        TM.define('AFSS',indict)
        indict={'Type':'Dipole','Length':2,'Tilt':math.asin(1),'Baugruppe':'AFD1'}
        TM.define('AFD1',indict)
        indict={'Type':'Dipole','Length':1.1,'Tilt':math.asin(1),'Baugruppe':'AFD2'}
        TM.define('AFD2',indict)
        indict={'Type':'Dipole','Length':0.3,'Tag':'MBNP','Baugruppe':'AFP1'}  
        TM.define('AFP1',indict)
        indict={'Type':'Dipole','Length':1.0,'cor':0,'Baugruppe':'AFDL'}
        TM.define('AFDL',indict)
        
        
        # define common correctors
        indict={'Type':'Corrector','Length':1,'Tag':'MKAC','cory':0,'Baugruppe':'RES-KICKER-AC'}
        TM.define('RESKICKAC',indict)
        indict={'Type':'Corrector','Length':0.21,'Tag':'MKDC','cory':0,'Baugruppe':'RES-KICKER-DC'}
        TM.define('RESKICKDC',indict)
        indict={'Type':'Corrector','Length':0.05,'LengthRes':0.1,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFC'}
        TM.define('SFC',indict)
        indict={'Type':'Corrector','Length':0.2,'LengthRes':0.3,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFQFM'}
        TM.define('SFQFM',indict)
        indict={'Type':'Corrector','Length':0.2,'LengthRes':0.2,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFQFM'}
        TM.define('SFQFM-short',indict)
        indict={'Type':'Corrector','Length':0.015,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFDD'}
        TM.define('SFDD',indict)
        indict={'Type':'Corrector','Length':0.015,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFD1'}
        TM.define('SFD1',indict)
        indict={'Type':'Corrector','Length':0.05,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFC'}
        TM.define('SFC',indict)
        indict={'Type':'Corrector','Length':0.005,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFB'}
        TM.define('SFB',indict)
        indict={'Type':'Corrector','Length':0.06,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFU'}
        TM.define('SFU',indict)
        indict={'Type':'Corrector','Length':0.01,'Tag':'MCOR','corx':0,'cory':0,'Baugruppe':'SFUE'}
        TM.define('SFUE',indict)


        
        # define common RF structure
        indict={'Type':'RF','Length': 0.2,'LengthRes':0.25,'Band':'S','Tag':'RGUN','Baugruppe':'PSI-GUN'}
        TM.define('GUN',indict)
        indict={'Type':'RF','Length': 1.978045,'LengthRes':2.05,'Band':'C','Baugruppe':'C-BAND-ACC'}
        TM.define('TW Cav C-Band',indict)
        indict={'Type':'RF','Length': 4.0830,'LengthRes':4.15,'Band':'S','Baugruppe':'S-BAND-ACC'}
        TM.define('TW Cav S-Band',indict)
        indict={'Type':'RF','Length': 0.75,'LengthRes':0.965,'Band':'X','Baugruppe':'X-BAND-ACC'}
        TM.define('TW Cav X-Band',indict)
        indict={'Type':'RF','Length': 0.240,'LengthRes':0.441,'Band':'S','Tag':'RTDS','Baugruppe':'S-BAND-TDS'}
        TM.define('TDS S-Band',indict)
        indict={'Type':'RF','Length': 1.9,'LengthRes':2.0,'Band':'C','Tag':'RTDS','Baugruppe':'C-BAND-TDS'}
        TM.define('TDS C-Band',indict)
        indict={'Type':'RF','Length': 1.20,'LengthRes':1.2,'Band':'X','Tag':'RTDS','Baugruppe':'X-BAND-TDS'}
        TM.define('TDS X-Band',indict)
        
        # define diagnostics template
        indict={'Type':'Diagnostic','Length':0.10,'Baugruppe':'DBPM-C16'}
        TM.define('DBPM-C16',indict)
        indict={'Type':'Diagnostic','Length':0.10,'Baugruppe':'DBPM-C8'}
        TM.define('DBPM-C8',indict)
        indict={'Type':'Diagnostic','Length':0.08,'Baugruppe':'DBPM-C5'}
        TM.define('DBPM-C5',indict)
        indict={'Type':'Diagnostic','Length':0.255,'Baugruppe':'DBPM-C38'}
        TM.define('DBPM-C38',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-OV16'}
        TM.define('DSCR-OV16',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-OV38'}
        TM.define('DSCR-OV38',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-HR16'}
        TM.define('DSCR-HR16',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-HR16-VO'}
        TM.define('DSCR-HR16-VACONLY',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-HR8'}
        TM.define('DSCR-HR8',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-HR8-TEMP'}
        TM.define('DSCR-HR8-P1-OV16',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-HR38'}
        TM.define('DSCR-HR38',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Seval': 0.0685, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-LH16'}
        TM.define('DSCR-LH16',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-LE16'}
        TM.define('DSCR-LE16',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-BC120'}
        TM.define('DSCR-BC120',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-LE38R'}
        TM.define('DSCR-LE38R',indict)
        indict={'Type':'Diagnostic','Length':0.126,'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-LE38'}
        TM.define('DSCR-LE38',indict)
        indict={'Type':'Diagnostic','Length':0.085,'Tag':'DHVS','Baugruppe':'DHVS-SLIT'}
        TM.define('DHVS',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DCDR','Baugruppe':'DCDR'}
        TM.define('DCDR',indict)


        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DSRM','Baugruppe':'DSRM-VIS'}
        TM.define('DSRM-VIS',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DSRM','Baugruppe':'DSRM-UV'}
        TM.define('DSRM-UV',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DBCM','Baugruppe':'DBCM-THZ'}
        TM.define('DBCM-THZ',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DBCM','Baugruppe':'DBCM-IR'}
        TM.define('DBCM-IR',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DALA','Baugruppe':'DALA'}
        TM.define('DALA',indict)


        indict={'Type':'Diagnostic','Length':0.02, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DSCR-LA'}
        TM.define('DSCR-LA',indict)
        indict={'Type':'Diagnostic','Length':0.02, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DLAC-TARGET'}
        TM.define('DLAC-TARGET',indict)
        indict={'Type':'Diagnostic','Length':0.02, 'Sx':1,'Sy':1,'Tag':'DSCR','Baugruppe':'DCDR-LA'}
        TM.define('DCDR-LA',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DLAC','Baugruppe':'DLAC-LL16'}        
        TM.define('DLAC-LL16',indict)




        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DWSC','Baugruppe':'DWSC-C16'}        
        TM.define('DWSC-C16',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DWSC','Baugruppe':'DWSC-C16-AL'}        
        TM.define('DWSC-C16-AL',indict)
        indict={'Type':'Diagnostic','Length':0.15,'Sx':1,'Sy':1,'Tag':'DWSC','Baugruppe':'DWSC-C38'}
        TM.define('DWSC-C38',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Sx':1,'Sy':1,'Tag':'DWSC','Baugruppe':'DWSC-C8'}
        TM.define('DWSC-C8',indict)
        indict={'Type':'Diagnostic','Length':0.137,'Sx':1,'Sy':1,'Tag':'DWSC','Apery':0,'Baugruppe':'DWSC-C16-COL'}
        TM.define('DWSC-C16-COL',indict)
        indict={'Type':'Diagnostic','Length':0.075,'Cx':0,'Cy':0,'Cz':1,'Tag':'DBAM','Baugruppe':'DBAM-PS16'}
        TM.define('DBAM-PS16',indict)
        indict={'Type':'Diagnostic','Length':0.075,'Cx':0,'Cy':0,'Cz':1,'Tag':'DBAM','Baugruppe':'DBAM-FS16'}
        TM.define('DBAM-FS16',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Cx':0,'Cy':0,'Cz':1,'Tag':'DBAM','Baugruppe':'DBAM-FS8'}
        TM.define('DBAM-FS8',indict)
        indict={'Type':'Diagnostic','Length':0.04,'Cx':0,'Cy':0,'Cz':0,'Tag':'DICT','Baugruppe':'DICT-C16'}
        TM.define('DICT-C16',indict)
        indict={'Type':'Diagnostic','Length':0.04,'Cx':0,'Cy':0,'Cz':0,'Tag':'DICT','Baugruppe':'DICT-C38'}
        TM.define('DICT-C38',indict)
        indict={'Type':'Diagnostic','Length':0.06,'Cx':0,'Cy':0,'Cz':0,'Tag':'DICT','Baugruppe':'DICT-C38-GUN'}
        TM.define('DICT-C38-GUN',indict)
        indict={'Type':'Diagnostic','Length':0.1,'Cx':0,'Cy':0,'Cz':0,'Tag':'DWCM','Baugruppe':'DWCM-C38'}
        TM.define('DWCM-C38',indict)
        indict={'Type':'Diagnostic','Length':0.15,'Cx':0,'Cy':0,'Sz':1,'Tag':'DTAU','Baugruppe':'DTAU'}
        TM.define('DTAU',indict)
        indict={'Type':'Diagnostic','Length':0.15,'Cx':0,'Cy':0,'Sz':1,'Tag':'DEOM','Baugruppe':'DEOM'}
        TM.define('DEOM',indict)
        indict={'Type':'Diagnostic','Length':0.126,'Cx':0,'Cy':0,'Sz':1,'Tag':'DFCP','Baugruppe':'DFCP-GUN'}
        TM.define('DFCP',indict)
        
        # define x-ray diagnostic
        indict={'Type':'Photonics','Length':0.15,'Sx':1,'Sy':1,'Tag':'PPRM','Baugruppe':'PPRM'}
        TM.define('PPRM-C38',indict)
        indict={'Type':'Photonics','Length':0.15,'Tag':'PCRY','Baugruppe':'BRAGG-CRYSTAL'}
        TM.define('PCRY-C38',indict)


        
        # define aperture templates (moving apertures are part of diagnostics and diagnostics)
        indict={'Type':'Diagnostic','Length':0.137,'Tag':'DCOL','Apery':0,'Baugruppe':'VERT-COL'}
        TM.define('COL-TR-16',indict)
        indict={'Type':'Diagnostic','Length':0.5,'Tag':'VCOL','Aperx':0,'Baugruppe': 'E-COL'}
        TM.define('COL-Energy',indict)
        indict={'Type':'Undulator','Length':1,'Tag':'UDCP','gap':20e-3,'offset':0,'Aperx':0,'Baugruppe': 'DECHIRPER-V'}
        TM.define('COL-Dechirper-V',indict)
        indict={'Type':'Undulator','Length':1,'Tag':'UDCP','gap':20e-3,'offset':0,'Aperx':0,'Baugruppe': 'DECHIRPER-H'}
        TM.define('COL-Dechirper-H',indict)
        indict={'Type':'Diagnostic','Length':0.01,'Tag':'DCOL','Aperx':0,'Baugruppe':'BC-SCRAPER'}
        TM.define('COL-BC-Scraper',indict)  
        indict={'Type':'Diagnostic','Length':0.01,'Tag':'DSFH','Baugruppe':'SLOT-FOIL-H'}
        TM.define('BC-SlotFoil-H',indict)
        indict={'Type':'Diagnostic','Length':0.15,'Tag':'DSFV','Baugruppe':'SLOT-FOIL-V'}
        TM.define('BC-SlotFoil-V',indict)
        indict={'Type':'Vacuum','Length':0.085,'Tag':'VLAP','Baugruppe':'LH-LASER-PORT'}
        TM.define('LH-Laserport',indict)
        indict={'Type':'Vacuum','Length':0.1,'Tag':'VLAP','Baugruppe':'LC-GUN-IN'}
        TM.define('GUN-Laserport',indict)


        # Beam Stopper and Dumps
        indict={'Type':'Vacuum','Length':1,'Tag':'SDMP','Baugruppe':'BEAM-DUMP-SIN'}
        TM.define('Beam-Dump-Sin',indict)
        indict={'Type':'Vacuum','Length':1,'Tag':'SDMP','Baugruppe':'BEAM-DUMP-S10'}
        TM.define('Beam-Dump-S10',indict)
        indict={'Type':'Vacuum','Length':1,'Tag':'SDMP','Baugruppe':'BEAM-DUMP-SAR'}
        TM.define('Beam-Dump-Sar',indict)
        indict={'Type':'Vacuum','Length':1,'Tag':'SDMP','Baugruppe':'BEAM-DUMP-SAT'}
        TM.define('Beam-Dump-Sat',indict)
        indict={'Type':'Vacuum','Length':2.5,'Tag':'SSTP','Baugruppe':'BEAM-STOP-SAR'}
        TM.define('Beam-Stopper-Sar',indict)
        indict={'Type':'Vacuum','Length':2.5,'Tag':'SSTP','Baugruppe':'BEAM-STOP-SAT'}
        TM.define('Beam-Stopper-Sat',indict)
        indict={'Type':'Vacuum','Length':1.6,'Tag':'SSTP','Baugruppe': 'BEAM-STOP-S10'}
        TM.define('Beam-Stopper-S10',indict)
        indict={'Type':'Vacuum','Length':1.5,'Tag':'SLOS','Baugruppe': 'SHIELD-FE'}
        TM.define('FE-Shielding',indict)

        #Laser Acceleration
        indict={'Type':'Diagnostic','Length':2.13,'Tag':'DLAC','Aperx':0,'Baugruppe':'LASER-ACC-BOX'}
        TM.define('Laser-Acceleration',indict)  


        # define branching point
        indict={'Type':'Marker','Length':0.0,'Tag':'MKBR','Baugruppe': 'BRANCHING-POINT'}
        TM.define('MKBR',indict)


     
    def Lines(self,TM):
# defines common lines in the lattice                 
        
        # define sequence templates
        
        # Aramis
        a0={'Length':4.75}
        a1cor={'Element':'SFU','sRef':0.105+0.026,'Ref':'absolute','index':10,'Option':{'MADthin':1,'MADshift':-0.02}}
        a1={'Element':'QFU','sRef':0.115,'Ref':'absolute','index':20}
        a2={'Element':'U15','sRef':0.0575,'Ref':'relative','index':30}
        a3cor={'Element':'SFU','sRef':0.0475-0.026,'Ref':'relative','index':40,'Option':{'MADthin':1,'MADshift':-0.02}}        
        a3={'Element':'QFU','sRef':4.27,'Ref':'absolute','index':50}
        a4={'Element':'PSU15','sRef':0.035,'Ref':'relative','index':60}
        a5={'Element':'DBPM-C8','sRef':0.078,'Ref':'relative','index':70}
        a6={'Element':'QFF','sRef':0.06,'Ref':'relative','index':80}
        seq=[a0,a1cor,a1,a2,a3cor,a3,a4,a5,a6]
        TM.define('U15-Cell',seq) 
        a5alt={'Element':'DBPM-C8','sRef':0.173,'Ref':'relative','index':70}
        seq=[a0,a1cor,a1,a2,a3cor,a3,a5alt,a6]
        TM.define('U15-Cell-Last',seq)  
        a5alt={'Element':'DBPM-C8','sRef':4.483,'Ref':'relative','index':70}
        seq=[a0,a5alt,a6]
        TM.define('U15-Cell-Empty',seq)


        # Athos

        a0={'Length':2.8}
        a1={'Element':'QFUE','sRef':0.035,'Ref':'relative','index':10}
        a2={'Element':'SFUE','sRef':0.0095,'Ref':'relative','index':20}
        a3={'Element':'UE38','sRef':0.038,'Ref':'relative','index':30}
        a4={'Element':'SFUE','sRef':0.038,'Ref':'relative','index':40}
        a5={'Element':'QFUE','sRef':0.0095,'Ref':'relative','index':50}
        a6={'Element':'PSUE38','sRef':0.035+0.01,'Ref':'relative','index':60}
        a7={'Element':'DBPM-C5','sRef':0.035-0.01+0.00775,'Ref':'relative','index':70}
        a8={'Element':'QFF','sRef':0.06025-0.00775+0.005,'Ref':'relative','index':80}

        seq=[a0,a1,a2,a3,a4,a5,a6,a7,a8]
        TM.define('UE38-Cell',seq)          # normal line                
        a7alt={'Element':'DBPM-C5','sRef':0.27+0.00775,'Ref':'relative','index':70}
        seq=[a0,a1,a2,a3,a4,a5,a7alt,a8]
        TM.define('UE38-Cell-Last',seq)     # line without phase shifter 
        a6alt={'Element':'PSUE38','sRef':2.21+0.035+0.01,'Ref':'relative','index':60}
        seq=[a0,a6alt,a7,a8]
        TM.define('UE38-Cell-PS',seq)       # empty cell with only phase shifter
        a7alt={'Element':'DBPM-C5','sRef':2.48+0.00775,'Ref':'relative','index':70}
        seq=[a0,a7alt,a8]
        TM.define('UE38-Cell-Empty',seq)   # fully empty cell 

        a7_400={'Element':'DBPM-C5','sRef':2.48+0.00775,'Ref':'relative','index':410}
        a8_400={'Element':'QFF','sRef':0.06025-0.00775+0.005,'Ref':'relative','index':420}
        seq=[a0,a7_400,a8_400]
        TM.define('UE38-Cell-Empty-400',seq)   # fully empty cell 


        # C-banLinac
  
        a0={'Length': 9.8}
        a1={'Element':'TW Cav C-Band','sRef':0.035,'Ref':'relative','index':100}
        a2={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':200}
        a3={'Element':'DBPM-C16','sRef':0.080613,'Ref':'relative','index':220}
        a4={'Element':'QFDM','sRef':0.049,'Ref':'relative','index':230}
        a5={'Element':'TW Cav C-Band','sRef':0.252075,'Ref':'relative','index':300}
        a6={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':400}
        a7={'Element':'DBPM-C16','sRef':0.099538,'Ref':'relative','index':420}
        a8={'Element':'QFDM','sRef':0.049,'Ref':'relative','index':430}
        a9={'Element':'DWSC-C16','sRef':0.019,'Ref':'relative','index':440}
        seq=[a0,a1,a2,a3,a4,a5,a6,a7,a8]
        TM.define('CB-Lin1-Cell',seq)
        seq=[a0,a1,a2,a3,a4,a5,a6,a7,a8,a9]
        TM.define('CB-Lin1-Cell-WSC',seq)
        a0alt={'Length': 9.135}
        seq=[a0alt,a1,a2,a3,a4,a5,a6]
        TM.define('CB-Lin1-Cell-Last',seq)
        
        a0={'Length': 9.8}
        a1={'Element':'TW Cav C-Band','sRef':0.035,'Ref':'relative','index':100}
        a2={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':200}
        a3={'Element':'DBPM-C16','sRef':0.080613,'Ref':'relative','index':220}

        a3empty={'Element':'DBPM-C16','sRef':4.265,'Ref':'relative','index':220}
        a4={'Element':'QFD','sRef':0.049,'Ref':'relative','index':230}
        a5={'Element':'COL-TR-16','sRef':0.019,'Ref':'relative','index':240}
        a6={'Element':'TW Cav C-Band','sRef':0.096075,'Ref':'relative','index':300}
        a7={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':400}
        a8={'Element':'DBPM-C16','sRef':0.099538,'Ref':'relative','index':420}
        a8empty={'Element':'DBPM-C16','sRef':4.501,'Ref':'relative','index':420}
        a9={'Element':'QFD','sRef':0.049,'Ref':'relative','index':430}
        a10={'Element':'COL-TR-16','sRef':0.019,'Ref':'relative','index':440}
        seq=[a0,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]
        TM.define('CB-Athos-Cell',seq)
        seq=[a0,a3empty,a4,a8empty,a9]
        TM.define('CB-Athos-Cell-empty',seq)
        
        
        a0={'Length': 9.1}
        a1={'Element':'TW Cav C-Band','sRef':0.035,'Ref':'relative','index':100}
        a2={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':200}
        a3={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':300}
        a4={'Element':'TW Cav C-Band','sRef':0.049387,'Ref':'relative','index':400}
        a5={'Element':'DBPM-C16','sRef':0.081839,'Ref':'relative','index':420}
        a6={'Element':'QFD','sRef':0.049,'Ref':'relative','index':430}
        a7={'Element':'DWSC-C16','sRef':0.019,'Ref':'relative','index':440}
       
        
        seq=[a0,a1,a2,a3,a4,a5,a6]
        TM.define('CB-Lin2-Cell',seq)
        seq=[{'Length': 8.435},a1,a2,a3,a4]
        TM.define('CB-Lin2-Cell-Last',seq)
        seq=[a0,a1,a2,a3,a4,a5,a6,a7]
        TM.define('CB-Lin2-Cell-WSC',seq)

        seq=[a0,a1,a2,a3,a4,a5,a6]
        TM.define('CB-Lin3-Cell-incomplete',seq)

        #s-Band 
        a0={'Length': 11.0}
        a1={'Element':'TW Cav S-Band','sRef':0.155,'Ref':'relative','index':100}
        a2={'Element':'DBPM-C16','sRef':0.835,'Ref':'relative','index':120}
        a3={'Element':'QFDM','sRef':0.03,'Ref':'relative','index':130}
        a4={'Element':'TW Cav S-Band','sRef':0.135-0.0016,'Ref':'relative','index':200}
        a5={'Element':'DBPM-C16','sRef':0.835+0.0016,'Ref':'relative','index':220}
        a6={'Element':'QFDM','sRef':0.03,'Ref':'relative','index':230}
        
        # replaces a3
        a3alt1={'Element':'DSCR-HR16','sRef':0.235,'Ref':'relative','index':110}
        a3alt2={'Element':'DBPM-C16','sRef':0.463,'Ref':'relative','index':120}
        a3alt3={'Element':'QFDM','sRef':0.03,'Ref':'relative','index':130}

        #
        a2alt1={'Element':'DBPM-C16','sRef':0.837+4.15+0.153,'Ref':'relative','index':120}
        a2alt2={'Element':'DBPM-C16','sRef':0.837+4.15+0.133,'Ref':'relative','index':220}


        a0alt={'Length': 11.6}
        a5alt1={'Element':'DBPM-C16','sRef':0.835+0.0016+0.57450,'Ref':'relative','index':220}
        
        seq=[a0,a1,a2,a3,a4,a5,a6]
        TM.define('SB-Lin-Cell-Mid',seq)
        seq=[a0,a1,a3alt1,a3alt2,a3alt3,a4,a5,a6]
        TM.define('SB-Lin-Cell-First',seq)
        seq=[a0,a2alt1,a3,a2alt2,a6]
        TM.define('SB-Lin-Cell-Empty',seq)

        seq=[a0alt,a1,a2,a3,a4,a5alt1,a6]
        TM.define('SB-Lin-TMP-DECHIRPER',seq)


    def build(self):
        
        #initiate the TypeManage
        TM = OMType.TypeManager()
        self.Types(TM)
        self.Lines(TM)
                
        #-----------------------------------------------
        # define actual layout




        #---------- short branch for gun dump
        BD01=OMType.LineContainer('BD01',0)
        BD01.append(TM.generate('DSCR-LE38R',10),0.489+0.097811,'relative')
        BD01.append(TM.generate('Beam-Dump-Sin',15),0.165+0.165-0.017,'relative')

        InjectorDump=OMType.LineContainer('IN')
        InjectorDump.append(BD01,0,'relative')



        #---------- elements of injector

        Lsec=3.6039       
        angle=0  # default angle
        EG01=OMType.LineContainer('EG01',Lsec)
        EG01.append(TM.generate('WFB',10),0,'absolute')
        EG01.append(TM.generate('GUN',100),0.1,'absolute')
        EG01.append(TM.generate('SFB',120,{'Overlap':1}),0.265,'absolute')
        EG01.append(TM.generate('WFG',130,{'Overlap':1}),0.27,'absolute')
        EG01.append(TM.generate('QFCOR',140,{'Overlap':1}),0.32,'absolute')
        EG01.append(TM.generate('QFCORS',150,{'Overlap':1}),0.32,'absolute')
        EG01.append(TM.generate('SFB',160,{'Overlap':1}),0.054,'relative')
        EG01.append(TM.generate('DWCM-C38',170),0.143,'relative')
        EG01.append(TM.generate('SFDD',180),0.07-0.0002,'relative')
        EG01.append(TM.generate('GUN-Laserport',185),0.2397,'relative')
        EG01.append(TM.generate('DFCP',185),0.0,'relative')
        EG01.append(TM.generate('DSCR-LE38',190),0.1445-0.126,'relative')
        EG01.append(TM.generate('SFDD',200),1.3725+0.0615-0.06+0.1445,'absolute')
        EG01.append(TM.generate('DICT-C38-GUN',210),0.07+0.0375-0.064,'relative')
        EG01.append(TM.generate('QFC',212),0.123-0.0547,'relative')
        EG01.append(TM.generate('DICT-C38',215),0.4-0.055+0.062-0.0845-0.223+0.0547,'relative')
        EG01.append(TM.generate('SFD1',220),0.6894-0.45-0.0425-0.0795,'relative')
        EG01.append(TM.generate('SHA',300, {'angle':angle,'design_angle':30,'e1':0.5,'e2':0.5,'branch':True}),0.035,'relative')
        EG01.append(TM.generate('MKBR',301),0.0,'relative') # Marker to indicate a branching to Injector beam dump 
#        EG01.append(TM.generate('QFC',310),0.123,'relative')
        EG01.append(TM.generate('QFCS',320),0.05+0.223,'relative')
        EG01.append(TM.generate('DHVS',330),0.06,'relative')
        EG01.append(TM.generate('DBPM-C16',340),0.2275-0.0885+0.041,'relative')
        EG01.append(TM.generate('DSCR-LE16',350),0.0455+0.013+0.0885-0.067,'relative')

        SB01=OMType.LineContainer('SB01',5-0.022)
        SB01.append(TM.generate('SFDD',10),0.02,'relative')
        SB01.append(TM.generate('TW Cav S-Band',100),0.025,'relative')
        SB01.append(TM.generate('WFS',110,{'Overlap':1}),0.41,'absolute')
        SB01.append(TM.generate('WFS',120,{'Overlap':1}),0.15,'relative')
        SB01.append(TM.generate('WFS',130,{'Overlap':1}),0.15,'relative')
        SB01.append(TM.generate('WFS',140,{'Overlap':1}),0.15,'relative')
        SB01.append(TM.generate('DBPM-C16',150),0.582,'relative')

        SB02=OMType.LineContainer('SB02',4.59+0.032-0.0039)
        SB02.append(TM.generate('SFC',10),0.,'relative')
        SB02.append(TM.generate('TW Cav S-Band',100),0.032,'relative')
        SB02.append(TM.generate('WFS',110,{'Overlap':1}),0.432,'absolute')
        SB02.append(TM.generate('WFS',120,{'Overlap':1}),0.15,'relative')
        SB02.append(TM.generate('WFS',130,{'Overlap':1}),0.15,'relative')
        SB02.append(TM.generate('WFS',140,{'Overlap':1}),0.15,'relative')
        SB02.append(TM.generate('DBPM-C16',150),0.585,'relative')

        LH01=OMType.LineContainer('LH01',2.19)
        LH01.append(TM.generate('DBAM-PS16',10),0.099,'relative') 
        LH01.append(TM.generate('QFDM-short',20),0.04+0.026,'relative')
        LH01.append(TM.generate('QFCS',30),0.1,'relative')
        LH01.append(TM.generate('QFDM-noCor',40),0.05,'relative')
        LH01.append(TM.generate('QFDM',50),0.2,'relative')
        LH01.append(TM.generate('DBPM-C16',60),0.18-0.008-0.056,'relative')
        LH01.append(TM.generate('QFDM-noCor',70),0.02+0.008+0.056,'relative')
        LH01.append(TM.generate('DSCR-OV16',80),0.066,'relative')
        
        LH02=OMType.LineContainer('LH02',-0.412)
        LH02.append(TM.generate('QFDM',10),0.09,'relative')
        LH02.append(TM.generate('LH-Laserport',15),0.033,'relative')
        varC=OMType.VariableContainer(0.16,0)
        LH02.append(TM.generate('AFL',100,{'angle':-4.1,'design_angle':-4.1,'e1':0,'e2':1,'BC':'Laser Heater'}),0.142,'relative')
        LH02.append(TM.generate('AFL',200,{'angle':4.1,'design_angle':4.1,'e1':1,'e2':0,'BC':'Laser Heater'}),2,varC)
        LH02.append(TM.generate('DBPM-C16',210),0.19,'relative')
        LH02.append(TM.generate('DSCR-LH16',220),0.08,'relative')
        LH02.append(TM.generate('U50',230),0.14-0.007,'relative')
        LH02.append(TM.generate('DBPM-C16',240),0.21-0.058,'relative')
        LH02.append(TM.generate('DSCR-LH16',250),0.08,'relative')
        LH02.append(TM.generate('AFL',300,{'angle':4.1,'design_angle':4.1,'e1':0,'e2':1,'BC':'Laser Heater'}),0.191,'relative')
        LH02.append(TM.generate('AFL',400,{'angle':-4.1,'design_angle':-4.1,'e1':1,'e2':0,'BC':'Laser Heater'}),2,varC)
        LH02.append(TM.generate('LH-Laserport',405),0.141,'relative')
        LH02.append(TM.generate('QFDM',410),0.038,'relative')

        LH03=OMType.LineContainer('LH03',2.563)
        LH03.append(TM.generate('DBPM-C16',10),0.,'relative')
        LH03.append(TM.generate('QFDM',30),0.298,'relative')
        LH03.append(TM.generate('QFDM-noCor',40),0.255,'relative')
        LH03.append(TM.generate('DBPM-C16',50),0.155-0.062,'relative')
        LH03.append(TM.generate('QFDM',60),0.062,'relative')
        LH03.append(TM.generate('QFDM-noCor',80),0.15-0.035+0.137+0.088,'relative')    
        LH03.append(TM.generate('DBPM-C16',90),0.135,'relative')
        
        SB03=TM.generate('SB-Lin-Cell-First',0,{'Name':'SB03'})
        SB04=TM.generate('SB-Lin-Cell-Mid',0,{'Name':'SB04'})
        SB05=TM.generate('SB-Lin-Cell-Empty',0,{'Name':'SB05'})
        
        XB01=OMType.LineContainer('XB01',5.311)
        XB01.append(TM.generate('TW Cav X-Band',100),0.305-0.013,'relative')
        XB01.append(TM.generate('DBPM-C16',120),0.2048,'relative')
        XB01.append(TM.generate('TW Cav X-Band',200),0.2048,'relative')
        
        BC01=OMType.LineContainer('BC01',6.615)
        BC01.append(TM.generate('DBPM-C16',10),0.12+0.08,'relative')
        BC01.append(TM.generate('QFDM',20),0.105-0.08,'relative')
        BC01.append(TM.generate('DBPM-C16',30),0.425,'relative')
        BC01.append(TM.generate('DSCR-OV16',40),0.15,'relative')
        BC01.append(TM.generate('QFDM',50),0.240-0.027,'relative')
        BC01.append(TM.generate('QFDM',70),0.466+0.749,'relative')
        BC01.append(TM.generate('DBPM-C16',80),1.011,'relative') 
        BC01.append(TM.generate('QFDM',90),0.189,'relative')
        BC01.append(TM.generate('DBPM-C16',100),0.987,'relative')
        BC01.append(TM.generate('QFDM',110),0.098,'relative')
        
        BC02=OMType.LineContainer('BC02',-0.8226)
        varC=OMType.VariableContainer(6,2.655+0.0175)
        varD=OMType.VariableContainer(6,3.601+0.0175+0.306)
        BC02.append(TM.generate('AFBC1',100,{'angle':-3.82,'design_angle':-3.82,'e1':0,'e2':1,'BC':'Bunch Compressor 1'}),0.,'relative')
        BC02.append(TM.generate('QFBS',110),1.8,'relative')
        BC02.append(TM.generate('QFB',120),0.1,'relative')
        BC02.append(TM.generate('HFA',130),0.1,'relative')
        BC02.append(TM.generate('DBPM-C38',140),0.1+0.0175,'relative')
        BC02.append(TM.generate('AFBC1',200,{'angle':3.82,'design_angle':3.82,'e1':1,'e2':0,'BC':'Bunch Compressor 1'}),0,varC)
        BC02.append(TM.generate('COL-BC-Scraper',210),0.29,'relative')
        BC02.append(TM.generate('DSCR-BC120',220),0.025,'relative')
        BC02.append(TM.generate('AFBC1',300,{'angle':3.82,'design_angle':3.82,'e1':0,'e2':1,'BC':'Bunch Compressor 1'}),0.325,'relative')
        BC02.append(TM.generate('DSRM-VIS',310),0.846+0.306,'relative')        
        BC02.append(TM.generate('DBPM-C38',320),0,varD)
        BC02.append(TM.generate('HFA',330),0.1+0.0175,'relative')
        BC02.append(TM.generate('QFB',340),0.1,'relative')
        BC02.append(TM.generate('QFAS',350),0.09,'relative')
        BC02.append(TM.generate('DALA',360),1.214-0.0385,'relative')
        BC02.append(TM.generate('AFBC1',400,{'angle':-3.82,'design_angle':-3.82,'e1':1,'e2':0,'BC':'Bunch Compressor 1'}),1.56-1.214+0.0385-0.037,'relative')
        BC02.append(TM.generate('DBCM-THZ',410),0.4274,'relative')  
        
        DI01=OMType.LineContainer('DI01',3.84)
        DI01.append(TM.generate('DBPM-C16',10),0.263,'relative')
        DI01.append(TM.generate('QFDM',20),0.037,'relative')
        DI01.append(TM.generate('QFBS',30),0.27,'relative')
        DI01.append(TM.generate('DBPM-C16',60),0.109+0.012+0.4+0.137,'relative')
        DI01.append(TM.generate('QFDM',70),0.03-0.008,'relative')
        DI01.append(TM.generate('DWSC-C16-AL',90),0.167-0.022+0.005+0.137+0.022+0.061,'relative')
        DI01.append(TM.generate('TDS S-Band',100),0.346,'relative')
        
        DI02=OMType.LineContainer('DI02',5.456)
        DI02.append(TM.generate('DBPM-C16',10),0.366+0.037,'relative')
        DI02.append(TM.generate('QFDM',20),0.09-0.037,'relative')
        DI02.append(TM.generate('QFDM',30),0.9,'relative')
        DI02.append(TM.generate('DBPM-C16',40),0.756,'relative')
        DI02.append(TM.generate('QFDM',50),0.044,'relative')
        DI02.append(TM.generate('DLAC-LL16',55),0.363-0.091,'relative')
        DI02.append(TM.generate('QFDM',60),0.4+0.091,'relative')
        DI02.append(TM.generate('DCDR',65),0.263,'relative')
        DI02.append(TM.generate('DSCR-OV16',75),0.09-0.137+0.1+0.047,'relative')
        DI02.append(TM.generate('DBPM-C16',80),0.11-0.047+0.037,'relative')
        DI02.append(TM.generate('QFDM',90),0.11-0.037,'relative')

                    
        InjLine=[EG01,SB01,SB02,LH01,LH02,LH03,SB03,SB04,SB05,XB01,BC01,BC02,DI01,DI02]        
        Injector=OMType.LineContainer('IN')
        Injector.append(InjLine)            



        #------------------------------------------------------
        #----- Insertion of short Linac beam dump
        BD01=OMType.LineContainer('BD01',0)
        BD01.append(TM.generate('QFA',10),1.1,'relative')
        BD01.append(TM.generate('DBPM-C38',20),0.4,'relative')
        BD01.append(TM.generate('DSCR-HR38',30),0.15,'relative')
        BD01.append(TM.generate('Beam-Dump-S10',35),3.8115,'relative')
        Linac1Dump=OMType.LineContainer('10')
        Linac1Dump.append(BD01,0,'relative')


        #-----------------------------------------------------
        # Linac 1
        
        CB01=TM.generate('CB-Lin1-Cell',0,{'Name':'CB01'})
        CB02=TM.generate('CB-Lin1-Cell',0,{'Name':'CB02'})
        
        angle=0
        Lcell=4.9
        DI01=OMType.LineContainer('DI01',Lcell)
        DI01.append(TM.generate('DWSC-C16',10),0.094,'relative')
        DI01.append(TM.generate('DSCR-HR16',20),0.12,'relative')
        DI01.append(TM.generate('DICT-C16',25),0.0675,'relative')
        DI01.append(TM.generate('QFDM-noCor',30),0.03-0.0005,'relative')
        DI01.append(TM.generate('AFDL',100,{'angle':angle,'design_angle':-20,'e1':0.5,'e2':0.5,'branch':True}),0.303,'relative')
        DI01.append(TM.generate('MKBR',101),0.0,'relative')
        DI01.append(TM.generate('DBPM-C16',110),2.09-0.003,'relative')
        DI01.append(TM.generate('QFDM',120),0.049,'relative')

        CB03=TM.generate('CB-Lin1-Cell-WSC',0,{'Name':'CB03'})
        CB04=TM.generate('CB-Lin1-Cell',0,{'Name':'CB04'})
        CB05=TM.generate('CB-Lin1-Cell-WSC',0,{'Name':'CB05'})
        CB06=TM.generate('CB-Lin1-Cell',0,{'Name':'CB06'})
        CB07=TM.generate('CB-Lin1-Cell-WSC',0,{'Name':'CB07'})
        CB08=TM.generate('CB-Lin1-Cell',0,{'Name':'CB08'})
        CB09=TM.generate('CB-Lin1-Cell-Last',0,{'Name':'CB09'})
        
        BC01=OMType.LineContainer('BC01',9.665)
        BC01.append(TM.generate('DBPM-C16',10),0.03,'relative')
        BC01.append(TM.generate('QFDM',20),0.049,'relative')
        BC01.append(TM.generate('DWSC-C16-AL',30),0.019,'relative')
        BC01.append(TM.generate('QFDM',40),1.08,'relative')
        BC01.append(TM.generate('DBPM-C16',50),2.351,'relative')
        BC01.append(TM.generate('QFDM',60),0.049,'relative')
        BC01.append(TM.generate('DBAM-FS16',70),0.839,'relative')
        BC01.append(TM.generate('QFDM',80),1.586,'relative')
        BC01.append(TM.generate('DBPM-C16',90),1.305,'relative')
        BC01.append(TM.generate('QFDM',100),0.095,'relative')
        
        BC02=OMType.LineContainer('BC02',-0.521)
#        varC=OMType.VariableContainer(7,3.15+0.1+0.72+0.037)
        varC=OMType.VariableContainer(7,3.15)
        varD=OMType.VariableContainer(7,4.2761+0.357-0.661)
        BC02.append(TM.generate('AFBC3',100,{'angle':-2.15,'design_angle':-2.15,'e1':0,'e2':1,'BC':'Bunch Compressor 2'}),0.,'relative')
        BC02.append(TM.generate('QFBS',110),2.45,'relative')
        BC02.append(TM.generate('QFB',120),0.1,'relative')
        BC02.append(TM.generate('HFB',130),0.09,'relative')
        BC02.append(TM.generate('DBPM-C16',140),0.11,'relative')
#        BC02.append(TM.generate('DALA',150),0,varC)
#        BC02.append(TM.generate('AFBC3',200,{'angle':2.15,'design_angle':2.15,'e1':1,'e2':0,'BC':'Bunch Compressor 2'}),0.720,'relative')
#        BC02.append(TM.generate('DALA',150),0,varC)
        BC02.append(TM.generate('AFBC3',200,{'angle':2.15,'design_angle':2.15,'e1':1,'e2':0,'BC':'Bunch Compressor 2'}),0,varC)
        BC02.append(TM.generate('COL-BC-Scraper',210),0.3005,'relative')
        BC02.append(TM.generate('DSCR-BC120',220),0.0395,'relative')
        BC02.append(TM.generate('BC-SlotFoil-H',230),0.0395,'relative')
        BC02.append(TM.generate('BC-SlotFoil-V',240),0.0405,'relative') 
        BC02.append(TM.generate('AFBC3',300,{'angle':2.15,'design_angle':2.15,'e1':0,'e2':1,'BC':'Bunch Compressor 2'}),0.26,'relative')
        BC02.append(TM.generate('DSRM-VIS',310),1.0261+0.357-0.661,'relative')        
        BC02.append(TM.generate('DBPM-C16',320),0,varD)
        BC02.append(TM.generate('HFB',330),0.11,'relative')
        BC02.append(TM.generate('QFB',340),0.09,'relative')
        BC02.append(TM.generate('QFS',350),0.05,'relative')
        BC02.append(TM.generate('DALA',360),1.922-0.019,'relative')
        BC02.append(TM.generate('AFBC3',400,{'angle':-2.15,'design_angle':-2.15,'e1':1,'e2':0,'BC':'Bunch Compressor 2'}),2.25-1.922+0.019-0.037,'relative')
        BC02.append(TM.generate('DBCM-IR',410),0.4-0.021,'relative')        
                 
        Lsec=9.43
        angle=0
        MA01=OMType.LineContainer('MA01',Lsec)
        MA01.append(TM.generate('DBPM-C16',10),0.104,'relative')
        MA01.append(TM.generate('QFDM',20),0.1-0.004,'relative')
#        MA01.append(TM.generate('DCDR-VACONLY',25),1.38-0.137,'relative')
        MA01.append(TM.generate('QFDM',50),0.05+0.15+0.12+1.480+0.05,'relative')
        MA01.append(TM.generate('DBPM-C16',60),1.82,'relative')
        MA01.append(TM.generate('QFDM',70),0.08,'relative')
        MA01.append(TM.generate('DCDR',80),1.008-0.312-0.037,'relative')
        MA01.append(TM.generate('DSCR-HR16',90),0.2,'relative')
        MA01.append(TM.generate('AFBC1',100,{'angle':0,'design_angle':0,'e1':0,'e2':1}),0.16+0.025+0.05+0.3-0.043,'relative')  
        MA01.append(TM.generate('QFDM',110),0.10-0.025,'relative')
        MA01.append(TM.generate('Beam-Stopper-S10',115),0.15,'relative')
        MA01.append(TM.generate('DBPM-C16',120),0.13-0.05,'relative')
        MA01.append(TM.generate('QFDM',130),0.07,'relative')


        L1Line=[CB01,CB02,DI01,CB03,CB04,CB05,CB06,CB07,CB08,CB09,BC01,BC02,MA01]
        Linac10=OMType.LineContainer('10')
        Linac10.append(L1Line)


        #--------------------------------
        # Linac 2

        CB01=TM.generate('CB-Lin2-Cell-WSC',0,{'Name':'CB01'})
#        CB01=TM.generate('CB-Lin2-Cell',0,{'Name':'CB01'})
        CB02=TM.generate('CB-Lin2-Cell',0,{'Name':'CB02'})
        CB03=TM.generate('CB-Lin2-Cell',0,{'Name':'CB03'})
        CB04=TM.generate('CB-Lin2-Cell-Last',0,{'Name':'CB04'})
        
        SY01=OMType.LineContainer('SY01',8.165)
        SY01.append(TM.generate('DBPM-C16',10),0.03,'relative')
        SY01.append(TM.generate('QFD',20),0.049,'relative')
        SY01.append(TM.generate('QFD',30),1.536+0.8,'relative')
        SY01.append(TM.generate('DBPM-C16',40),3.9-0.8+0.032,'relative')
        SY01.append(TM.generate('QFD',50),0.1-0.032,'relative')
        SY01.append(TM.generate('DBPM-C16',60),0.75-0.042,'relative')
        SY01.append(TM.generate('DWSC-C16',70),0.1,'relative')
        SY01.append(TM.generate('QFD',80),0.063+0.042,'relative')
        
        SY02=OMType.LineContainer('SY02',-0.7502)
        SY02.append(TM.generate('RESKICKDC',10,{'design_kick':0}),0.285,'relative')
        SY02.append(TM.generate('RESKICKAC',20,{'design_kick':0}),0.0,'relative')
        SY02.append(TM.generate('RESKICKDC',30,{'design_kick':0}),0.0,'relative')
        SY02.append(TM.generate('RESKICKAC',40,{'design_kick':0}),0.0,'relative')
        SY02.append(TM.generate('RESKICKDC',50,{'design_kick':0}),0.0,'relative')
        SY02.append(TM.generate('SFC',60),0.080,'relative')
        SY02.append(TM.generate('QFA',70),0.105,'relative')
        SY02.append(TM.generate('DBPM-C38',80),1.33-0.12,'relative')
        SY02.append(TM.generate('SFC',90),0.08,'relative')
        SY02.append(TM.generate('QFA',100),0.105,'relative')
        SY02.append(TM.generate('DBPM-C38',120),1.33-0.12,'relative')
        SY02.append(TM.generate('SFC',130),0.08,'relative')
        SY02.append(TM.generate('QFA',140),0.105,'relative')
        SY02.append(TM.generate('DBPM-C38',150),1.18-0.24,'relative')
        SY02.append(TM.generate('DWSC-C38',160),0.12,'relative')
        SY02.append(TM.generate('SFC',170),0.08,'relative')
        SY02.append(TM.generate('QFA',180),0.105,'relative')
        angle=0
        SY02.append(TM.generate('AFS',200,{'angle':angle,'design_angle':2,'e1':0,'e2':0,'branch':True,'BC':'Switch Yard 1'}),0.30-0.0002+0.12,'relative')
        SY02.append(TM.generate('MKBR',201),0.,'relative')
                
        SY03=OMType.LineContainer('SY03', 19.53+0.12)
        SY03.append(TM.generate('DBPM-C16',10),4.8+0.12,'relative')
        SY03.append(TM.generate('QFD',20),0.1,'relative')
        SY03.append(TM.generate('QFD',30),3,'relative')
        SY03.append(TM.generate('DBPM-C16',40),2.6,'relative')
        SY03.append(TM.generate('QFD',50),0.1,'relative')
        SY03.append(TM.generate('QFD',60),4.2,'relative')
        if self.alt < 2:
            SY03.append(TM.generate('DBPM-C16',80),0.2+2.31+0.05-0.257,'relative')
        else:
            SY03.append(TM.generate('DCDR',70),0.876+0.7-0.594,'relative')
            SY03.append(TM.generate('DBPM-C16',80),0.2+2.31+0.05-0.257-0.137-0.876-0.7+0.594,'relative')
        if self.alt == 0:
            SY03.append(TM.generate('DWSC-C16-AL',90),0.1+0.257,'relative')
        else:
            SY03.append(TM.generate('DSCR-HR16',85),0.12,'relative')            
            SY03.append(TM.generate('DWSC-C16-AL',90),0.1+0.257-0.12-0.137,'relative')

        SY03.append(TM.generate('QFD',100),0.053,'relative')

        L2Line=[CB01,CB02,CB03,CB04,SY01,SY02,SY03]
        Linac20=OMType.LineContainer('20')
        Linac20.append(L2Line)

        
        #--------------------------------------
        # Linac 3
        
        CB01=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB01'})
        CB01.append(TM.generate('DWSC-C16',440),0.019,'relative')
        CB02=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB02'})
        CB03=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB03'})
        CB04=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB04'})
        CB05=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB05'})
        CB05.append(TM.generate('DWSC-C16-AL',440),0.019,'relative')
        CB06=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB06'})
        CB07=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB07'})
        CB08=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB08'})
        CB08.append(TM.generate('COL-TR-16',440),0.019,'relative')
        CB09=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB09'})
        CB09.append(TM.generate('DWSC-C16',440),0.019,'relative')
        CB10=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB10'})
        CB10.append(TM.generate('COL-TR-16',440),0.019,'relative')
        CB11=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB11'})
        CB12=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB12'})
        CB12.append(TM.generate('COL-TR-16',440),0.019,'relative')
        CB13=TM.generate('CB-Lin3-Cell-incomplete',0,{'Name':'CB13'})
        CB13.append(TM.generate('DWSC-C16',440),0.019,'relative')
        CB14=OMType.LineContainer('CB14', 9.1)
        CB14.append(TM.generate('TDS C-Band',100),0.035,'relative')
        CB14.append(TM.generate('TDS C-Band',200),0.1,'relative')
        CB14.append(TM.generate('DBPM-C16',420),4.33,'relative')
        CB14.append(TM.generate('QFD',430),0.049,'relative')
        CB14.append(TM.generate('COL-TR-16',440),0.019,'relative')
        CB15=OMType.LineContainer('CB15', 9.1)
        CB15.append(TM.generate('COL-Dechirper-H',100),1-0.315,'relative')
        CB15.append(TM.generate('COL-Dechirper-V',200),1+0.315-0.465,'relative')
        CB15.append(TM.generate('DBPM-C16',420),4.465+0.465,'relative')
        CB15.append(TM.generate('QFD',430),0.049,'relative')
        CB16=OMType.LineContainer('CB16', 8.435)

        L3Line  =[CB01,CB02,CB03,CB04,CB05,CB06,CB07,CB08,CB09,CB10,CB11,CB12,CB13,CB14,CB15,CB16]
        Linac30=OMType.LineContainer('30')
        Linac30.append(L3Line)


        #----------------------------
        # Aramis

        
        CL01=OMType.LineContainer('CL01', 13.54)
        CL01.append(TM.generate('DBPM-C16',10),0.03,'relative')
        CL01.append(TM.generate('QFD',20),0.049,'relative')
        CL01.append(TM.generate('COL-TR-16',30),0.019,'relative')
        CL01.append(TM.generate('SFQFM',40),0.855,'relative')
        CL01.append(TM.generate('QFM',50),0,'relative')
        CL01.append(TM.generate('DBPM-C16',60),1.95,'relative')
        CL01.append(TM.generate('SFQFM',70),0.0,'relative')
        CL01.append(TM.generate('QFM',80),0,'relative')
        CL01.append(TM.generate('SFQFM',90),2.05,'relative')
        CL01.append(TM.generate('QFM',100),0,'relative')
        CL01.append(TM.generate('DBAM-FS16',110),1.775,'relative')
        CL01.append(TM.generate('DBPM-C16',120),0.1,'relative')
        CL01.append(TM.generate('SFQFM',130),0.0,'relative')
        CL01.append(TM.generate('QFM',140),0,'relative')
        CL01.append(TM.generate('DBPM-C16',150),0.276,'relative')
        CL01.append(TM.generate('DWSC-C16-AL',160),0.1,'relative')
        CL01.append(TM.generate('DSCR-HR16',170),0.1,'relative')
        CL01.append(TM.generate('SFQFM',180),0.0,'relative')
        CL01.append(TM.generate('QFM',190),0,'relative')
        
        CL02=OMType.LineContainer('CL02', 0)
        CL02.append(TM.generate('AFBC3',100,{'angle':-1,'design_angle':-1,'e1':0,'e2':1,'BC':'Aramis Collimator'}),0.,'relative')
        CL02.append(TM.generate('DBPM-C16',110),2.55+0.035,'relative')
        CL02.append(TM.generate('SFQFM',120),0.0,'relative')
        CL02.append(TM.generate('QFM-short',130),0.1-0.035,'relative')
#        CL02.append(TM.generate('HFB',140),0.35+0.035,'relative')
        CL02.append(TM.generate('QFB',150),0.1+0.45+0.035,'relative')
        CL02.append(TM.generate('QFBS',160),0.1,'relative')
        dl=5.25/math.cos(math.asin(1)/90)-4.4-0.035
        CL02.append(TM.generate('AFBC3',200,{'angle':1,'design_angle':1,'e1':1,'e2':0,'BC':'Aramis Collimator'}),dl,'relative')
        CL02.append(TM.generate('QFM-short',210),0.35,'relative')
        CL02.append(TM.generate('DBPM-C16',220),0.1-0.065,'relative')
        CL02.append(TM.generate('SFQFM',230),0.065,'relative')
        CL02.append(TM.generate('DWSC-C16',235),0.1+0.141,'relative')
        CL02.append(TM.generate('SFQFM',240),0.4-0.237-0.141,'relative')
        CL02.append(TM.generate('QFM-short',250),0.1,'relative')
        CL02.append(TM.generate('HFB',255),0.02,'relative')
        CL02.append(TM.generate('DBPM-C16',260),0.1-0.089+0.157,'relative')
        CL02.append(TM.generate('DSCR-HR16',280),0.12,'relative')
        CL02.append(TM.generate('BC-SlotFoil-V',282),0.57,'relative') 
        CL02.append(TM.generate('COL-Energy',290),0.8-0.15-0.57,'relative')
        CL02.append(TM.generate('QFS',300),0.274-0.073+0.104,'relative')
        CL02.append(TM.generate('HFB',305),0.08,'relative')
        CL02.append(TM.generate('QFM-short',310),0.02,'relative')
        CL02.append(TM.generate('SFQFM',320),0.1,'relative')
        CL02.append(TM.generate('DALA',325),0.119-0.011,'relative')
        CL02.append(TM.generate('DBPM-C16',330),0.35+0.015-0.137-0.119+0.011,'relative')
        CL02.append(TM.generate('SFQFM',340),0.035,'relative')
        CL02.append(TM.generate('QFM',350),0,'relative')
        CL02.append(TM.generate('AFBC3',400,{'angle':1,'design_angle':1,'e1':0,'e2':1,'BC':'Aramis Collimator'}),0.25,'relative')
        dl=5.25/math.cos(math.asin(1)/90)-5.0+0.03-0.1
        CL02.append(TM.generate('DSRM-UV',410),0.5,'relative')
        CL02.append(TM.generate('QFBS',420),dl,'relative')
        CL02.append(TM.generate('QFB',430),0.1,'relative')
#        CL02.append(TM.generate('HFB',440),0.1,'relative')
        CL02.append(TM.generate('SFQFM',450),0.05+0.2,'relative')
        CL02.append(TM.generate('QFM-short',460),0.1-0.03,'relative')
        CL02.append(TM.generate('DBPM-C16',470),0.3+0.03,'relative')
        CL02.append(TM.generate('SFQFM',480),0.00,'relative')
        CL02.append(TM.generate('DALA',485),1.875-0.012,'relative')
        CL02.append(TM.generate('AFBC3',500,{'angle':-1,'design_angle':-1,'e1':1,'e2':0,'BC':'Aramis Collimator'}),2.35-0.03-0.137-1.875+0.012,'relative')
        
        MA01=OMType.LineContainer('MA01', 13.25)
        MA01.append(TM.generate('QFM-veryshort',10),0.3,'relative')
        MA01.append(TM.generate('DBCM-IR',15),0.125,'relative')
        MA01.append(TM.generate('SFQFM-short',20),0.05-0.025,'relative')
        MA01.append(TM.generate('DBPM-C16',40),0.25+0.7+0.1,'relative')
        MA01.append(TM.generate('SFQFM',50),0.00,'relative')
        MA01.append(TM.generate('QFM',60),0.0,'relative')
        MA01.append(TM.generate('SFQFM',70),2.55,'relative')
        MA01.append(TM.generate('QFM',80),0.0,'relative')
        MA01.append(TM.generate('DICT-C16',90),1.95-0.075-0.09+0.1575-0.05,'relative')
        MA01.append(TM.generate('DBPM-C16',100),0.2+0.175-0.1575+0.05,'relative')
        MA01.append(TM.generate('SFQFM',110),0.00,'relative')
        MA01.append(TM.generate('QFM',120),0.0,'relative')
        MA01.append(TM.generate('SFQFM',130),2.0,'relative')
        MA01.append(TM.generate('QFM',140),0.0,'relative')
        
        
        Lsec=9.5
        angle=0
        MA02=OMType.LineContainer('MA02', Lsec)
        MA02.append(TM.generate('DBPM-C8',10),0.385,'relative')
        MA02.append(TM.generate('DBPM-C8',20),0.85+0.05+1-0.002+0.051,'relative')
        MA02.append(TM.generate('DSCR-HR8',30),1.78-0.037+0.009-0.06,'relative')
        MA02.append(TM.generate('DBPM-C8',40),0.12,'relative')
        MA02.append(TM.generate('QFF',50),0.06,'relative')
        MA02.append(TM.generate('DWSC-C8',60),0.077,'relative')
        MA02.append(TM.generate('AFP1',100,{'angle':angle,'design_angle':0,'e1':0,'e2':1}),0.175,'relative')
        MA02.append(TM.generate('Beam-Stopper-Sar',105),0.881,'relative')
        MA02.append(TM.generate('DBPM-C8',110),0.477,'relative')
        MA02.append(TM.generate('QFF',120),0.06,'relative')
        
        UN01=TM.generate('U15-Cell-Empty',0,{'Name':'UN01'})

        if (self.alt==2):
            UN02=TM.generate('U15-Cell',0,{'Name':'UN02'})
        else:    
            UN02=TM.generate('U15-Cell-Empty',0,{'Name':'UN02'})

        UN03=TM.generate('U15-Cell',0,{'Name':'UN03'})
        UN04=TM.generate('U15-Cell',0,{'Name':'UN04'})
        UN05=TM.generate('U15-Cell',0,{'Name':'UN05'})
        UN06=TM.generate('U15-Cell',0,{'Name':'UN06'})
        UN07=TM.generate('U15-Cell',0,{'Name':'UN07'})
        UN08=TM.generate('U15-Cell',0,{'Name':'UN08'})

        if (self.alt==2):
            UN09=OMType.LineContainer('UN09',-0.027)
            varC=OMType.VariableContainer(1.200,0)
            UN09.append(TM.generate('DWSC-C8',10),0.05+0.175,'relative')
            UN09.append(TM.generate('AFSS',100,{'angle':-0,'design_angle':-0.22,'e1':0,'e2':1,'BC':'Aramis Self-Seeding'}),0.199,'relative')
            UN09.append(TM.generate('AFSS',200,{'angle':0,'design_angle':0.22,'e1':1,'e2':0,'BC':'Aramis Self-Seeding'}),1,varC)
            UN09.append(TM.generate('AFSS',300,{'angle':0,'design_angle':0.22,'e1':0,'e2':1,'BC':'Aramis Self-Seeding'}),0.16,'relative')
            UN09.append(TM.generate('AFSS',400,{'angle':-0,'design_angle':-0.22,'e1':1,'e2':0,'BC':'Aramis Self-Seeding'}),1,varC)
            UN09.append(TM.generate('DBPM-C8',410),0.374-0.175,'relative')
            UN09.append(TM.generate('QFF',420),0.06,'relative')
        else:
            UN09=TM.generate('U15-Cell',0,{'Name':'UN09'})
  
        UN10=TM.generate('U15-Cell',0,{'Name':'UN10'})
        UN11=TM.generate('U15-Cell',0,{'Name':'UN11'})
        UN12=TM.generate('U15-Cell',0,{'Name':'UN12'})
        UN13=TM.generate('U15-Cell',0,{'Name':'UN13'})
        UN14=TM.generate('U15-Cell',0,{'Name':'UN14'})
        UN15=TM.generate('U15-Cell-Last',0,{'Name':'UN15'})
        UN16=TM.generate('U15-Cell-Empty',0,{'Name':'UN16'})
        UN17=TM.generate('U15-Cell-Empty',0,{'Name':'UN17'})
        UN18=OMType.LineContainer('UN18',4.75)
        UN18.append(TM.generate('COL-Dechirper-H',10),0.85-0.0625,'relative')
        UN18.append(TM.generate('COL-Dechirper-H',20),0.85,'relative')
        UN18.append(TM.generate('DBPM-C8',70),4.483-3.7+0.0625,'relative')
        UN18.append(TM.generate('QFF',80),0.06,'relative')
        UN19=TM.generate('U15-Cell-Empty',0,{'Name':'UN19'})
        UN20=OMType.LineContainer('UN20',4.75)
        UN20.append(TM.generate('DWSC-C8',10),0.05,'relative')
        UN20.append(TM.generate('DBAM-FS8',20),0.025+2.133-0.0005,'relative')
        UN20.append(TM.generate('DBPM-C8',70),2.1+0.0005+0.025-0.05,'relative')
        UN20.append(TM.generate('QFF',80),0.06,'relative')
        
        Lsec=0
        angle=0
        BD01=OMType.LineContainer('BD01',Lsec)
        BD01.append(TM.generate('QFF',20),0.2265-0.116+0.29+0.125+0.075+1.05-0.29,'relative')
        BD01.append(TM.generate('DICT-C16',30),0.06+0.3235-0.125+0.03,'relative')
        BD01.append(TM.generate('DBPM-C16',40),0.25+0.106-0.1-0.1885,'relative')
        BD01.append(TM.generate('DSCR-HR16',50),0.12,'relative')
        BD01.append(TM.generate('AFD1',100,{'angle':angle,'design_angle':8,'e1':0.5,'e2':0.5,'branch':True}),0.279-0.0125,'relative')
        BD01.append(TM.generate('MKBR',101),0.0,'relative') 
        BD01.append(TM.generate('DSCR-OV38',110),5.55-2.2665,'relative')
        BD01.append(TM.generate('AFP1',200,{'angle':0,'design_angle':0,'e1':0,'e2':1,'Tilt':math.asin(1)}),0.363,'relative')     
        BD01.append(TM.generate('FE-Shielding',205),2.967,'relative')


        ArLine=[CL01,CL02,MA01,MA02,UN01,UN02,UN03,UN04,UN05,UN06,UN07,UN08,UN09,UN10,UN11,UN12,UN13,UN14,UN15,UN16,UN17,UN18,UN19,UN20,BD01]
        Aramis=OMType.LineContainer('AR')
        Aramis.append(ArLine)


        # Aramis Dump
        BD02=OMType.LineContainer('BD02',0)
        BD02.append(TM.generate('DBPM-C16',10),0.42,'relative')
        dlict=0.0
        dlict=0.1575
        LD=1.1/math.cos(8*math.asin(1)/90)-0.92-0.1+dlict-0.0075
        BD02.append(TM.generate('QFM',30),LD,'relative')
        LD=LD+0.3015-dlict
        BD02.append(TM.generate('DBPM-C16',40),LD-0.022+0.03235,'relative')
        BD02.append(TM.generate('DSCR-HR16',50),0.12,'relative')
        LD=19.478/math.cos(8*math.asin(1)/90)-0.0685+0.2+0.002-0.0249
        BD02.append(TM.generate('Beam-Dump-Sar',55),LD,'relative')

        AramisDump=OMType.LineContainer('AR')
        AramisDump.append(BD02,0,'relative')


        #-----------------------------
        # Athos Beamline

 

        ddx=0.7502
        SY01=OMType.LineContainer('SY01', 29.100107+ddx+0.12+0.000049)
        SY01.append(OMType.Alignment({'dy':0.01,'Tag':'ALIG','index':1}))
        SY01.append(TM.generate('DBPM-C16',10),3.3+ddx+0.12+0.000048,'relative')
        SY01.append(TM.generate('QFM',20),0.35-0.183-0.035,'relative')
        SY01.append(TM.generate('SFQFM',22),0.183+0.925+0.035,'relative')
        SY01.append(TM.generate('BC-SlotFoil-V',25),1.65-0.626-0.925,'relative') 
        SY01.append(TM.generate('QFBS',30),0.15+0.026,'relative')


        SY01.append(TM.generate('QFD',40),0.05,'relative')
        SY01.append(TM.generate('HFB',50),0.1,'relative')
        SY01.append(TM.generate('DBPM-C16',60),2.1,'relative')
        SY01.append(TM.generate('QFD',70),0.1,'relative')
        SY01.append(TM.generate('HFB',80),0.1,'relative')
        SY01.append(TM.generate('QFD',90),2.3,'relative')
        SY01.append(TM.generate('DBPM-C16',100),1.25-0.135,'relative')
        SY01.append(TM.generate('AFBC3-noCor',200,{'angle':1,'design_angle':1,'e1':0.5,'e2':0.5,'BC':'Switch Yard 1'}),0.15+0.135,'relative')
        #used for matching        SY01.append(TM.generate('AFBC3',200,{'angle':1,'e1':0.5,'e2':0.5}),0.15,'relative')
        SY01.append(TM.generate('QFD',210),1.5,'relative')
        SY01.append(TM.generate('HFB',220),2.3,'relative')
        SY01.append(TM.generate('QFD',230),0.1,'relative')
        SY01.append(TM.generate('DBPM-C16',240),1.8,'relative')
        SY01.append(TM.generate('HFB',250),0.4,'relative')
        SY01.append(TM.generate('QFD',260),0.1,'relative')
        SY01.append(TM.generate('QFS',270),0.05,'relative')
        SY01.append(TM.generate('QFM',280),1.912,'relative')
        SY01.append(TM.generate('SFQFM',282),0.,'relative')
        SY01.append(TM.generate('DBPM-C16',290),3.0-0.45-0.012,'relative')           
        SY01.append(TM.generate('QFD',300),0.1,'relative')
        SY01.append(TM.generate('AFBC3-noCor',400,{'angle':2,'design_angle':2,'e1':1,'e2':0.,'BC':'Switch Yard 1'}),1.15,'relative') 
        
        SY02=OMType.LineContainer('SY02', 9.13)
        SY02.append(TM.generate('QFD',10),1.0,'relative')
        SY02.append(TM.generate('DBPM-C16',20),0.7-0.004,'relative')
        SY02.append(TM.generate('AFL',100,{'angle':0.0756,'design_angle':0.108,'e1':0,'e2':1.,'Tilt':math.asin(1)}),0.194,'relative') 
        SY02.append(TM.generate('QFD',110),1.29,'relative')
        SY02.append(TM.generate('QFD',120),2.1,'relative')
        SY02.append(TM.generate('AFL',200,{'angle':-0.0756,'design_angle':-0.108,'e1':1,'e2':0.,'Tilt':math.asin(1)}),1.29,'relative') 
        SY02.append(TM.generate('DBPM-C16',210),0.103,'relative')
        SY02.append(TM.generate('QFD',230),0.03+0.137+0.12,'relative')

        SY03=OMType.LineContainer('SY03', 12.65)
        SY03.append(TM.generate('QFD',10),0.45,'relative')
        SY03.append(TM.generate('DBPM-C16',30),0.1+2.35,'relative')
        SY03.append(TM.generate('QFD',40),0.1,'relative')
        if self.alt < 2:
            SY03.append(TM.generate('DBPM-C16',60),0.1+2.25,'relative')
        else:
            SY03.append(TM.generate('DCDR',50),0.876,'relative')
            SY03.append(TM.generate('DBPM-C16',60),0.1+2.25-0.876-0.137,'relative')

        SY03.append(TM.generate('QFD',70),0.1,'relative')
        SY03.append(TM.generate('Laser-Acceleration',80),0.13-0.106,'relative')
        SY03.append(TM.generate('DBPM-C16',90),0.1-0.01+0.106,'relative')
        SY03.append(TM.generate('QFD',100),0.1,'relative')
        SY03.append(TM.generate('DWSC-C16',110),2.-0.02-0.064,'relative')
        SY03.append(TM.generate('DALA',115),0.08,'relative')
        SY03.append(TM.generate('DBPM-C16',120),0.08,'relative')
        SY03.append(TM.generate('QFD',130),0.1,'relative')
        SY03.append(TM.generate('DSCR-HR16',140),0.08+0.153,'relative')


        CL01=OMType.LineContainer('CL01', 12.050318)
        CL01.append(TM.generate('AFBC3',100,{'angle':-2.5,'design_angle':-2.5,'e1':0,'e2':1.,'BC':'Switch Yard 2'}),0.0,'relative')
        if self.alt>1:
            CL01.append(TM.generate('DSRM-UV',105),0.6,'relative')   
            CL01.append(TM.generate('HFB',110),0.15,'relative')
            CL01.append(TM.generate('QFD',120),0.05,'relative')
            CL01.append(TM.generate('QFD',130),2.5,'relative')
            CL01.append(TM.generate('DBPM-C16',140),0.718,'relative')
            CL01.append(TM.generate('DSCR-HR16',150),0.12,'relative')
            CL01.append(TM.generate('HFB',160),0.45,'relative')
            CL01.append(TM.generate('DALA',165),0.5-0.05-0.137-0.1+0.0197938,'relative')
            CL01.append(TM.generate('COL-Energy',170),0.1-0.0197938,'relative')
            CL01.append(TM.generate('QFD',180),0.475,'relative')
            CL01.append(TM.generate('QFD',190),2.5,'relative')
            CL01.append(TM.generate('AFBC3',300,{'angle':-2.5,'design_angle':-2.5,'e1':1,'e2':0.,'BC':'Switch Yard 2'}),0.85-0.137-0.26+0.001+0.546,'relative') 
        else:
            CL01.append(TM.generate('HFB',110),0.15+0.7,'relative')
            CL01.append(TM.generate('QFD',120),0.05,'relative')
            CL01.append(TM.generate('QFD',130),2.5,'relative')
            CL01.append(TM.generate('DBPM-C16',140),0.718,'relative')
            CL01.append(TM.generate('DSCR-HR16',150),0.12,'relative')
            CL01.append(TM.generate('HFB',160),0.45,'relative')
            CL01.append(TM.generate('COL-Energy',170),0.5-0.05,'relative')
            CL01.append(TM.generate('QFD',180),0.475,'relative')
            CL01.append(TM.generate('QFD',190),2.5,'relative')
            CL01.append(TM.generate('HFB',200),0.05,'relative')
            CL01.append(TM.generate('DALA',205),0.2600-0.001,'relative')
            CL01.append(TM.generate('AFBC3',300,{'angle':-2.5,'design_angle':-2.5,'e1':1,'e2':0.,'BC':'Switch Yard 2'}),0.85-0.137-0.26+0.001,'relative') 
        
   
  
        if self.alt>1:
            DI01=OMType.LineContainer('DI01', 18.52)
            DI01.append(TM.generate('DBCM-IR',10),0.4,'relative')
            DI01.append(TM.generate('DICT-C16',20),0.46,'relative')
            DI01.append(TM.generate('QFD',25),0.15,'relative')
            DI01.append(TM.generate('DBPM-C16',30),0.1+0.226,'relative')
            DI01.append(TM.generate('DSCR-OV16',40),0.1,'relative')
            DI01.append(TM.generate('UMOD',50),0.4-0.226,'relative')
            DI01.append(TM.generate('UMOD',51),0.001,'relative')
            DI01.append(TM.generate('UMOD',52),0.001,'relative')
            DI01.append(TM.generate('UMOD',53),0.001,'relative')
            DI01.append(TM.generate('UMOD',54),0.001,'relative')
            DI01.append(TM.generate('UMOD',55),0.001,'relative')
            DI01.append(TM.generate('UMOD',56),0.001,'relative')
            DI01.append(TM.generate('UMOD',57),0.001,'relative')
            DI01.append(TM.generate('UMOD',58),0.001,'relative')
            DI01.append(TM.generate('DBPM-C16',60),0.286-0.008-0.06,'relative')
            DI01.append(TM.generate('DSCR-OV16',65),0.1,'relative')
            DI01.append(TM.generate('DBAM-FS16',70),0.1+0.06+0.02,'relative')
            DI01.append(TM.generate('QFD',80),2.15-1.563-0.397-0.02,'relative')
            DI01.append(TM.generate('DBPM-C16',90),0.063,'relative')
            DI01.append(TM.generate('COL-Dechirper-H',100,{'gap':2e-3}),0.5+0.087,'relative')
            DI01.append(TM.generate('COL-Dechirper-V',200,{'gap':2e-3}),0.5+0.35,'relative')
            DI01.append(TM.generate('DBPM-C16',210),0.5+0.019+0.115+0.327-0.437,'relative')
            DI01.append(TM.generate('QFD',230),0.081,'relative')
            DI01.append(TM.generate('DBPM-C16',240),1.2-0.001-0.327,'relative')
            DI01.append(TM.generate('QFD',250),0.101,'relative')
            DI01.append(TM.generate('QFD',260),1.4,'relative')
            DI01.append(TM.generate('DBPM-C16',270),1.2-0.021+0.117-0.2,'relative')
            DI01.append(TM.generate('QFD',280),0.121-0.117,'relative')
            DI01.append(TM.generate('DWSC-C16',290),2,'relative')
            DI01.append(TM.generate('QFD',300),0.4-0.137,'relative')
            DI01.append(TM.generate('DBPM-C16',310),0.04,'relative')
        else:
            DI01=OMType.LineContainer('DI01', 18.52)
            DI01.append(TM.generate('DICT-C16',20),1.4+0.043-0.0075+0.5,'relative')
            DI01.append(TM.generate('DBPM-C16',30),0.15-0.043+0.013+0.175-0.1575,'relative')
            DI01.append(TM.generate('QFD',40),0.1-0.013,'relative')
            DI01.append(TM.generate('QFD',50),1.15,'relative')
            DI01.append(TM.generate('DBPM-C16',60),0.063,'relative')
            DI01.append(TM.generate('DWSC-C16',65),0.12,'relative')
            DI01.append(TM.generate('DBPM-C16',210),0.5+0.019+2+3.58,'relative')
            DI01.append(TM.generate('QFD',220),0.1-0.019,'relative')
            DI01.append(TM.generate('QFD',230),1.25,'relative')
            DI01.append(TM.generate('DBPM-C16',240),1.05-0.001,'relative')
            DI01.append(TM.generate('QFD',250),0.101,'relative')
            DI01.append(TM.generate('QFD',260),1.25,'relative')
            DI01.append(TM.generate('DBPM-C16',270),1.05-0.021,'relative')
            DI01.append(TM.generate('QFD',280),0.121,'relative')
            DI01.append(TM.generate('QFD',300),0.163+0.137+0.85,'relative')
            DI01.append(TM.generate('DBPM-C16',310),0.04,'relative')

    
        CB01=OMType.LineContainer('CB01',9.8)
        CB02=OMType.LineContainer('CL02',9.8)
        CB01.append(TM.generate('TW Cav C-Band',100),0.035,'relative')
        CB01.append(TM.generate('TW Cav C-Band',200),0.049387,'relative')
        CB01.append(TM.generate('DBPM-C16',220),0.080613,'relative')
        CB01.append(TM.generate('QFD',230),0.049,'relative')
        CB01.append(TM.generate('TW Cav C-Band',300),0.096075+0.137+0.019,'relative')
        CB01.append(TM.generate('TW Cav C-Band',400),0.049387,'relative')
        CB01.append(TM.generate('DBPM-C16',420),0.099538,'relative')
        CB01.append(TM.generate('QFD',430),0.049,'relative')
        CB02.append(TM.generate('COL-Dechirper-V',100,{'gap':2e-3}),0.5+0.528-0.003,'relative')
        CB02.append(TM.generate('COL-Dechirper-H',200,{'gap':2e-3}),0.5-0.528+0.875+0.003,'relative')
        CB02.append(TM.generate('DBPM-C16',220),0.080613+0.035+0.049387+0.085+1.015-0.875,'relative')
        CB02.append(TM.generate('QFD',230),0.049,'relative')
        CB02.append(TM.generate('COL-Dechirper-V',300,{'gap':2e-3}),0.5+0.74208,'relative')
        CB02.append(TM.generate('COL-Dechirper-H',400,{'gap':2e-3}),0.5-0.74208+1.09208,'relative')
        CB02.append(TM.generate('DBPM-C16',420),0.099538+1.40146-1.09208,'relative')
        CB02.append(TM.generate('QFD',430),0.049,'relative')


        # here the missing part of the Athos comes only in the later phase (planned and final)

        Lsec=9.51+18.0+1.1245+0.0275+20-11.6247-0.2-0.0027
        if self.alt > 1:
            MA01=OMType.LineContainer('MA01', Lsec)
        else:
            MA01=OMType.LineContainer('MA01', Lsec-8.1726)

        angle=0
        MA01.append(TM.generate('DBPM-C8',10),0.293+0.102-0.257,'relative')
        MA01.append(TM.generate('COL-Dechirper-V',15,{'gap':2e-3}),0.5+0.257-0.202,'relative')
        MA01.append(TM.generate('DBPM-C8',20),0.5-0.051-0.1285+0.202,'relative')
        if self.alt > 1:
            MA01.append(TM.generate('COL-Dechirper-H',25,{'gap':2e-3}),0.5+0.1285-0.2155,'relative')
            MA01.append(TM.generate('DSCR-HR8',30),0.28-0.037-0.051+0.2155,'relative')
        else:
            MA01.append(TM.generate('DSCR-HR8',30),0.28-0.037-0.051+0.2155+0.5+0.1285-0.2155+1,'relative')

        MA01.append(TM.generate('DBPM-C8',40),0.12,'relative')
        MA01.append(TM.generate('QFF',50),0.06,'relative')
        MA01.append(TM.generate('AFP1',100,{'angle':0,'e1':0,'e2':1}),0.175+0.177,'relative')
        MA01.append(TM.generate('Beam-Stopper-Sat',105),0.881,'relative')


        if self.alt<2:
            MA01.append(TM.generate('DBPM-C8',110),1.477,'relative')
            MA01.append(TM.generate('QFF',120),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',130),4,'relative')
            MA01.append(TM.generate('QFF',140),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',150),4.,'relative')
            MA01.append(TM.generate('QFF',160),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',170),4.,'relative')
            MA01.append(TM.generate('QFF',180),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',190),4,'relative')
            MA01.append(TM.generate('QFF',200),0.06,'relative')
            UN01=TM.generate('UE38-Cell-Empty',0,{'Name':'UN01'})
            UN02=TM.generate('UE38-Cell-Empty',0,{'Name':'UN02'})
            UN03=TM.generate('UE38-Cell-Empty',0,{'Name':'UN03'})
            UN04=TM.generate('UE38-Cell-Empty',0,{'Name':'UN04'})  # modulator goes in here.....
            UN05=TM.generate('UE38-Cell-Empty-400',0,{'Name':'UN05'})
        else:
            MA01.append(TM.generate('DBPM-C8',110),0.6013,'relative')
            MA01.append(TM.generate('QFF',120),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',130),2.8-0.24,'relative')
            MA01.append(TM.generate('QFF',140),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',150),2.8-0.24,'relative')
            MA01.append(TM.generate('QFF',160),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',170),2.8-0.24,'relative')
            MA01.append(TM.generate('QFF',180),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',190),2.8-0.24,'relative')
            MA01.append(TM.generate('QFF',200),0.06,'relative')
            MA01.append(TM.generate('DBPM-C8',210),2.8-0.24,'relative')
            MA01.append(TM.generate('QFF',220),0.06,'relative')
            MA01.append(TM.generate('QFF',230),1-0.18,'relative')
            MA01.append(TM.generate('DBPM-C8',240),0.06+0.6,'relative')
            MA01.append(TM.generate('QFF',250),1-0.18-0.16-0.6,'relative')
            MA01.append(TM.generate('AFBC3',300,{'angle':-0,'design_angle':-2.3,'e1':0,'e2':1,'BC':'Athos EEHG first BC'}),0.26,'relative')
            MA01.append(TM.generate('AFBC3',400,{'angle':0,'design_angle':2.3,'e1':1,'e2':0,'BC':'Athos EEHG first BC'}),3.47,'relative')
            MA01.append(TM.generate('AFBC3',500,{'angle':0,'design_angle':2.3,'e1':0,'e2':1,'BC':'Athos EEHG first BC'}),0.2,'relative')
            MA01.append(TM.generate('AFBC3',600,{'angle':0,'design_angle':-2.3,'e1':1,'e2':0,'BC':'Athos EEHG first BC'}),3.47,'relative')
            MA01.append(TM.generate('QFD',610),0.06+0.22,'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            MA01.append(TM.generate('DBPM-C16',620),0.2+0.0438,'relative')

            MA01.append(TM.generate('QFD',630),1-0.18-0.17-0.3-0.25-0.0438,'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            MA01.append(TM.generate('QFD',640),1-0.18-0.17-0.25,'relative')  # reserve space for 9.5 m chcicane (4x 0.5m Dipole, 2x3m long drift, 3x 0.5m short drift)
            UN04=OMType.LineContainer('UN04',3.0247+0.0027)    # modulator
            UN04.append(TM.generate('DBPM-C16',10),0.,'relative')
            UN04.append(TM.generate('DSCR-HR16',20),0.05+0.0293,'relative')
            UN04.append(TM.generate('UMOD',30),0.03+0.3491,'relative')
            UN04.append(TM.generate('UMOD',31),0.001,'relative')
            UN04.append(TM.generate('UMOD',32),0.001,'relative')
            UN04.append(TM.generate('UMOD',33),0.001,'relative')
            UN04.append(TM.generate('UMOD',34),0.001,'relative')
            UN04.append(TM.generate('UMOD',35),0.001,'relative')
            UN04.append(TM.generate('UMOD',36),0.001,'relative')
            UN04.append(TM.generate('UMOD',37),0.001,'relative')
            UN04.append(TM.generate('UMOD',38),0.001,'relative')
            UN04.append(TM.generate('DBPM-C16',40),0.03-0.0381,'relative')
            UN04.append(TM.generate('DSCR-HR16',50),0.05,'relative')
            UN04.append(TM.generate('QFF',60),0.06025-0.00775+0.005+0.0338+0.0381-0.00004-0.059,'relative')
            UN05=OMType.LineContainer('UN05',-0.027-0.07275+0.005)
            varC=OMType.VariableContainer(0.38,0)
            UN05.append(TM.generate('AFSS',100,{'angle':0.0,'design_angle':-0.1,'e1':0,'e2':1,'BC':'Athos Self-Seeding'}),0.18,'relative')
            UN05.append(TM.generate('AFSS',200,{'angle':0.0,'design_angle':0.1,'e1':1,'e2':0,'BC':'Athos Self-Seeding'}),1,varC)
            UN05.append(TM.generate('AFSS',300,{'angle':0.0,'design_angle':0.1,'e1':0,'e2':1,'BC':'Athos Self-Seeding'}),0.16,'relative')
            UN05.append(TM.generate('AFSS',400,{'angle':0.0,'design_angle':-0.1,'e1':1,'e2':0,'BC':'Athos Self-Seeding'}),1,varC)
            UN05.append(TM.generate('DBPM-C5',410),0.18+0.00775,'relative')
            UN05.append(TM.generate('QFF',420),0.06025-0.00775+0.005,'relative')

        if self.alt < 1:
            UN06=TM.generate('UE38-Cell-Empty',0,{'Name':'UN06'})
            UN07=TM.generate('UE38-Cell-Empty',0,{'Name':'UN07'})
            UN08=TM.generate('UE38-Cell-Empty',0,{'Name':'UN08'})
            UN09=TM.generate('UE38-Cell-Empty',0,{'Name':'UN09'})  # modulator goes in here.....
        else:
            UN06=TM.generate('UE38-Cell',0,{'Name':'UN06'})
            UN07=TM.generate('UE38-Cell',0,{'Name':'UN07'})
            UN08=TM.generate('UE38-Cell',0,{'Name':'UN08'}) 
            UN09=TM.generate('UE38-Cell',0,{'Name':'UN09'})

        UN10=TM.generate('UE38-Cell',0,{'Name':'UN10'})
        UN11=TM.generate('UE38-Cell',0,{'Name':'UN11'})
        UN12=TM.generate('UE38-Cell',0,{'Name':'UN12'})
        UN13=TM.generate('UE38-Cell',0,{'Name':'UN13'})

        SS=OMType.LineContainer('UN14',-0.027-0.07275+0.005)
        varC=OMType.VariableContainer(0.38,0)
        SS.append(TM.generate('AFSS',100,{'angle':0.0,'design_angle':-0.1,'e1':0,'e2':1,'BC':'Athos Self-Seeding'}),0.18,'relative')
        SS.append(TM.generate('AFSS',200,{'angle':0.0,'design_angle':0.1,'e1':1,'e2':0,'BC':'Athos Self-Seeding'}),1,varC)
        SS.append(TM.generate('AFSS',300,{'angle':0.0,'design_angle':0.1,'e1':0,'e2':1,'BC':'Athos Self-Seeding'}),0.16,'relative')
        SS.append(TM.generate('AFSS',400,{'angle':0.0,'design_angle':-0.1,'e1':1,'e2':0,'BC':'Athos Self-Seeding'}),1,varC)
        SS.append(TM.generate('DBPM-C5',410),0.18+0.00775,'relative')
        SS.append(TM.generate('QFF',420),0.06025-0.00775+0.005,'relative')
        

        UN14=TM.generate('UE38-Cell',0,{'Name':'UN15'})
        UN15=TM.generate('UE38-Cell',0,{'Name':'UN16'})
        UN16=TM.generate('UE38-Cell',0,{'Name':'UN17'})
        UN17=TM.generate('UE38-Cell',0,{'Name':'UN18'})
        UN18=TM.generate('UE38-Cell',0,{'Name':'UN19'})
        UN19=TM.generate('UE38-Cell',0,{'Name':'UN20'})
        UN20=TM.generate('UE38-Cell',0,{'Name':'UN21'})
        UN21=TM.generate('UE38-Cell-Last',0,{'Name':'UN22'})



        MA02=OMType.LineContainer('MA02',15-1.2591+1.3)
        MA02.append(TM.generate('QFF',10),1.51534,'relative')
        MA02.append(TM.generate('QFF',20),2.183,'relative')
        MA02.append(TM.generate('DBPM-C8',30),2.183-0.2,'relative')
        MA02.append(TM.generate('QFF',40),0.1,'relative')
        MA02.append(TM.generate('COL-Dechirper-H',45),0.1+0.6015-0.03,'relative')
        MA02.append(TM.generate('QFF',50),2.183-1.1-0.6015+0.03,'relative')
        MA02.append(TM.generate('DBPM-C8',60),2.183-0.2,'relative')
        MA02.append(TM.generate('QFF',70),0.1,'relative')
        if self.alt >0:
            MA02.append(TM.generate('TDS X-Band',100),2.0535-0.22+0.06,'relative')
            MA02.append(TM.generate('TDS X-Band',200),0.1,'relative')  # currently disable the second cavity


        BD01=OMType.LineContainer('BD01',0)


        BD01.append(TM.generate('QFM',10),0.15+0.12-0.06,'relative')
        BD01.append(TM.generate('DBPM-C16',20),1.1-0.3,'relative')
        BD01.append(TM.generate('QFM',30),0.2,'relative')
        BD01.append(TM.generate('SFQFM',40),0.1,'relative')
        BD01.append(TM.generate('QFM',50),1.1-0.4,'relative')
        BD01.append(TM.generate('DBPM-C16',60),1.1-0.3,'relative')
        BD01.append(TM.generate('QFM',70),0.2,'relative')
        BD01.append(TM.generate('SFQFM',80),0.1,'relative')
        BD01.append(TM.generate('QFM',90),1.1-0.4,'relative')
        BD01.append(TM.generate('DBAM-FS8',95),0.025+0.4735+0.0018+1-0.002998+0.0026,'relative')
        BD01.append(TM.generate('DBPM-C16',100),3.1-0.0685-0.2-0.237-0.1-0.4753-0.025-1+0.002998-0.0026,'relative')
        BD01.append(TM.generate('DWSC-C16',110),0.1,'relative')
        BD01.append(TM.generate('DSCR-HR16',120),0.1,'relative')
        BD01.append(TM.generate('AFD1',200,{'angle':angle,'design_angle':8,'e1':0.5,'e2':0.5,'branch':True}),0.2165+0.05,'relative')
        BD01.append(TM.generate('MKBR',201),0.0,'relative') 
        BD01.append(TM.generate('DSCR-OV38',210),5.5-1.2683-0.0044-0.94425,'relative')
        BD01.append(TM.generate('AFP1',300,{'angle':0,'design_angle':0,'e1':0,'e2':1,'Tilt':math.asin(1)}),0.363+0.0064,'relative')     
        BD01.append(TM.generate('FE-Shielding',305),2.967+0.94425,'relative')

        if (self.alt<2):
            AtLine=[SY01,SY02,SY03,CL01,DI01,CB01,CB02,MA01,UN01,UN02,UN03,UN04,UN05,UN06,UN07,UN08,UN09,UN10,UN11,UN12,UN13,SS,UN14,UN15,UN16,UN17,UN18,UN19,UN20,UN21,MA02,BD01]
        else:
            AtLine=[SY01,SY02,SY03,CL01,DI01,CB01,CB02,MA01,UN04,UN05,UN06,UN07,UN08,UN09,UN10,UN11,UN12,UN13,SS,UN14,UN15,UN16,UN17,UN18,UN19,UN20,UN21,MA02,BD01]
    
        Athos=OMType.LineContainer('AT')
        Athos.append(AtLine)

        BD02=OMType.LineContainer('BD02',0)
        BD02.append(TM.generate('DBPM-C16',10),0.4+0.02072,'relative')
        BD02.append(TM.generate('DICT-C16',20),0.12-0.0035,'relative')
        LD=1.1/math.cos(8*math.asin(1)/90)-0.92-0.1
        BD02.append(TM.generate('QFM',30),LD+0.01-0.02072+0.0035,'relative')
        LD=LD+0.3015
        BD02.append(TM.generate('DBPM-C16',40),LD+0.00317,'relative')
        BD02.append(TM.generate('DSCR-HR16',50),0.1+0.01913,'relative')
        LD=19.478/math.cos(8*math.asin(1)/90)-0.0685+0.44+0.21-0.45
        BD02.append(TM.generate('Beam-Dump-Sat',55),LD-0.00317-0.01913,'relative')
        AthosDump=OMType.LineContainer('AT')
        AthosDump.append(BD02,0,'relative')


        Linac=OMType.LineContainer('')
        Linac.append(Linac10,0,'relative')        
        Linac.append(Linac20,0,'relative')        
        Linac.append(Linac30,0,'relative')        


        SwissFEL=OMType.LineContainer('S')




        # [BeamlineInstance, ParentIndex, BranchIndex, Remark]
        # BranchIndex=-1 -> added to the end of the parent line
        # BranchIndex=0  -> Beamline is the root element

        PartsList=[[Injector,   -1, 0,'SwissFEL Injector'],            #0
                   [Linac,       0,-1,'SwissFEL Linac'],               #1
                   [Aramis,      1,-1,'Aramis beamline'],              #2
                   [Athos,       1, 2,'Athos beamline'],               #3
                   [InjectorDump,0, 1,'SwissFEL Injector beam dump'],  #4
                   [Linac1Dump,  1, 1,'Linac1 beam dump'],             #5
                   [AramisDump,  2, 1,'Aramis beam dump'],             #6
                   [AthosDump,   3, 1,'Athos beam dump']]              #7
 
        return PartsList


    def initialize(self,ElementDB):
        

        Parameters={}
        Parameters['SINLH01.MQUA020']={'k1':-0.1248942891}
        Parameters['SINLH01.MQUA030']={'k1':0.0}
        Parameters['SINLH01.MQUA040']={'k1':-2.364010703}
        Parameters['SINLH01.MQUA050']={'k1':1.534012211}
        Parameters['SINLH01.MQUA070']={'k1':1.469465702}
        Parameters['SINLH02.MQUA010']={'k1':-0.2172694024}
        Parameters['SINLH02.MQUA410']={'k1':0.6302004521}
        Parameters['SINLH03.MQUA030']={'k1':0.8650676221}
        Parameters['SINLH03.MQUA040']={'k1':-2.9998}
        Parameters['SINLH03.MQUA060']={'k1':2.172457874}
        Parameters['SINLH03.MQUA080']={'k1':-2.364503759}
        Parameters['SINSB03.MQUA130']={'k1':-1.152661876}
        Parameters['SINSB03.MQUA230']={'k1':1.009887168}
        Parameters['SINSB04.MQUA130']={'k1':-0.18310469}
        Parameters['SINSB04.MQUA230']={'k1':0.1684242647}
        Parameters['SINSB05.MQUA130']={'k1':-0.3827305491}
        Parameters['SINSB05.MQUA230']={'k1':0.3827305491}
        Parameters['SINBC01.MQUA020']={'k1':-0.6549527404}
        Parameters['SINBC01.MQUA050']={'k1':-0.09954807193}
        Parameters['SINBC01.MQUA070']={'k1':-0.1297472191}
        Parameters['SINBC01.MQUA090']={'k1':-0.3698583224}
        Parameters['SINBC01.MQUA110']={'k1':1.214785876}
        Parameters['SINBC02.MQUA110']={'k1':0.0}
        Parameters['SINBC02.MQUA120']={'k1':0.0}
        Parameters['SINBC02.MQUA340']={'k1':0.0}
        Parameters['SINBC02.MQUA350']={'k1':0.0}
        Parameters['SINDI01.MQUA020']={'k1':-1.056924525}
        Parameters['SINDI01.MQUA030']={'k1':0.0}
        Parameters['SINDI01.MQUA070']={'k1':-0.6132129554}
        Parameters['SINDI02.MQUA020']={'k1':1.307728839}
        Parameters['SINDI02.MQUA030']={'k1':0.9162121288}
        Parameters['SINDI02.MQUA050']={'k1':-0.1300784429}
        Parameters['SINDI02.MQUA060']={'k1':-0.9839853251}
        Parameters['SINDI02.MQUA070']={'k1':0.0}
        Parameters['SINDI02.MQUA090']={'k1':0.5816436339}
        Parameters['S10CB01.MQUA230']={'k1':-1.490399943}
        Parameters['S10CB01.MQUA430']={'k1':1.489935064}
        Parameters['S10CB02.MQUA230']={'k1':-1.490399943}
        Parameters['S10CB02.MQUA430']={'k1':1.489935064}
        Parameters['S10DI01.MQUA030']={'k1':0.0}
        Parameters['S10DI01.MQUA120']={'k1':-1.490399943}
        Parameters['S10CB03.MQUA230']={'k1':1.489935064}
        Parameters['S10CB03.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB04.MQUA230']={'k1':1.489935064}
        Parameters['S10CB04.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB05.MQUA230']={'k1':1.489935064}
        Parameters['S10CB05.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB06.MQUA230']={'k1':1.489935064}
        Parameters['S10CB06.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB07.MQUA230']={'k1':1.489935064}
        Parameters['S10CB07.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB08.MQUA230']={'k1':1.489935064}
        Parameters['S10CB08.MQUA430']={'k1':-1.490399943}
        Parameters['S10CB09.MQUA230']={'k1':1.489935064}
        Parameters['S10BC01.MQUA020']={'k1':1.823377711}
        Parameters['S10BC01.MQUA040']={'k1':-1.480799442}
        Parameters['S10BC01.MQUA060']={'k1':-0.4468464966}
        Parameters['S10BC01.MQUA080']={'k1':-1.143231693}
        Parameters['S10BC01.MQUA100']={'k1':1.906209865}
        Parameters['S10BC02.MQUA110']={'k1':0.0}
        Parameters['S10BC02.MQUA120']={'k1':0.0}
        Parameters['S10BC02.MQUA340']={'k1':0.0}
        Parameters['S10BC02.MQUA350']={'k1':0.0}
        Parameters['S10MA01.MQUA020']={'k1':-1.064109773}
        Parameters['S10MA01.MQUA050']={'k1':-0.07795876948}
        Parameters['S10MA01.MQUA070']={'k1':0.499548722}
        Parameters['S10MA01.MQUA110']={'k1':1.098939773}
        Parameters['S10MA01.MQUA130']={'k1':-0.4817341425}
        Parameters['S20CB01.MQUA430']={'k1':-0.8156482483}
        Parameters['S20CB02.MQUA430']={'k1':0.8156420722}
        Parameters['S20CB03.MQUA430']={'k1':-0.8156482483}
        Parameters['S20SY01.MQUA020']={'k1':1.07467527}
        Parameters['S20SY01.MQUA030']={'k1':-1.711922083}
        Parameters['S20SY01.MQUA050']={'k1':0.2355252484}
        Parameters['S20SY01.MQUA080']={'k1':1.093857674}
        Parameters['S20SY02.MQUA070']={'k1':0.05766263385}
        Parameters['S20SY02.MQUA100']={'k1':-1.402835963}
        Parameters['S20SY02.MQUA140']={'k1':0.6480723563}
        Parameters['S20SY02.MQUA180']={'k1':-0.8067664079}
        Parameters['S20SY03.MQUA020']={'k1':1.299900815}
        Parameters['S20SY03.MQUA030']={'k1':-1.251360079}
        Parameters['S20SY03.MQUA050']={'k1':0.310416242}
        Parameters['S20SY03.MQUA060']={'k1':0.8960587177}
        Parameters['S20SY03.MQUA100']={'k1':-1.169393907}
        Parameters['S30CB01.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB02.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB03.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB04.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB05.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB06.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB07.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB08.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB09.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB10.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB11.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB12.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB13.MQUA430']={'k1':0.8168945173}
        Parameters['S30CB14.MQUA430']={'k1':-0.8168918323}
        Parameters['S30CB15.MQUA430']={'k1':0.8168945173}
        Parameters['SARCL01.MQUA020']={'k1':-0.4926461486}
        Parameters['SARCL01.MQUA050']={'k1':-0.04101806243}
        Parameters['SARCL01.MQUA080']={'k1':-0.2492246765}
        Parameters['SARCL01.MQUA100']={'k1':0.2476931921}
        Parameters['SARCL01.MQUA140']={'k1':1.296780549}
        Parameters['SARCL01.MQUA190']={'k1':-1.506460951}
        Parameters['SARCL02.MQUA130']={'k1':2.47047}
        Parameters['SARCL02.MQUA150']={'k1':0.0}
        Parameters['SARCL02.MQUA160']={'k1':0.0}
        Parameters['SARCL02.MQUA210']={'k1':-1.857}
        Parameters['SARCL02.MQUA250']={'k1':1.45623}
        Parameters['SARCL02.MQUA300']={'k1':0.0}
        Parameters['SARCL02.MQUA310']={'k1':1.45623}
        Parameters['SARCL02.MQUA350']={'k1':-1.857}
        Parameters['SARCL02.MQUA420']={'k1':0.0}
        Parameters['SARCL02.MQUA430']={'k1':0.0}
        Parameters['SARCL02.MQUA460']={'k1':2.47047}
        Parameters['SARMA01.MQUA010']={'k1':-1.373019157}
        Parameters['SARMA01.MQUA060']={'k1':1.324308916}
        Parameters['SARMA01.MQUA080']={'k1':-0.5164976308}
        Parameters['SARMA01.MQUA120']={'k1':0.08774327505}
        Parameters['SARMA01.MQUA140']={'k1':0.2419885346}
        Parameters['SARMA02.MQUA050']={'k1':-1.789186727}
        Parameters['SARMA02.MQUA120']={'k1':1.814590494}
        Parameters['SARUN01.MQUA080']={'k1':-1.787193844}
        Parameters['SARUN02.MQUA080']={'k1':1.745376027}
        Parameters['SARUN03.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN04.MQUA080']={'k1':1.746023863}
        Parameters['SARUN05.MQUA080']={'k1':-1.751681566}
        Parameters['SARUN06.MQUA080']={'k1':1.715113815}
        Parameters['SARUN07.MQUA080']={'k1':-1.59306807}
        Parameters['SARUN08.MQUA420']={'k1':1.672694319}
#        Parameters['SARUN08.MQUA080']={'k1':1.672694319}
        Parameters['SARUN09.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN10.MQUA080']={'k1':1.746023863}
        Parameters['SARUN11.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN12.MQUA080']={'k1':1.746023863}
        Parameters['SARUN13.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN14.MQUA080']={'k1':1.746023863}
        Parameters['SARUN15.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN16.MQUA080']={'k1':1.746023863}
        Parameters['SARUN17.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN18.MQUA080']={'k1':1.746023863}
        Parameters['SARUN19.MQUA080']={'k1':-1.699574707}
        Parameters['SARUN20.MQUA080']={'k1':-0.781522606}
        Parameters['SARBD01.MQUA020']={'k1':-0.7159533104}
        Parameters['SATSY01.MQUA020']={'k1':-0.5}
        Parameters['SATSY01.MQUA030']={'k1':0}
        Parameters['SATSY01.MQUA040']={'k1':2.16}
        Parameters['SATSY01.MQUA070']={'k1':-2.07}
        Parameters['SATSY01.MQUA090']={'k1':0.53}
        Parameters['SATSY01.MQUA210']={'k1':0.53}
        Parameters['SATSY01.MQUA230']={'k1':-2.07}
        Parameters['SATSY01.MQUA260']={'k1':2.16}
        Parameters['SATSY01.MQUA270']={'k1':0}
        Parameters['SATSY01.MQUA280']={'k1':-0.68}
        Parameters['SATSY01.MQUA300']={'k1':0.37}
        Parameters['SATSY02.MQUA010']={'k1':-1.87}
        Parameters['SATSY02.MQUA110']={'k1':1.47}
        Parameters['SATSY02.MQUA120']={'k1':1.77}
        Parameters['SATSY02.MQUA230']={'k1':0.12}
        Parameters['SATSY03.MQUA010']={'k1':-1.89}
        Parameters['SATSY03.MQUA040']={'k1':0.64}
        Parameters['SATSY03.MQUA070']={'k1':0.81}
        Parameters['SATSY03.MQUA100']={'k1':1.83}
        Parameters['SATSY03.MQUA130']={'k1':-1.63}
        Parameters['SATCL01.MQUA120']={'k1':-0.54}
        Parameters['SATCL01.MQUA130']={'k1':1.68}
        Parameters['SATCL01.MQUA180']={'k1':1.68}
        Parameters['SATCL01.MQUA190']={'k1':-0.54}
        
        
        for idx in range(3,16):
            ele='SARUN%2.2d.UIND030' % (idx)
            if idx!=8:
                Parameters[ele]={'K':1.2}

        Parameters['SINEG01.MBND300']={'angle':30}        
        Parameters['SINLH02.UIND230']={'K':2.34}                
        Parameters['SINLH02.MBND100']={'angle':-4.1}        
        Parameters['SINLH02.MBND200']={'angle':4.1}        
        Parameters['SINLH02.MBND300']={'angle':4.1}        
        Parameters['SINLH02.MBND400']={'angle':-4.1}  
        Parameters['SINBC02.MBND100']={'angle':-3.82}        
        Parameters['SINBC02.MBND200']={'angle':3.82}        
        Parameters['SINBC02.MBND300']={'angle':3.82}        
        Parameters['SINBC02.MBND400']={'angle':-3.82}  
        Parameters['S10DI01.MBND100']={'angle':-20}        
        Parameters['S10BC02.MBND100']={'angle':-2.15}        
        Parameters['S10BC02.MBND200']={'angle':2.15}        
        Parameters['S10BC02.MBND300']={'angle':2.15}        
        Parameters['S10BC02.MBND400']={'angle':-2.15}          
        Parameters['S10MA01.MBND100']={'angle':0}
        Parameters['S20SY02.MBND200']={'angle':2} ##
        Parameters['SARCL02.MBND100']={'angle':-1}        
        Parameters['SARCL02.MBND200']={'angle':1}        
        Parameters['SARCL02.MBND400']={'angle':1}        
        Parameters['SARCL02.MBND500']={'angle':-1}             
        Parameters['SARMA02.MBND100']={'angle':0}   
        Parameters['SARUN08.MBND100']={'angle':-0.22}        
        Parameters['SARUN08.MBND200']={'angle':0.22}        
        Parameters['SARUN08.MBND300']={'angle':0.22}        
        Parameters['SARUN08.MBND400']={'angle':-0.22}  
        Parameters['SARBD01.MBND100']={'angle':8}    
        Parameters['SARBD01.MBND200']={'angle':0}   
        Parameters['SATSY01.MBND200']={'angle':1} 
        Parameters['SATSY01.MBND400']={'angle':2} 
        Parameters['SATSY02.MBND100']={'angle':0.108} 
        Parameters['SATSY02.MBND200']={'angle':-0.108} 
        Parameters['SATCL01.MBND100']={'angle':-2.5} 
        Parameters['SATCL01.MBND300']={'angle':-2.5} 
        Parameters['SATUN10.MBND100']={'angle':0.0}        
        Parameters['SATUN10.MBND200']={'angle':0.0}        
        Parameters['SATUN10.MBND300']={'angle':0.0}        
        Parameters['SATUN10.MBND400']={'angle':0.0}  
        Parameters['SATBD01.MBND100']={'angle':8.0}    
        Parameters['SATBD01.MBND200']={'angle':0}   
        Parameters['SATMA01.MBND100']={'angle':0}   # Missing?
 
         # standard RF

        Parameters['SINEG01.RGUN100']={'Gradient':33.0e6,'Phase':90.0} # Gun is added   
        Parameters['SINSB01.RACC100']={'Gradient':18.e6,'Phase':90}              
        Parameters['SINSB02.RACC100']={'Gradient':17.54e6,'Phase':90}      
        Parameters['SINSB03.RACC100']={'Gradient':16.32e6,'Phase':66.41}              
        Parameters['SINSB03.RACC200']={'Gradient':16.32e6,'Phase':66.41}      
        Parameters['SINSB04.RACC100']={'Gradient':16.32e6,'Phase':66.41}      
        Parameters['SINSB04.RACC200']={'Gradient':16.32e6,'Phase':66.41}      
        Parameters['SINXB01.RACC100']={'Gradient':18.96e6,'Phase':265.93}      
        Parameters['SINXB01.RACC200']={'Gradient':18.96e6,'Phase':265.93} 

                
        for idx in (1,2,3,4,5,6,7,8,9):
            for cell in (100,200,300,400):
                ele='S10CB%2.2d.RACC%3.3d' % (idx,cell)
                Parameters[ele]={'Gradient':28.14e6,'Phase':68.55}

        for idx in (1,2,3,4):
            for cell in range (1,5):
                ele='S20CB%2.2d.RACC%3.3d' % (idx,cell*100)
                Parameters[ele]={'Gradient':27e6,'Phase':90}
 
        for idx in (1,2,3,4,5,6,7,8,9,10,11,12,13):
            for cell in range (1,5):
                ele='S30CB%2.2d.RACC%3.3d' % (idx,cell*100)
                Parameters[ele]={'Gradient':28e6,'Phase':90}



        for e in ElementDB.keys():
            ele=ElementDB[e]
            if ele.Name in Parameters.keys():
                inputData=Parameters[ele.Name]
                for k in inputData.keys():
#                    if k=='angle':
#                        print k,'cccccccc',ele.Name
                    ele.__dict__.update({k:inputData[k]})
