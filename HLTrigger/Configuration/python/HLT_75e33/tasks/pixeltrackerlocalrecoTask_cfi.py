import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2SiClusters_cfi import *

hltPhase2PixeltrackerlocalrecoTask = cms.Task(
    hltPhase2SiClusters,
)
