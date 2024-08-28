import FWCore.ParameterSet.Config as cms

def _TrimmedVertices(process):
  ''' define the modules needed for producing the trimmed pixel vertex collection
  '''
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
  return process

def _InitialStep(process):
  ''' modify the initialStep to select only tracks compatible with a pixel vertex
  from the trimmed collection
  '''
  process.initialStepSeeds.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
  return process

def _HighPtTripletStep(process):
  #!!! DOES NOT WORK !!! (missing PV tracking region module, does it exist?)
  ''' modify the initialStep to select only tracks compatible with a pixel vertex
  from the trimmed collection.
  '''
  process.highPtTripletStepSeeds.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
  #process.hltTrackingRegionFromTrimmedPixelVertices = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
  #  RegionPSet  = cms.PSet(
  #    beamSpot                      = cms.InputTag("hltOnlineBeamSpot"),
  #    deltaEta                      = cms.double(0.5),
  #    deltaPhi                      = cms.double(0.3),
  #    input                         = cms.InputTag(""),
  #    maxNRegions                   = cms.int32(10),
  #    maxNVertices                  = cms.int32(1),
  #    measurementTrackerName        = cms.InputTag(""),
  #    mode                          = cms.string('VerticesFixed'),
  #    nSigmaZBeamSpot               = cms.double(0.0),
  #    nSigmaZVertex                 = cms.double(0.0),
  #    originRadius                  = cms.double(0.3),
  #    precise                       = cms.bool(True),
  #    ptMin                         = cms.double(0.9),
  #    searchOpt                     = cms.bool(False),
  #    vertexCollection              = cms.InputTag("hltTrimmedPixelVertices"),
  #    whereToUseMeasurementTracker  = cms.string('Never'),
  #    zErrorBeamSpot                = cms.double(0.0),
  #    zErrorVetex                   = cms.double(1.5)
  #  )
  #)
  #process.highPtTripletStepHitDoublets.trackingRegions = cms.InputTag("hltTrackingRegionFromTrimmedPixelVertices")
  process.highPtTripletStepSequence = cms.Sequence(process.highPtTripletStepClusters
    +process.highPtTripletStepSeedLayers
    #+process.hltTrackingRegionFromTrimmedPixelVertices
    +process.highPtTripletStepHitDoublets
    +process.highPtTripletStepHitTriplets
    +process.highPtTripletStepSeeds
    +process.highPtTripletStepTrackCandidates
    +process.highPtTripletStepTracks
    +process.highPtTripletStepTrackCutClassifier
    +process.highPtTripletStepTrackSelectionHighPurity
  )

  return process

def _InitialStepOnly(process):
  ''' remove the highPtTripleStep from the full tracking (testing purpose)
  '''
  process.generalTracks.TrackProducers     = cms.VInputTag("initialStepTrackSelectionHighPurity")
  process.generalTracks.selectedTrackQuals = cms.VInputTag(cms.InputTag("initialStepTrackSelectionHighPurity"))
  process.generalTracks.hasSelector        = cms.vint32(0)
  process.generalTracks.indivShareFrac     = cms.vdouble(1.0)
  process.generalTracks.setsToMerge        = cms.VPSet(cms.PSet( # what does this do?
    pQual   = cms.bool(True),
    tLists  = cms.vint32(0)
  ))

  return process

def _TrackingOnly(process):
  ''' remove everything but the tracking sequence from the menu
  '''
  process.HLTTrackingV61Sequence = cms.Sequence((process.itLocalRecoSequence
    +process.otLocalRecoSequence
    +process.trackerClusterCheck
    +process.hltPhase2PixelTracksSequence
    +process.hltPhase2PixelVertices
    +process.hltTrimmedPixelVertices
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
  ''' main function for trimmed tracking (run the full menu)
  '''
  process = _TrimmedVertices(process)
  process = _InitialStep(process)
  process = _HighPtTripletStep(process)
  #process = _InitialStepOnly(process)
  
  return process

def customizeHLTforTrimmedTrackingTrackingOnly(process):
  ''' main function for trimmed tracking (run only the tracking sequence)
  '''
  import pdb; pdb.set_trace()
  process = customizeHLTforTrimmedTracking(process)
  process = _TrackingOnly(process)
  return process