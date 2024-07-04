# adapted from  https://github.com/cms-sw/cmssw/blob/CMSSW_14_0_0/HLTrigger/Configuration/python/customizeHLTforAlpaka.py#L579
import FWCore.ParameterSet.Config as cms
from HeterogeneousCore.AlpakaCore.functions import *

# TODO: implement the standatd simplified menu (ie include physics paths)
# TODO: adopt a better naming scheme (eg. hltPhase2...)

def customizeHLTforAlpakaPixelRecoLocal(process):
    '''Customisation to introduce the Local Pixel Reconstruction in Alpaka
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
    process.siPixelClusters = cms.EDProducer('SiPixelDigisClustersFromSoAAlpakaPhase2',
        src = cms.InputTag('siPixelClustersSoA'),
        clusterThreshold_layer1 = cms.int32(4000),
        clusterThreshold_otherLayers = cms.int32(4000),
        produceDigis = cms.bool(False),
        storeDigis = cms.bool(False)
    )
    process.siPixelClusterShapeCache = cms.EDProducer('SiPixelClusterShapeCacheProducer',
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
    process.siPixelRecHits = cms.EDProducer('SiPixelRecHitFromSoAAlpakaPhase2',
        pixelRecHitSrc = cms.InputTag('siPixelRecHitsSoA'),
        src = cms.InputTag('siPixelClusters'),
    )
    process.itLocalRecoSequence = cms.Sequence(process.hltOnlineBeamSpotDevice
        +process.siPhase2Clusters
        +process.siPixelClustersSoA
        +process.siPixelClusters
        #+process.siPixelClusterShapeCache  # disable for tracking only but more attention is needed for the full simplified menu
        #+process.siPixelDigis              # not needed when copying digis from sim
        +process.siPixelRecHitsSoA
        +process.siPixelRecHits
    )
    # some paths redefine this sequence (not used in tracking only configuration)
    process.HLTDoLocalPixelSequence = cms.Sequence(process.hltOnlineBeamSpotDevice
        +process.siPhase2Clusters
        +process.siPixelClustersSoA
        +process.siPixelClusters
        #+process.siPixelClusterShapeCache
        #+process.siPixelDigis             # not needed when copying digis from sim 
        +process.siPixelRecHitsSoA
        +process.siPixelRecHits
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
    process.hltPhase2PixelTracks = cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase2",
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        minNumberOfHits = cms.int32(0),
        minQuality = cms.string('loose'),
        pixelRecHitLegacySrc = cms.InputTag("siPixelRecHits"),
        trackSrc = cms.InputTag("hltPhase2PixelTracksSoA")
    )
    process.hltPhase2PixelTracksSequence = cms.Sequence(process.hltPhase2PixelTracksSoA+process.hltPhase2PixelTracks)

    return process

def customizeHLTforAlpakaFullTrackingSingleIteration(process):
    ''' track building seeded by hltPhase2PixelTracks, possibly from patatrack
    (copied from initialStep).
    '''
    process.generalTracks = process.initialStepTrackSelectionHighPurity.clone()
    process.hltPhase2TrackingSingleIter = cms.Sequence(process.hltPhase2PixelVertices
        +process.MeasurementTrackerEvent
        +process.initialStepSeeds
        +process.initialStepTrackCandidates
        +process.initialStepTracks
        +process.initialStepTrackCutClassifier
        +process.generalTracks
    )

    return process

def customizeHLTforAlpakaTrackingOnly(process):
    process.HLT_TrackingOnly = cms.Path()
    process.HLT_TrackingOnly.insert(item=process.HLTBeginSequence               , index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.itLocalRecoSequence            , index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.hltPhase2PixelTracksSequence   , index=len(process.HLT_TrackingOnly.moduleNames()))
    if hasattr(process, 'hltPhase2TrackingSingleIter'):
        process.HLT_TrackingOnly.insert(item=process.hltPhase2TrackingSingleIter, index=len(process.HLT_TrackingOnly.moduleNames()))
    process.HLT_TrackingOnly.insert(item=process.HLTEndSequence                 , index=len(process.HLT_TrackingOnly.moduleNames()))

    process.outputmodule = cms.EndPath(*[getattr(process, outmod) for outmod in process.outputModules.keys()])
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
    import pdb; pdb.set_trace()
    return process