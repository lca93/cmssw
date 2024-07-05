# adapted from  https://github.com/cms-sw/cmssw/blob/CMSSW_14_0_0/HLTrigger/Configuration/python/customizeHLTforAlpaka.py#L579
import FWCore.ParameterSet.Config as cms
from HeterogeneousCore.AlpakaCore.functions import *

def customizeHLTforAlpakaPixelRecoLocal(process):
    '''Customisation to introduce the Local Pixel Reconstruction in Alpaka.
    The "FromAlpaka" label is appended to the new collections to avoid conflicts in the simplified menu
    '''
    process.hltESPSiPixelCablingSoA = cms.ESProducer('SiPixelCablingSoAESProducer@alpaka', 
            CablingMapLabel = cms.string(''),
            UseQualityInfo = cms.bool(False),
            appendToDataLabel = cms.string(''),
            alpaka = cms.untracked.PSet(
                backend = cms.untracked.string('')
        )
    )
    process.hltESPSiPixelGainCalibrationForHLTSoA = cms.ESProducer('SiPixelGainCalibrationForHLTSoAESProducer@alpaka',
            appendToDataLabel = cms.string(''),
            alpaka = cms.untracked.PSet(
                backend = cms.untracked.string('')
        )
    )
    process.hltESPPixelCPEFastParamsPhase2 = cms.ESProducer('PixelCPEFastParamsESProducerAlpakaPhase2@alpaka', 
            ComponentName = cms.string("PixelCPEFastParamsPhase2"),
            appendToDataLabel = cms.string(''),
            alpaka = cms.untracked.PSet(
                backend = cms.untracked.string('')
        )
    )
    process.hltOnlineBeamSpotDevice = cms.EDProducer('BeamSpotDeviceProducer@alpaka',
            src = cms.InputTag('hltOnlineBeamSpot'),
            alpaka = cms.untracked.PSet(
                backend = cms.untracked.string('')
        )
    )
    process.siPixelClustersSoA = cms.EDProducer('SiPixelPhase2DigiToCluster@alpaka',
        mightGet = cms.optional.untracked.vstring,
        alpaka = cms.untracked.PSet(
            backend = cms.untracked.string('')
        )
    )
    process.siPixelClustersFromAlpaka = cms.EDProducer('SiPixelDigisClustersFromSoAAlpakaPhase2',
        src = cms.InputTag('siPixelClustersSoA'),
        clusterThreshold_layer1 = cms.int32(4000),
        clusterThreshold_otherLayers = cms.int32(4000),
        produceDigis = cms.bool(False),
        storeDigis = cms.bool(False)
    )
    process.siPixelClusterShapeCacheFromAlpaka = cms.EDProducer('SiPixelClusterShapeCacheProducer',
        src = cms.InputTag('siPixelClustersSoA' ),
        onDemand = cms.bool( False )
    )
    process.siPixelRecHitsSoA = cms.EDProducer('SiPixelRecHitAlpakaPhase2@alpaka',
        beamSpot = cms.InputTag('hltOnlineBeamSpotDevice'),
        src = cms.InputTag('siPixelClustersSoA'),
        CPE = cms.string('PixelCPEFastParamsPhase2'),
        mightGet = cms.optional.untracked.vstring,
        # autoselect the alpaka backend
        alpaka = cms.untracked.PSet(
            backend = cms.untracked.string('')
        )
    )
    process.siPixelRecHitsFromAlpaka = cms.EDProducer('SiPixelRecHitFromSoAAlpakaPhase2',
        pixelRecHitSrc = cms.InputTag('siPixelRecHitsSoA'),
        src = cms.InputTag('siPixelClustersFromAlpaka'),
    )
    process.itLocalRecoSequenceFromAlpaka = cms.Sequence(process.hltOnlineBeamSpotDevice
        +process.siPhase2Clusters
        +process.siPixelClustersSoA
        +process.siPixelClustersFromAlpaka
        #+process.siPixelClusterShapeCache  # disable for tracking only but more attention is needed for the full simplified menu
        #+process.siPixelDigis              # not needed when copying digis from sim
        +process.siPixelRecHitsSoA
        +process.siPixelRecHitsFromAlpaka
    )
    # some paths redefine this sequence (not used in tracking only configuration)
    process.HLTDoLocalPixelSequenceFromAlpaka = cms.Sequence(process.hltOnlineBeamSpotDevice
        +process.siPhase2Clusters
        +process.siPixelClustersSoA
        +process.siPixelClustersFromAlpaka
        #+process.siPixelClusterShapeCache
        #+process.siPixelDigis             # not needed when copying digis from sim 
        +process.siPixelRecHitsSoA
        +process.siPixelRecHitsFromAlpaka
    )

    return process

