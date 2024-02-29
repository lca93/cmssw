import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelClustersCache = cms.EDProducer('SiPixelClusterShapeCacheProducer',
    src = cms.InputTag( 'hltPhase2SiPixelClusters' ),
    onDemand = cms.bool( False )
)