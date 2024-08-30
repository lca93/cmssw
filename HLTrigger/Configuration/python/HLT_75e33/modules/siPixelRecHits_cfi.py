import FWCore.ParameterSet.Config as cms

siPixelRecHits = cms.EDProducer("SiPixelRecHitConverter",
    CPE = cms.string('PixelCPEGeneric'),
    VerboseLevel = cms.untracked.int32(0),
    src = cms.InputTag("siPixelClusters")
)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
alpakaTrackingPhase2.toReplaceWith(siPixelRecHits, cms.EDProducer('SiPixelRecHitFromSoAAlpakaPhase2',
    pixelRecHitSrc = cms.InputTag('hltPhase2SiPixelRecHitsSoA'),
    src = cms.InputTag('siPixelClusters'),
))
