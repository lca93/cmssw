import FWCore.ParameterSet.Config as cms

hltPhase2PixelTracks = cms.EDProducer("PixelTrackProducer",
    Cleaner = cms.string('pixelTrackCleanerBySharedHits'),
    Filter = cms.InputTag("hltPhase2PixelTrackFilterByKinematics"),
    Fitter = cms.InputTag("hltPhase2PixelFitterByHelixProjections"),
    SeedingHitSets = cms.InputTag("hltPhase2PixelTracksHitSeeds"),
    mightGet = cms.optional.untracked.vstring,
    passLabel = cms.string('hltPhase2PixelTracks')
)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
alpakaTrackingPhase2.toReplaceWith(hltPhase2PixelTracks, cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase2",
    beamSpot = cms.InputTag("hltOnlineBeamSpot"),
    minNumberOfHits = cms.int32(0),
    minQuality = cms.string('tight'),
    pixelRecHitLegacySrc = cms.InputTag("siPixelRecHits"),
    trackSrc = cms.InputTag("hltPhase2PixelTracksSoA")
))
