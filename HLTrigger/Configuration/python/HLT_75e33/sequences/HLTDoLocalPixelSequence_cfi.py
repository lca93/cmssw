import FWCore.ParameterSet.Config as cms

#from ..tasks.HLTDoLocalPixelTask_cfi import *
from ..tasks.hltPhase2DoLocalPixelTask_cfi import *

HLTDoLocalPixelSequence = cms.Sequence(
    hltPhase2DoLocalPixelTask
)
