import FWCore.ParameterSet.Config as cms

hltESPSiPixelCablingSoA = cms.ESProducer('SiPixelCablingSoAESProducer@alpaka', 
    CablingMapLabel = cms.string(''),
    UseQualityInfo = cms.bool(False),
    appendToDataLabel = cms.string(''),
    alpaka = cms.untracked.PSet(backend = cms.untracked.string(''))
)