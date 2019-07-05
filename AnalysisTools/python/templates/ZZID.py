from UWVV.AnalysisTools.AnalysisFlowBase import AnalysisFlowBase

import FWCore.ParameterSet.Config as cms


class ZZID(AnalysisFlowBase):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'year'):
            self.year = kwargs.pop('year', '2016')

        super(ZZID, self).__init__(*args, **kwargs)

    def makeAnalysisStep(self, stepName, **inputs):
        step = super(ZZID, self).makeAnalysisStep(stepName, **inputs)

        LeptonSetup = cms.string(self.year)
        if stepName == 'embedding':
            if LeptonSetup=="2016":
                eIDEmbedder = cms.EDProducer(
                    "PATElectronZZIDEmbedder",
                    src = step.getObjTag('e'),
                    idLabel = cms.string(self.getZZIDLabel()),
                    vtxSrc = step.getObjTag('v'),
                    #Cuts and IDs differ by year: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4lRunIILegacy#Electrons
                    bdtLabel=cms.string("ElectronMVAEstimatorRun2Summer16IdIsoValues"),#2016 version of the ID
                    idCutLowPtLowEta = cms.double(0.95034841889),
                    idCutLowPtMedEta = cms.double(0.94606270058),
                    idCutLowPtHighEta = cms.double(0.93872558098),
                    idCutHighPtLowEta = cms.double(0.3782357877),
                    idCutHighPtMedEta = cms.double(0.35871320305),
                    idCutHighPtHighEta = cms.double(-0.57451499543),
                    missingHitsCut = cms.int32(999),
                    ptCut = cms.double(7.), 
                )
            if LeptonSetup=="2017":
                eIDEmbedder = cms.EDProducer(
                    "PATElectronZZIDEmbedder",
                    src = step.getObjTag('e'),
                    idLabel = cms.string(self.getZZIDLabel()),
                    vtxSrc = step.getObjTag('v'),
                    bdtLabel=cms.string("ElectronMVAEstimatorRun2Fall17IsoV2Values"),#2017 version of the ID
                    idCutLowPtLowEta = cms.double(0.85216885148),
                    idCutLowPtMedEta = cms.double(0.82684550976),
                    idCutLowPtHighEta = cms.double(0.86937630022),
                    idCutHighPtLowEta = cms.double(0.98248928759),
                    idCutHighPtMedEta = cms.double(0.96919224579),
                    idCutHighPtHighEta = cms.double(0.79349796445),
                    missingHitsCut = cms.int32(999),
                    ptCut = cms.double(7.), 
                )
            if LeptonSetup=="2018":
                print "LeptonSetup:",LeptonSetup
                eIDEmbedder = cms.EDProducer(
                    "PATElectronZZIDEmbedder",
                    src = step.getObjTag('e'),
                    idLabel = cms.string(self.getZZIDLabel()),
                    vtxSrc = step.getObjTag('v'),
                    bdtLabel=cms.string("ElectronMVAEstimatorRun2Autumn18IdIsoValues"),#2018 version of the ID
                    idCutLowPtLowEta = cms.double(0.8955937602),
                    idCutLowPtMedEta = cms.double(0.91106464032),
                    idCutLowPtHighEta = cms.double(0.94067753025),
                    idCutHighPtLowEta = cms.double(0.04240620843),
                    idCutHighPtMedEta = cms.double(0.0047338429),
                    idCutHighPtHighEta = cms.double(-0.60423293572),
                    missingHitsCut = cms.int32(999),
                    ptCut = cms.double(7.), 
                )
                #HZZWP = cms.string("mvaEleID-Fall17-iso-V2-wpHZZ"),#2018 version

            mIDEmbedder = cms.EDProducer(
                "PATMuonZZIDEmbedder",
                src = step.getObjTag('m'),
                vtxSrc = step.getObjTag('v'),
                ptCut = cms.double(5.),
                idLabel = cms.string(self.getZZIDLabel()),
                )

            step.addModule("eZZIDEmbedder", eIDEmbedder, 'e')
            step.addModule("mZZIDEmbedder", mIDEmbedder, 'm')

        return step

    def getZZIDLabel(self):
        return 'ZZIDPass'
