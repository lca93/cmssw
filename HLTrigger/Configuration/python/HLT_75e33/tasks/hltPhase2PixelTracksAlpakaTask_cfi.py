import FWCore.ParameterSet.Config as cms
from ..modules.hltPixelTracksSoA_cfi     import *
from ..modules.hltPixelTracks_cfi        import *

hltPhase2PixelTracksAlpakaTask = cms.ConditionalTask(
    hltPixelTracksSoA,
    hltPixelTracks,
)