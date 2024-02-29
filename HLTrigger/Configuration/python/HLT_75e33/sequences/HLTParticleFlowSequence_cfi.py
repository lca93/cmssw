import FWCore.ParameterSet.Config as cms

#from ..tasks.HLTParticleFlowTask_cfi import *
from ..tasks.hltPhase2ParticleFlowTask_cfi import *

HLTParticleFlowSequence = cms.Sequence(
    #HLTParticleFlowTask
    hltPhase2ParticleFlowTask
)
