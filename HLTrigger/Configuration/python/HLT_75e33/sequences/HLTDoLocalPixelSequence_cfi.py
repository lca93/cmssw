import FWCore.ParameterSet.Config as cms

from ..modules.siPixelClusters_cfi             import *
from ..modules.siPixelRecHits_cfi              import *

HLTDoLocalPixelSequence = cms.Sequence(siPixelClusters+siPixelRecHits)

from ..modules.hltPhase2SiPixelClustersSoA_cfi import *
from ..modules.hltPhase2SiPixelRecHitsSoA_cfi  import *
from ..modules.siPixelClusterShapeCache_cfi    import siPixelClusterShapeCache
_HLTDoLocalPixelSequence = cms.Sequence(
    hltPhase2SiPixelClustersSoA
    +siPixelClusters
    +siPixelClusterShapeCache  # should we disable this? Still needed by tracker muons
    +hltPhase2SiPixelRecHitsSoA
    +siPixelRecHits
)

from Configuration.ProcessModifiers.alpaka_cff import alpaka
alpaka.toReplaceWith(HLTDoLocalPixelSequence, _HLTDoLocalPixelSequence)
