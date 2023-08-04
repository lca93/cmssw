import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2SiClusters_cfi import *
from ..modules.siPixelClusters_cfi import *
from ..modules.siPixelClusterShapeCache_cfi import *
from ..modules.siPixelRecHits_cfi import *

itLocalRecoTask = cms.Task(
    hltPhase2SiClusters,
    siPixelClusterShapeCache,
    siPixelClusters,
    siPixelRecHits
)
