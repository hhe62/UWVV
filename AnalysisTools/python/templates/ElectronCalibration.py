from UWVV.AnalysisTools.AnalysisFlowBase import AnalysisFlowBase

import FWCore.ParameterSet.Config as cms

class ElectronCalibration(AnalysisFlowBase):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'isMC'):
            self.isMC = kwargs.pop('isMC', True)
        if not hasattr(self, 'isSync'):
            self.isSync = self.isMC and kwargs.pop('isSync', False)

        if not hasattr(self, 'year'):
            self.year = kwargs.pop('year', '2016')

        eesShift = kwargs.pop('electronScaleShift', 0) if self.isMC else 0
        eerRhoShift = kwargs.pop('electronRhoResShift', 0) if self.isMC else 0
        eerPhiShift = kwargs.pop('electronPhiResShift', 0) if self.isMC else 0
        if not hasattr(self, 'electronScaleShift'):
            self.electronScaleShift = eesShift
        if not hasattr(self, 'electronRhoResShift'):
            self.electronRhoResShift = eerRhoShift
        if not hasattr(self, 'electronPhiResShift'):
            self.electronPhiResShift = eerPhiShift

        super(ElectronCalibration, self).__init__(*args, **kwargs)

    def makeAnalysisStep(self, stepName, **inputs):
        step = super(ElectronCalibration, self).makeAnalysisStep(stepName, **inputs)

        if stepName == 'preliminary':

            if not hasattr(self.process, 'RandomNumberGeneratorService'):
                self.process.RandomNumberGeneratorService = cms.Service(
                    'RandomNumberGeneratorService',
                    )
            LeptonSetup = cms.string(self.year)
            #https://twiki.cern.ch/twiki/bin/view/CMS/EgammaPostRecoRecipes
            #fix a bug in the ECAL-Tracker momentum combination when applying the scale and smearing
            from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
            if LeptonSetup=="2016":
                setupEgammaPostRecoSeq(self.process,
                        runEnergyCorrections=True,
                        runVID=True,
                        eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Summer16_ID_ISO_cff','RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'],
                        era='2016-Legacy')

            if LeptonSetup=="2017":
                setupEgammaPostRecoSeq(self.process,
                        runEnergyCorrections=True,
                        runVID=True,
                        era='2017-Nov17ReReco',
                        )

            if LeptonSetup=="2018":
                setupEgammaPostRecoSeq(self.process,
                        runEnergyCorrections=True,
                        runVID=True,
                        eleIDModules=['RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Autumn18_ID_ISO_cff','RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV70_cff'],
                        era='2018-Prompt'
                        )
            
            step.addModule('egammaPostRecoSeq',self.process.egammaPostRecoSeq)

            if self.electronScaleShift or self.electronRhoResShift or self.electronPhiResShift:
                self.process.RandomNumberGeneratorService.electronSystematicShift = cms.PSet(
                    initialSeed = cms.untracked.uint32(345),
                    )

                shiftMod = cms.EDProducer(
                    "PATElectronSystematicShifter",
                    src = step.getObjTag('e'),
                    correctionFile = cms.string(correctionFile),
                    scaleShift = cms.double(self.electronScaleShift),
                    rhoResShift = cms.double(self.electronRhoResShift),
                    phiResShift = cms.double(self.electronPhiResShift),
                    )

                step.addModule('electronSystematicShift', shiftMod, 'e')

        if stepName == 'selection':
            # need to re-sort now that we're calibrated
            eSort = cms.EDProducer(
                "PATElectronCollectionSorter",
                src = step.getObjTag('e'),
                function = cms.string('pt'),
                )
            step.addModule('electronSorting', eSort, 'e')

        return step
