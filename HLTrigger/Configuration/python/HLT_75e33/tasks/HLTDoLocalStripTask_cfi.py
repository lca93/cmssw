import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2SiClusters_cfi import *

HLTDoLocalStripTask = cms.Task(
    hltPhase2SiClusters,
)
