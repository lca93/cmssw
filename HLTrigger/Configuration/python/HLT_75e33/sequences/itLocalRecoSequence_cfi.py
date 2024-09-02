import FWCore.ParameterSet.Config as cms

from ..modules.siPhase2Clusters_cfi import *
from ..modules.siPixelClusters_cfi import *
from ..modules.siPixelClusterShapeCache_cfi import *
from ..modules.siPixelRecHits_cfi import *

itLocalRecoSequence = cms.Sequence(siPhase2Clusters+siPixelClusters+siPixelClusterShapeCache+siPixelRecHits)

from Configuration.ProcessModifiers.alpaka_cff import alpaka
from ..sequences.HLTDoLocalStripSequence_cfi import *
from ..sequences.HLTDoLocalPixelSequence_cfi import *
_itLocalRecoSequence = cms.Sequence(
     HLTDoLocalStripSequence
    +HLTDoLocalPixelSequence
)

alpaka.toReplaceWith(itLocalRecoSequence, _itLocalRecoSequence)