import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2PixelFitterByHelixProjections_cfi import *
from ..modules.hltPhase2PixelTrackFilterByKinematics_cfi import *
from ..modules.hltPhase2PixelTracks_cfi import *
from ..modules.hltPhase2PixelTracksAndHighPtStepTrackingRegions_cfi import *
from ..modules.hltPhase2PixelTracksHitDoublets_cfi import *
from ..modules.hltPhase2PixelTracksHitSeeds_cfi import *
from ..modules.hltPhase2PixelTracksSeedLayers_cfi import *

hltPhase2PixelTracksSequence = cms.Sequence(hltPhase2PixelTracksSeedLayers+hltPhase2PixelTracksAndHighPtStepTrackingRegions+hltPhase2PixelTracksHitDoublets+hltPhase2PixelTracksHitSeeds+hltPhase2PixelFitterByHelixProjections+hltPhase2PixelTrackFilterByKinematics+hltPhase2PixelTracks)

from Configuration.ProcessModifiers.alpakaTrackingPhase2_cff import alpakaTrackingPhase2
from ..sequences.HLTBeamSpotSequence_cfi import HLTBeamSpotSequence
from ..modules.hltPhase2PixelTracksSoA_cfi import hltPhase2PixelTracksSoA
_hltPhase2PixelTracksSequence = cms.Sequence(
   HLTBeamSpotSequence
  +hltPhase2PixelTracksAndHighPtStepTrackingRegions # needed by highPtTripletStep iteration
  +hltPhase2PixelFitterByHelixProjections # needed by tracker muons
  +hltPhase2PixelTrackFilterByKinematics  # needed by tracker muons
  +hltPhase2PixelTracksSoA
  +hltPhase2PixelTracks
)
alpakaTrackingPhase2.toReplaceWith(hltPhase2PixelTracksSequence, _hltPhase2PixelTracksSequence)
