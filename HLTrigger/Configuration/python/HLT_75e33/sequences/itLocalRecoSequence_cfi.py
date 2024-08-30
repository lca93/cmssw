import FWCore.ParameterSet.Config as cms

from ..modules.siPhase2Clusters_cfi import *
from ..modules.siPixelClusters_cfi import *
from ..modules.siPixelClusterShapeCache_cfi import *
from ..modules.siPixelRecHits_cfi import *

itLocalRecoSequence = cms.Sequence(siPhase2Clusters+siPixelClusters+siPixelClusterShapeCache+siPixelRecHits)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
from ..sequences.HLTDoLocalStripSequence_cfi import HLTDoLocalStripSequence
from ..sequences.HLTDoLocalPixelSequence_cfi import HLTDoLocalPixelSequence
_itLocalRecoSequence = cms.Sequence(
     HLTDoLocalStripSequence
    +HLTDoLocalPixelSequence
)
alpakaTrackingPhase2.toReplaceWith(itLocalRecoSequence, _itLocalRecoSequence)
