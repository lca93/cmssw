import FWCore.ParameterSet.Config as cms

def customizeHLTforTrimmedTrackingInitialStep(process):
  process.hltESPTTRHBuilderPixelOnly = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    ComponentName                       = cms.string("hltESPTTRHBuilderPixelOnly"),
    ComputeCoarseLocalPositionFromDisk  = cms.bool(False),
    StripCPE                            = cms.string("Fake"),
    PixelCPE                            = cms.string("PixelCPEGeneric"),
    Matcher                             = cms.string("StandardMatcher"),
    Phase2StripCPE                      = cms.string(""),
    appendToDataLabel                   = cms.string("")
  )
  process.HLTPSetPvClusterComparerForIT = cms.PSet( 
    track_chi2_max  = cms.double(20.0),
    track_pt_max    = cms.double(20.0),
    track_prob_min  = cms.double(-1.0),
    track_pt_min    = cms.double(1.0)
  )
  process.hltTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
    src             = cms.InputTag("hltPhase2PixelVertices"),
    maxVtx          = cms.uint32(100),
    fractionSumPt2  = cms.double(0.5),
    minSumPt2       = cms.double(0.0),
    PVcomparer      = cms.PSet(refToPSet_=cms.string("HLTPSetPvClusterComparerForIT"))
  )
  process.HLTSeedFromProtoTracks = cms.PSet( 
    TTRHBuilder                       = cms.string("hltESPTTRHBuilderPixelOnly"),
    SeedMomentumForBOFF               = cms.double(5.0),
    propagator                        = cms.string("PropagatorWithMaterialParabolicMf"),
    forceKinematicWithRegionDirection = cms.bool(False),
    magneticField                     = cms.string("ParabolicMf"),
    OriginTransverseErrorMultiplier   = cms.double(1.0),
    ComponentName                     = cms.string("SeedFromConsecutiveHitsCreator"),
    MinOneOverPtError                 = cms.double(1.0)
  )
  process.initialStepSeeds = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
    InputCollection         = cms.InputTag("hltPhase2PixelTracks"),
    InputVertexCollection   = cms.InputTag("hltTrimmedPixelVertices"),
    originHalfLength        = cms.double(0.3),
    originRadius            = cms.double(0.1),
    useProtoTrackKinematics = cms.bool(False),
    useEventsWithNoVertex   = cms.bool(True ),
    TTRHBuilder             = cms.string("WithTrackAngle"),
    usePV                   = cms.bool(False),
    includeFourthHit        = cms.bool(True ),
    produceComplement       = cms.bool(False),
    SeedCreatorPSet         = cms.PSet(refToPSet_=cms.string("seedFromProtoTracks"))
  )
  process.initialStepSequence = cms.Sequence(process.hltTrimmedPixelVertices
    +process.initialStepSeeds
    +process.initialStepTrackCandidates
    +process.initialStepTracks
    +process.initialStepTrackCutClassifier
    +process.initialStepTrackSelectionHighPurity
  )

  return process

def customizeHLTforTrimmedTrackingHighPtTripletStep(process):
  process.hltPhase2PixelTracksAndHighPtStepTrackingRegions = None
  process.hltPhase2PixelTracksSequence = cms.Sequence(process.hltPhase2PixelTracksSeedLayers
    +process.hltPhase2PixelTracksAndHighPtStepTrackingRegions
    +process.hltPhase2PixelTracksHitDoublets
    +process.hltPhase2PixelTracksHitSeeds
    +process.hltPhase2PixelFitterByHelixProjections
    +process.hltPhase2PixelTrackFilterByKinematics
    +process.hltPhase2PixelTracks
  )


def customizeHLTforTrimmedTrackingTrackingOnly(process):
  process.HLTTrackingV61Sequence = cms.Sequence((process.itLocalRecoSequence
    +process.otLocalRecoSequence
    +process.trackerClusterCheck
    +process.hltPhase2PixelTracksSequence
    +process.hltPhase2PixelVertices
    +process.initialStepSequence
    +process.highPtTripletStepSequence
    +process.generalTracks
  ))
  process.HLT_TrackingOnly = cms.Path(process.HLTBeginSequence
    +process.HLTTrackingV61Sequence
    +process.HLTEndSequence
  )
  process.outputmodule = cms.EndPath(*[getattr(process, outmod) for outmod in process.outputModules.keys()])
  process.schedule = cms.Schedule(*[
      process.HLT_TrackingOnly,
      process.endjob_step,
      process.outputmodule
  ])
  
  return process

def customizeHLTforTrimmedTracking(process):
  import pdb; pdb.set_trace()
  process = customizeHLTforTrimmedTrackingInitialStep(process)
  process = customizeHLTforTrimmedTrackingTrackingOnly(process)
  
  return process