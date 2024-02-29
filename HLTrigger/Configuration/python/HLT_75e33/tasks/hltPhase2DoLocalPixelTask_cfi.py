import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2SiPixelClusters_cfi import *
from ..modules.hltPhase2SiPixelRecHits_cfi import *

hltPhase2DoLocalPixelTask = cms.Task(
    hltPhase2SiPixelClusters,
    hltPhase2SiPixelRecHits
)
