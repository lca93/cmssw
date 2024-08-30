import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelClustersSoA = cms.EDProducer('SiPixelPhase2DigiToCluster@alpaka',
    mightGet = cms.optional.untracked.vstring,
    alpaka = cms.untracked.PSet(backend = cms.untracked.string(''))
)