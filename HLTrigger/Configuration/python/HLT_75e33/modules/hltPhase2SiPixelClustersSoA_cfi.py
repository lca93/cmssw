import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelClustersSoA = cms.EDProducer(
    "SiPixelPhase2DigiToCluster@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    )
)