import FWCore.ParameterSet.Config as cms

hltPhase2ESPPixelCPEFastParams = cms.ESProducer('PixelCPEFastParamsESProducerAlpakaPhase2@alpaka', 
    appendToDataLabel = cms.string(''),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    )
)