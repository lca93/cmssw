import FWCore.ParameterSet.Config as cms

from ..modules.siPixelClusters_cfi             import *
from ..modules.siPixelRecHits_cfi              import *

HLTDoLocalPixelSequence = cms.Sequence(siPixelClusters+siPixelRecHits)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
from ..modules.hltPhase2SiPixelClustersSoA_cfi import hltPhase2SiPixelClustersSoA
from ..modules.hltPhase2SiPixelRecHitsSoA_cfi  import hltPhase2SiPixelRecHitsSoA
from ..modules.siPixelClusterShapeCache_cfi    import siPixelClusterShapeCache
_HLTDoLocalPixelSequence = cms.Sequence(
     hltPhase2SiPixelClustersSoA
    +siPixelClusters
    +siPixelClusterShapeCache  # should we disable this? Still needed by tracker muons
    #+siPixelDigis             # not needed when copying digis from sim
    +hltPhase2SiPixelRecHitsSoA
    +siPixelRecHits
)
alpakaTrackingPhase2.toReplaceWith(HLTDoLocalPixelSequence, _HLTDoLocalPixelSequence)