def customizeHLTforAlpakaPixelRecoTracking(process):
    '''Customisation to introduce the Pixel-Track Reconstruction in Alpaka
    '''
    # copied from https://github.com/cms-sw/cmssw/blob/CMSSW_14_1_X/Geometry/CommonTopologies/interface/SimplePixelTopology.h
    process.hltPhase2PixelTracksSoA = cms.EDProducer('CAHitNtupletAlpakaPhase2@alpaka',
        pixelRecHitSrc = cms.InputTag('siPixelRecHitsSoA'),
        CPE = cms.string('PixelCPEFastParamsPhase2'),
        ptmin = cms.double(0.9),
        CAThetaCutBarrel = cms.double(0.002),
        CAThetaCutForward = cms.double(0.003),
        hardCurvCut = cms.double(0.0328407225),
        dcaCutInnerTriplet = cms.double(0.15),
        dcaCutOuterTriplet = cms.double(0.25),
        earlyFishbone = cms.bool(True),
        lateFishbone = cms.bool(False),
        fillStatistics = cms.bool(False),
        minHitsPerNtuplet = cms.uint32(3),
        phiCuts = cms.vint32(
            522, 522, 522, 626, 730, 730, 626, 730, 730, 522, 522,
            522, 522, 522, 522, 522, 522, 522, 522, 522, 522, 522,
            522, 522, 522, 522, 522, 522, 522, 730, 730, 730, 730,
            730, 730, 730, 730, 730, 730, 730, 730, 730, 730, 730,
            730, 730, 730, 522, 522, 522, 522, 522, 522, 522, 522
        ),
        maxNumberOfDoublets = cms.uint32(5*512*1024),
        minHitsForSharingCut = cms.uint32(10),
        fitNas4 = cms.bool(False),
        doClusterCut = cms.bool(True),
        doZ0Cut = cms.bool(True),
        doPtCut = cms.bool(True),
        useRiemannFit = cms.bool(False),
        doSharedHitCut = cms.bool(True),
        dupPassThrough = cms.bool(False),
        useSimpleTripletCleaner = cms.bool(True),
        idealConditions = cms.bool(False),
        includeJumpingForwardDoublets = cms.bool(True),
        trackQualityCuts = cms.PSet(
            # phase1 quality cuts not implemented for phase2
            # https://github.com/cms-sw/cmssw/blob/CMSSW_14_1_X/RecoTracker/PixelSeeding/plugins/CAHitNtupletGeneratorOnGPU.cc#L253-L257
            #chi2MaxPt = cms.double(10),
            #chi2Coeff = cms.vdouble(0.9, 1.8),
            #chi2Scale = cms.double(8),
            #tripletMinPt = cms.double(0.5),
            #tripletMaxTip = cms.double(0.3),
            #tripletMaxZip = cms.double(12),
            #quadrupletMinPt = cms.double(0.3),
            #quadrupletMaxTip = cms.double(0.5),
            #quadrupletMaxZip = cms.double(12)
            maxChi2 = cms.double(5.0),
            minPt   = cms.double(0.9),
            maxTip  = cms.double(0.3),
            maxZip  = cms.double(12.),
        ),
        # autoselect the alpaka backend
        alpaka = cms.untracked.PSet(
            backend = cms.untracked.string('')
        )
    )
    process.hltPhase2PixelTracksFromAlpaka = cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase2",
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        minNumberOfHits = cms.int32(0),
        minQuality = cms.string('loose'),
        pixelRecHitLegacySrc = cms.InputTag("siPixelRecHitsFromAlpaka"),
        trackSrc = cms.InputTag("hltPhase2PixelTracksSoA")
    )
    process.hltPhase2PixelTracksSequenceFromAlpaka = cms.Sequence(process.hltPhase2PixelTracksSoA+process.hltPhase2PixelTracksFromAlpaka)

    return process

