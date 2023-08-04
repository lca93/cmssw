import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2SiClusters_cfi import *

pixeltrackerlocalrecoTask = cms.Task(
    hltPhase2SiClusters,
)
