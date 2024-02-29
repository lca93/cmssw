import FWCore.ParameterSet.Config as cms

hltPhase2ESPSiPixelGainCalibrationForHLTSoA = cms.ESProducer('SiPixelGainCalibrationForHLTSoAESProducer@alpaka',
    appendToDataLabel = cms.string(''),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    )
)