def customizeHLTforAlpakaFullTrackingSingleIteration(process):
    # original cfg at hand as in 14_1_0_pre4 simplified menu 
    # https://lguzzi.web.cern.ch/lguzzi/Tracking/Phase2/hlt-dump_simplifiedMenu_14_1_0_pre4.txt
    ''' track building seeded by hltPhase2PixelTracks, possibly from patatrack
    (copied from initialStep).
    The "FromAlpaka" label is appended to the new collections to avoid conflicts in the simplified menu
    '''
    process.hltPhase2PixelVerticesFromAlpaka = process.hltPhase2PixelVertices.clone()
    process.hltPhase2PixelVerticesFromAlpaka.TrackCollection = cms.InputTag("hltPhase2PixelTracksFromAlpaka")

    process.MeasurementTrackerEventFromAlpaka = process.MeasurementTrackerEvent.clone()
    process.MeasurementTrackerEventFromAlpaka.pixelClusterProducer = cms.string('siPixelClustersFromAlpaka')

    process.initialStepSeedsFromAlpaka = process.initialStepSeeds.clone()
    process.initialStepSeedsFromAlpaka.InputCollection = cms.InputTag("hltPhase2PixelTracksFromAlpaka")

    process.initialStepTrackCandidatesFromAlpaka = process.initialStepTrackCandidates.clone()
    process.initialStepTrackCandidatesFromAlpaka.MeasurementTrackerEvent    = cms.InputTag("MeasurementTrackerEventFromAlpaka")
    process.initialStepTrackCandidatesFromAlpaka.src                        = cms.InputTag("initialStepSeedsFromAlpaka")

    process.initialStepTracksFromAlpaka = process.initialStepTracks.clone()
    process.initialStepTracksFromAlpaka.MeasurementTrackerEvent = cms.InputTag("MeasurementTrackerEventFromAlpaka")
    process.initialStepTracksFromAlpaka.AlgorithmName           = cms.string('initialStepFromAlpaka')
    process.initialStepTracksFromAlpaka.src                     = cms.InputTag("initialStepTrackCandidatesFromAlpaka")

    process.initialStepTrackCutClassifierFromAlpaka = process.initialStepTrackCutClassifier.clone()
    process.initialStepTrackCutClassifierFromAlpaka.src         = cms.InputTag("initialStepTracksFromAlpaka")
    process.initialStepTrackCutClassifierFromAlpaka.vertices    = cms.InputTag("hltPhase2PixelVerticesFromAlpaka")

    process.generalTracksFromAlpaka = process.initialStepTrackSelectionHighPurity.clone()
    process.generalTracksFromAlpaka.originalMVAVals     = cms.InputTag("initialStepTrackCutClassifierFromAlpaka","MVAValues")
    process.generalTracksFromAlpaka.originalQualVals    = cms.InputTag("initialStepTrackCutClassifierFromAlpaka","QualityMasks")
    process.generalTracksFromAlpaka.originalSource      = cms.InputTag("initialStepTracksFromAlpaka")

    process.hltPhase2TrackingSingleIterFromAlpaka = cms.Sequence(
         process.hltPhase2PixelVerticesFromAlpaka
        +process.MeasurementTrackerEventFromAlpaka
        +process.initialStepSeedsFromAlpaka
        +process.initialStepTrackCandidatesFromAlpaka
        +process.initialStepTracksFromAlpaka
        +process.initialStepTrackCutClassifierFromAlpaka
        +process.generalTracksFromAlpaka
    )

    return process

def customizeHLTforAlpakaTrackingOnly(process):
    ''' Create a tracking-only sequence to test the configuration.
    '''
    process.HLT_TrackingOnly = cms.Path()
    process.HLT_TrackingOnly.insert(item=process.HLTBeginSequence                       , index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.itLocalRecoSequenceFromAlpaka          , index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.hltPhase2PixelTracksSequenceFromAlpaka , index=len(process.HLT_TrackingOnly.moduleNames()))
    if hasattr(process, 'hltPhase2TrackingSingleIterFromAlpaka'):
        process.HLT_TrackingOnly.insert(item=process.hltPhase2TrackingSingleIterFromAlpaka, index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.HLTEndSequence                         , index=len(process.HLT_TrackingOnly.moduleNames()))

    process.FEVTDEBUGHLTEventContent.outputCommands.append('keep *_*FromAlpaka_*_reHLT')
    process.outputmodule = cms.EndPath(process.FEVTDEBUGHLToutput)
    process.schedule = cms.Schedule(*[
        process.HLT_TrackingOnly,
        process.endjob_step,
        process.outputmodule
    ])
    
    return process

def customizeHLTforAlpaka(process):
    process.load("HeterogeneousCore.AlpakaCore.ProcessAcceleratorAlpaka_cfi")
    process.load('Configuration.StandardSequences.Accelerators_cff')
    process = customizeHLTforAlpakaPixelRecoLocal(process)
    process = customizeHLTforAlpakaPixelRecoTracking(process)
    process = customizeHLTforAlpakaFullTrackingSingleIteration(process)
    process = customizeHLTforAlpakaTrackingOnly(process)
    return process