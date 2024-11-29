import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import producers_by_type

def customizeHLTforTrimmedTrackingVertexing(process):
  ''' define the modules needed for producing the trimmed pixel vertex collection
  '''
  #process.pSetPvClusterComparerForIT = cms.PSet( 
  #  track_chi2_max  = cms.double(20.0),
  #  track_pt_max    = cms.double(20.0),
  #  track_prob_min  = cms.double(-1.0),
  #  track_pt_min    = cms.double(1.0)
  #)
  process.hltTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
    src             = cms.InputTag("hltPhase2PixelVertices"),
    maxVtx          = cms.uint32(300),
    fractionSumPt2  = cms.double(0.3),
    minSumPt2       = cms.double(0.0),
    PVcomparer      = cms.PSet(refToPSet_=cms.string("pSetPvClusterComparerForIT"))
  )
  process.HLTTrackingV61Sequence.insert(process.HLTTrackingV61Sequence.index(process.hltPhase2PixelVertices)+1, process.hltTrimmedPixelVertices)
  return process

def customizeHLTforTrimmedTrackingInitialStep(process):
  ''' modify the initialStep to select only tracks compatible with a pixel vertex
  from the trimmed collection
  '''
  process.hltInitialStepSeeds.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
  '''
  could put instead:
  for producer in producers_by_type(process, "SeedGeneratorFromProtoTracksEDProducer"):
    producer.InputVertexCollection  = cms.InputTag("hltTrimmedPixelVertices")
  '''
  return process

def customizeHLTforTrimmedTrackingHighPtTripletStep(process):
  ''' modify the highPtTripletStep to select only doublets compatible with a pixel vertex
  from the trimmed collection.
  '''
  process.hltTrackingRegionFromTrimmedVertices = cms.EDProducer('GlobalTrackingRegionWithVerticesEDProducer',
    RegionPSet = cms.PSet(
      ptMin                   = cms.double(0.5),
      beamSpot                = cms.InputTag('hltOnlineBeamSpot'),
      #pixelClustersForScaling = cms.InputTag('hltSiPhase2Clusters'),
      VertexCollection        = cms.InputTag('hltTrimmedPixelVertices'),
    ),
    mightGet = cms.optional.untracked.vstring,
  )
  process.hltHighPtTripletStepHitDoublets.trackingRegions = cms.InputTag('hltTrackingRegionFromTrimmedVertices')
  process.HLTHighPtTripletStepSequence.insert(0, process.hltTrackingRegionFromTrimmedVertices)
  return process

def HLTTrackingPath(process):
    ''' Create a tracking-only path
    '''
    process.HLT_TrackingPath = cms.Path()
    process.HLT_TrackingPath.insert(item=process.HLTBeginSequence       , index=len(process.HLT_TrackingPath.moduleNames()))
    process.HLT_TrackingPath.insert(item=process.HLTTrackingV61Sequence , index=len(process.HLT_TrackingPath.moduleNames()))
    process.HLT_TrackingPath.insert(item=process.HLTEndSequence         , index=len(process.HLT_TrackingPath.moduleNames()))
    process.outputmodule = cms.EndPath(process.FEVTDEBUGHLToutput)
    process.schedule.insert(-4, process.HLT_TrackingPath)
    return process

def customizeHLTforTrimmedTracking(process):
  ''' main function for trimmed tracking (run the full menu)
  '''
  process = customizeHLTforTrimmedTrackingVertexing(process)
  #process = customizeHLTforTrimmedTrackingInitialStep(process)
  process = customizeHLTforTrimmedTrackingHighPtTripletStep(process)
  return process

def customizeHLTforTrimmedTrackingTrackingOnly(process):
  ''' main function for trimmed tracking (run only the tracking sequence)
  '''
  process = customizeHLTforTrimmedTracking(process)
  process = HLTTrackingPath(process)
  process.schedule = cms.Schedule(*[
    process.HLT_TrackingPath,
    process.endjob_step,
    process.outputmodule
  ])
  return process

