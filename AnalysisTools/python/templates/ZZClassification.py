from UWVV.AnalysisTools.templates.JetQuarkGluonTagging import JetQuarkGluonTagging

import FWCore.ParameterSet.Config as cms


class ZZClassification(JetQuarkGluonTagging):
    def __init__(self, *args, **kwargs):
        if not hasattr(self, 'year'):
            self.year = kwargs.pop('year', '2016')

        super(ZZClassification, self).__init__(*args, **kwargs)

    def makeAnalysisStep(self, stepName, **inputs):
        step = super(ZZClassification, self).makeAnalysisStep(stepName, **inputs)

        LeptonSetup = cms.string(self.year)
        
        if stepName == 'initialStateEmbedding':
            meEmbedding4e = cms.EDProducer(
                "ZZDiscriminantEmbedderEEEE",
                src = step.getObjTag('eeee'),
                jetSrc = step.getObjTag('j'),
                fsrLabel = cms.string(self.getFSRLabel()),
                qgDiscriminator = cms.string(self.qgLikelihoodLabel()),
                skimDecisionLabels = cms.vstring(
                    '{}Tight'.format(self.getZZIDLabel()),
                    self.getZZIsoLabel(),
                    ),
                )
            step.addModule('meEmbedding4e', meEmbedding4e, 'eeee')
                
            meEmbedding2e2m = cms.EDProducer(
                "ZZDiscriminantEmbedderEEMM",
                src = step.getObjTag('eemm'),
                jetSrc = step.getObjTag('j'),
                fsrLabel = cms.string(self.getFSRLabel()),
                qgDiscriminator = cms.string(self.qgLikelihoodLabel()),
                skimDecisionLabels = cms.vstring(
                    '{}Tight'.format(self.getZZIDLabel()),
                    self.getZZIsoLabel(),
                    ),
                )
            step.addModule('meEmbedding2e2m', meEmbedding2e2m, 'eemm')
                
            meEmbedding4m = cms.EDProducer(
                "ZZDiscriminantEmbedderMMMM",
                src = step.getObjTag('mmmm'),
                jetSrc = step.getObjTag('j'),
                fsrLabel = cms.string(self.getFSRLabel()),
                qgDiscriminator = cms.string(self.qgLikelihoodLabel()),
                skimDecisionLabels = cms.vstring(
                    '{}Tight'.format(self.getZZIDLabel()),
                    self.getZZIsoLabel(),
                    ),
                )
            step.addModule('meEmbedding4m', meEmbedding4m, 'mmmm')
            
             
            if LeptonSetup=="2016":
                btagWP = cms.double(0.6321);
            if LeptonSetup=="2018":
                btagWP = cms.double(0.4941);
            if LeptonSetup=="2018":
                btagWP = cms.double(0.4184);

            categoryEmbedding4e = cms.EDProducer(
                'ZZCategoryEmbedder',
                src = step.getObjTag('eeee'),
                electronSrc = step.getObjTag('e'),
                muonSrc = step.getObjTag('m'),
                jetSrc = step.getObjTag('j'),
                leptonSelection = cms.string('userFloat("{}Tight") > 0.5 && userFloat("{}") > 0.5'.format(self.getZZIDLabel(), self.getZZIsoLabel())),
                bDiscriminator = cms.string('pfDeepCSVJetTags:probb'),# + pfDeepCSVJetTags:probbb'),
                bDiscriminatorCut = cms.double(btagWP),
                )
            step.addModule('categoryEmbedding4e', categoryEmbedding4e, 'eeee')

            categoryEmbedding2e2m = cms.EDProducer(
                'ZZCategoryEmbedder',
                src = step.getObjTag('eemm'),
                electronSrc = step.getObjTag('e'),
                muonSrc = step.getObjTag('m'),
                jetSrc = step.getObjTag('j'),
                leptonSelection = cms.string('userFloat("{}Tight") > 0.5 && userFloat("{}") > 0.5'.format(self.getZZIDLabel(), self.getZZIsoLabel())),
                bDiscriminator = cms.string('pfDeepCSVJetTags:probb'),#+ pfDeepCSVJetTags:probbb'),
                bDiscriminatorCut = cms.double(btagWP),
                )
            step.addModule('categoryEmbedding2e2m', categoryEmbedding2e2m, 'eemm')

            categoryEmbedding4m = cms.EDProducer(
                'ZZCategoryEmbedder',
                src = step.getObjTag('mmmm'),
                electronSrc = step.getObjTag('e'),
                muonSrc = step.getObjTag('m'),
                jetSrc = step.getObjTag('j'),
                leptonSelection = cms.string('userFloat("{}Tight") > 0.5 && userFloat("{}") > 0.5'.format(self.getZZIDLabel(), self.getZZIsoLabel())),
                bDiscriminator = cms.string('pfDeepCSVJetTags:probb'),# + pfDeepCSVJetTags:probbb'),
                bDiscriminatorCut = cms.double(btagWP),
                )
            step.addModule('categoryEmbedding4m', categoryEmbedding4m, 'mmmm')


        return step

