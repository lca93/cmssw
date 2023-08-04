import FWCore.ParameterSet.Config as cms

hltElePixelHitTripletsClusterRemoverUnseeded = cms.EDProducer("SeedClusterRemoverPhase2",
    phase2OTClusters = cms.InputTag("hltPhase2SiClusters"),
    pixelClusters = cms.InputTag("siPixelClusters"),
    trajectories = cms.InputTag("hltElePixelSeedsTripletsUnseeded")
)