def customizeHLTforTrimmedTrackingMixedPF(process):
  # Use the standard trimmed tracking
  process = customizeHLTforTrimmedTracking(process)
  
  process.initialStepSeeds.produceComplement = cms.bool(True)
  
  # Take from the complement some of the tracks to use for "PU tracks".
  process.hltPixelTracksForPU = cms.EDProducer( "TrackWithVertexSelector",
    normalizedChi2 = cms.double( 999999.0 ),
    numberOfValidHits = cms.uint32( 0 ),
    zetaVtx = cms.double( 9999999.0 ),
    rhoVtx = cms.double( 9999999.0 ),
    ptErrorCut = cms.double( 100.0 ),
    dzMax = cms.double( 999.0 ),
    etaMin = cms.double( 0.0 ),
    etaMax = cms.double( 5.0 ),
    quality = cms.string( "" ), ##loose, tight, highPurity # quality isn't working removes everything
    copyTrajectories = cms.untracked.bool( False ),
    nSigmaDtVertex = cms.double( 0.0 ),
    timesTag = cms.InputTag( "" ),
    ptMin = cms.double( 0.5 ), # minimum pT cut 
    ptMax = cms.double( 5.0 ), # maximum pT cut // results not super sensitive to that could keep even higher
    d0Max = cms.double( 999.0 ),
    copyExtras = cms.untracked.bool( False ),
    nVertices = cms.uint32( 0 ),
    vertexTag = cms.InputTag( "hltTrimmedPixelVertices" ),
    src = cms.InputTag( "initialStepSeeds" ), # the complement reco::TrackCollection
    vtxFallback = cms.bool( False ),
    numberOfLostHits = cms.uint32( 999 ),
    numberOfValidPixelHits = cms.uint32( 4 ), # using only quadraplets 
    timeResosTag = cms.InputTag( "" ),
    useVtx = cms.bool( True ) ## Turning off vertex selection
  )
  
  process.initialStepSequence.insert(process.initialStepSequence.index(process.initialStepSeeds)+1, process.hltPixelTracksForPU)
  
  # Making the mixed tracks that are going to feed all the subsequent steps
  process.mixedGeneralTracks  = cms.EDProducer( "TrackListMerger",
      ShareFrac = cms.double( 0.19 ),
      FoundHitBonus = cms.double( 5.0 ),
      LostHitPenalty = cms.double( 20.0 ),
      MinPT = cms.double( 0.05 ),
      Epsilon = cms.double( -0.001 ),
      MaxNormalizedChisq = cms.double( 1000.0 ),
      MinFound = cms.int32( 3 ),
      TrackProducers = cms.VInputTag( 'hltPixelTracksForPU','generalTracks' ),
      hasSelector = cms.vint32( 0, 0),
      indivShareFrac = cms.vdouble( 1.0, 1.0),
      selectedTrackQuals = cms.VInputTag( 'hltPixelTracksForPU','generalTracks' ),
      setsToMerge = cms.VPSet(
        cms.PSet(  pQual = cms.bool( False ),
          tLists = cms.vint32( 0, 1)
        )
      ),
      trackAlgoPriorityOrder = cms.string( "hltESPTrackAlgoPriorityOrder" ),
      allowFirstHitShare = cms.bool( True ),
      newQuality = cms.string( "confirmed" ),
      copyExtras = cms.untracked.bool( True ),
      writeOnlyTrkQuals = cms.bool( False ),
      copyMVA = cms.bool( False )
  )

  process.HLTTrackingV61Sequence.insert(process.HLTTrackingV61Sequence.index(process.generalTracks)+1, process.mixedGeneralTracks)
  
  '''
  Need to update the Offline vertices to also use this "mixed" collection. The reason is we need the vertex fit to be executed with the full collection.
  In this way the PUPPI algorithm can find which tracks were coming from the PV fits and which not , to then fallback to dz.
  More optional : remove those extra pixel tracks - in case you don't want to change the vertices (needs a change in CMSSW producer):
  Remove tracks without valid strip hits from vertices, such that these extra pixel tracks don't affect the vertices.
  '''
  process.unsortedOfflinePrimaryVertices.TrackLabel = cms.InputTag("mixedGeneralTracks")
  process.unsortedOfflinePrimaryVertices.TkFilterParameters.minValidStripHits = cms.int32(1)


  process.trackWithVertexRefSelectorBeforeSorting = process.trackWithVertexRefSelectorBeforeSorting.clone(
    src = cms.InputTag("mixedGeneralTracks"),
    useVtx = cms.bool(False),
  )


  '''
  Use those tracks in PF and TICL
  '''
  process.pfTrack.TkColList = cms.VInputTag(cms.InputTag("mixedGeneralTracks"))
  process.ticlTrackstersMerge.tracks = cms.InputTag("mixedGeneralTracks")
  
  
  return process
