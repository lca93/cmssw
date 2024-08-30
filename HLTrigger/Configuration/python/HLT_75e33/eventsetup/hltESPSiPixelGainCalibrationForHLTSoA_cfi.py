import FWCore.ParameterSet.Config as cms

hltESPSiPixelGainCalibrationForHLTSoA = cms.ESProducer('SiPixelGainCalibrationForHLTSoAESProducer@alpaka',
    appendToDataLabel = cms.string(''),
    alpaka = cms.untracked.PSet(backend = cms.untracked.string(''))
)