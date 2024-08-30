import FWCore.ParameterSet.Config as cms

from ..modules.hltOnlineBeamSpot_cfi import *

HLTBeamSpotSequence = cms.Sequence(hltOnlineBeamSpot)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
from ..modules.hltPhase2OnlineBeamSpotDevice_cfi import hltPhase2OnlineBeamSpotDevice
_HLTBeamSpotSequence = cms.Sequence(
     hltOnlineBeamSpot
    +hltPhase2OnlineBeamSpotDevice
)
alpakaTrackingPhase2.toReplaceWith(HLTBeamSpotSequence, _HLTBeamSpotSequence)
