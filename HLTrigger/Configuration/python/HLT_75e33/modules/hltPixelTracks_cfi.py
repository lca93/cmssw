import FWCore.ParameterSet.Config as cms

hltPixelTracks = cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase2",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    minNumberOfHits = cms.int32(0),
    minQuality = cms.string('loose'),
    pixelRecHitLegacySrc = cms.InputTag("hltSiPixelRecHits"),
    trackSrc = cms.InputTag("hltPixelTracksSoA")
)