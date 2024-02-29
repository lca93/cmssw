import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelRecHits = cms.EDProducer('SiPixelRecHitFromSoAAlpakaPhase2',
    pixelRecHitSrc = cms.InputTag('hltPhase2SiPixelRecHitsSoA'),
    src = cms.InputTag('hltPhase2SiPixelClusters'),
)