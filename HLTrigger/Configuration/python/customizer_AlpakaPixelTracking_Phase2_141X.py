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
        +process.siPixelClusterShapeCache
        #+process.siPixelDigis             # not needed when copying digis from sim 
        +process.siPixelRecHitsSoA
        +process.siPixelRecHits
    )

    return process

def customizeHLTforAlpakaPixelRecoTracking(process):
    '''Customisation to introduce the Pixel-Track Reconstruction in Alpaka
    '''
    # copied from https://github.com/cms-sw/cmssw/blob/CMSSW_14_1_X/Geometry/CommonTopologies/interface/SimplePixelTopology.h 
    process.hltPixelTracksSoA = cms.EDProducer('CAHitNtupletAlpakaPhase2@alpaka',
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
            minPt   = cms.double(0.5),
            maxTip  = cms.double(0.3),
            maxZip  = cms.double(12.),
        ),
        # autoselect the alpaka backend
        alpaka = cms.untracked.PSet(
            backend = cms.untracked.string('')
        )
    )
    process.hltPixelTracks = cms.EDProducer("PixelTrackProducerFromSoAAlpakaPhase2",
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        minNumberOfHits = cms.int32(0),
        minQuality = cms.string('loose'),
        pixelRecHitLegacySrc = cms.InputTag("siPixelRecHits"),
        trackSrc = cms.InputTag("hltPixelTracksSoA")
    )
    process.hltPhase2PixelTracksSequence = cms.Sequence(process.hltPixelTracksSoA+process.hltPixelTracks)

    return process

# NOTE: is there a smarter way of implementing the full simplified menu?
from .HLT_75e33.paths.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon_cfi import *
from .HLT_75e33.paths.HLT_TriMu_10_5_5_DZ_FromL1TkMuon_cfi import *
from .HLT_75e33.paths.HLT_IsoMu24_FromL1TkMuon_cfi import *
def customizeHLTforAlpakaPaths(process):
    ''' redefine paths including tracking sequences
    '''
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon = cms.Path(HLTBeginSequence+hltL1TkDoubleMuFiltered7+hltL1TkSingleMuFiltered15+hltDoubleMuon7DZ1p0+hltL3fL1DoubleMu155fPreFiltered8+hltL3fL1DoubleMu155fFiltered17+hltDiMuon178RelTrkIsoFiltered0p4+hltDiMuon178RelTrkIsoFiltered0p4DzFiltered0p2+HLTEndSequence, cms.ConditionalTask(MeasurementTrackerEvent, hltCsc2DRecHits, hltCscSegments, hltDt1DRecHits, hltDt4DSegments, hltGemRecHits, hltGemSegments, hltIter0Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter0Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks, hltIter0Phase2L3FromL1TkMuonTrackCutClassifier, hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltIter2Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter2Phase2L3FromL1TkMuonClustersRefRemoval, hltIter2Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter2Phase2L3FromL1TkMuonMaskedMeasurementTrackerEvent, hltIter2Phase2L3FromL1TkMuonMerged, hltIter2Phase2L3FromL1TkMuonPixelClusterCheck, hltIter2Phase2L3FromL1TkMuonPixelHitDoublets, hltIter2Phase2L3FromL1TkMuonPixelHitTriplets, hltIter2Phase2L3FromL1TkMuonPixelLayerTriplets, hltIter2Phase2L3FromL1TkMuonPixelSeeds, hltIter2Phase2L3FromL1TkMuonPixelSeedsFiltered, hltIter2Phase2L3FromL1TkMuonTrackCutClassifier, hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltL2MuonSeedsFromL1TkMuon, hltL2MuonsFromL1TkMuon, hltL2OfflineMuonSeeds, hltPhase2L3FromL1TkMuonPixelLayerQuadruplets, hltPhase2L3FromL1TkMuonPixelTracks, hltPhase2L3FromL1TkMuonPixelTracksHitDoublets, hltPhase2L3FromL1TkMuonPixelTracksHitQuadruplets, hltPhase2L3FromL1TkMuonPixelTracksTrackingRegions, hltPhase2L3FromL1TkMuonPixelVertices, hltPhase2L3FromL1TkMuonTrimmedPixelVertices, hltPhase2L3GlbMuon, hltPhase2L3MuonCandidates, hltPhase2L3MuonGeneralTracks, hltPhase2L3MuonHighPtTripletStepClusters, hltPhase2L3MuonHighPtTripletStepHitDoublets, hltPhase2L3MuonHighPtTripletStepHitTriplets, hltPhase2L3MuonHighPtTripletStepSeedLayers, hltPhase2L3MuonHighPtTripletStepSeeds, hltPhase2L3MuonHighPtTripletStepTrackCandidates, hltPhase2L3MuonHighPtTripletStepTrackCutClassifier, hltPhase2L3MuonHighPtTripletStepTrackingRegions, hltPhase2L3MuonHighPtTripletStepTracks, hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity, hltPhase2L3MuonInitialStepSeeds, hltPhase2L3MuonInitialStepTrackCandidates, hltPhase2L3MuonInitialStepTrackCutClassifier, hltPhase2L3MuonInitialStepTracks, hltPhase2L3MuonInitialStepTracksSelectionHighPurity, hltPhase2L3MuonMerged, hltPhase2L3MuonPixelTracks, hltPhase2L3MuonPixelTracksHitDoublets, hltPhase2L3MuonPixelTracksHitQuadruplets, hltPhase2L3MuonPixelTracksSeedLayers, hltPhase2L3MuonPixelTracksTrackingRegions, hltPhase2L3MuonPixelVertices, hltPhase2L3Muons, hltPhase2L3MuonsNoID, hltPhase2L3MuonsTrkIsoRegionalNewdR0p3dRVeto0p005dz0p25dr0p20ChisqInfPtMin0p0Cut0p4, hltPhase2L3OIMuCtfWithMaterialTracks, hltPhase2L3OIMuonTrackCutClassifier, hltPhase2L3OIMuonTrackSelectionHighPurity, hltPhase2L3OISeedsFromL2Muons, hltPhase2L3OITrackCandidates, hltPhase2PixelFitterByHelixProjections, hltPhase2PixelTrackFilterByKinematics, hltRpcRecHits, process.hltOnlineBeamSpotDevice, process.siPhase2Clusters, process.siPixelClusterShapeCache, process.siPixelClustersSoA, process.siPixelClusters, process.siPixelRecHitsSoA, process.siPixelRecHits, trackerClusterCheck))
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon = cms.Path(HLTBeginSequence+hltTripleMuon3DZ1p0+hltTripleMuon3DR0+hltL3fL1TkTripleMu533PreFiltered555+hltL3fL1TkTripleMu533L3Filtered1055+hltL3fL1TkTripleMu533L31055DZFiltered0p2+HLTEndSequence, cms.ConditionalTask(MeasurementTrackerEvent, hltCsc2DRecHits, hltCscSegments, hltDt1DRecHits, hltDt4DSegments, hltGemRecHits, hltGemSegments, hltIter0Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter0Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks, hltIter0Phase2L3FromL1TkMuonTrackCutClassifier, hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltIter2Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter2Phase2L3FromL1TkMuonClustersRefRemoval, hltIter2Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter2Phase2L3FromL1TkMuonMaskedMeasurementTrackerEvent, hltIter2Phase2L3FromL1TkMuonMerged, hltIter2Phase2L3FromL1TkMuonPixelClusterCheck, hltIter2Phase2L3FromL1TkMuonPixelHitDoublets, hltIter2Phase2L3FromL1TkMuonPixelHitTriplets, hltIter2Phase2L3FromL1TkMuonPixelLayerTriplets, hltIter2Phase2L3FromL1TkMuonPixelSeeds, hltIter2Phase2L3FromL1TkMuonPixelSeedsFiltered, hltIter2Phase2L3FromL1TkMuonTrackCutClassifier, hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltL2MuonSeedsFromL1TkMuon, hltL2MuonsFromL1TkMuon, hltL2OfflineMuonSeeds, hltPhase2L3FromL1TkMuonPixelLayerQuadruplets, hltPhase2L3FromL1TkMuonPixelTracks, hltPhase2L3FromL1TkMuonPixelTracksHitDoublets, hltPhase2L3FromL1TkMuonPixelTracksHitQuadruplets, hltPhase2L3FromL1TkMuonPixelTracksTrackingRegions, hltPhase2L3FromL1TkMuonPixelVertices, hltPhase2L3FromL1TkMuonTrimmedPixelVertices, hltPhase2L3GlbMuon, hltPhase2L3MuonCandidates, hltPhase2L3MuonMerged, hltPhase2L3Muons, hltPhase2L3MuonsNoID, hltPhase2L3OIMuCtfWithMaterialTracks, hltPhase2L3OIMuonTrackCutClassifier, hltPhase2L3OIMuonTrackSelectionHighPurity, hltPhase2L3OISeedsFromL2Muons, hltPhase2L3OITrackCandidates, hltPhase2PixelFitterByHelixProjections, hltPhase2PixelTrackFilterByKinematics, hltRpcRecHits, process.hltOnlineBeamSpotDevice, process.siPhase2Clusters, process.siPixelClusterShapeCache, process.siPixelClustersSoA, process.siPixelClusters, process.siPixelRecHitsSoA, process.siPixelRecHits))
    process.HLT_IsoMu24_FromL1TkMuon = cms.Path(HLTBeginSequence+hltL3fL1TkSingleMu22L3Filtered24Q+hltL3crIsoL1TkSingleMu22L3f24QL3pfecalIsoFiltered0p41+hltL3crIsoL1TkSingleMu22L3f24QL3pfhcalIsoFiltered0p40+hltL3crIsoL1TkSingleMu22L3f24QL3pfhgcalIsoFiltered4p70+hltL3crIsoL1TkSingleMu22L3f24QL3trkIsoRegionalNewFiltered0p07EcalHcalHgcalTrk+itLocalRecoSequence+HLTEndSequence, cms.ConditionalTask(HGCalRecHit, HGCalUncalibRecHit, MeasurementTrackerEvent, bunchSpacingProducer, ecalMultiFitUncalibRecHit, hgcalDigis, hgcalLayerClustersEE, hgcalLayerClustersHSci, hgcalLayerClustersHSi, hgcalMergeLayerClusters, hltCsc2DRecHits, hltCscSegments, hltDt1DRecHits, hltDt4DSegments, hltEcalDetIdToBeRecovered, hltEcalDigis, hltEcalRecHit, hltEcalUncalibRecHit, hltFixedGridRhoFastjetAllCaloForEGamma, hltGemRecHits, hltGemSegments, hltHbhereco, hltHcalDigis, hltIter0Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter0Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter0Phase2L3FromL1TkMuonPixelSeedsFromPixelTracks, hltIter0Phase2L3FromL1TkMuonTrackCutClassifier, hltIter0Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltIter2Phase2L3FromL1TkMuonCkfTrackCandidates, hltIter2Phase2L3FromL1TkMuonClustersRefRemoval, hltIter2Phase2L3FromL1TkMuonCtfWithMaterialTracks, hltIter2Phase2L3FromL1TkMuonMaskedMeasurementTrackerEvent, hltIter2Phase2L3FromL1TkMuonMerged, hltIter2Phase2L3FromL1TkMuonPixelClusterCheck, hltIter2Phase2L3FromL1TkMuonPixelHitDoublets, hltIter2Phase2L3FromL1TkMuonPixelHitTriplets, hltIter2Phase2L3FromL1TkMuonPixelLayerTriplets, hltIter2Phase2L3FromL1TkMuonPixelSeeds, hltIter2Phase2L3FromL1TkMuonPixelSeedsFiltered, hltIter2Phase2L3FromL1TkMuonTrackCutClassifier, hltIter2Phase2L3FromL1TkMuonTrackSelectionHighPurity, hltL2MuonSeedsFromL1TkMuon, hltL2MuonsFromL1TkMuon, hltL2OfflineMuonSeeds, hltParticleFlowClusterECALUncorrectedUnseeded, hltParticleFlowClusterECALUnseeded, hltParticleFlowClusterHBHE, hltParticleFlowClusterHCAL, hltParticleFlowRecHitECALUnseeded, hltParticleFlowRecHitHBHE, hltPhase2L3FromL1TkMuonPixelLayerQuadruplets, hltPhase2L3FromL1TkMuonPixelTracks, hltPhase2L3FromL1TkMuonPixelTracksHitDoublets, hltPhase2L3FromL1TkMuonPixelTracksHitQuadruplets, hltPhase2L3FromL1TkMuonPixelTracksTrackingRegions, hltPhase2L3FromL1TkMuonPixelVertices, hltPhase2L3FromL1TkMuonTrimmedPixelVertices, hltPhase2L3GlbMuon, hltPhase2L3MuonCandidates, hltPhase2L3MuonGeneralTracks, hltPhase2L3MuonHighPtTripletStepClusters, hltPhase2L3MuonHighPtTripletStepHitDoublets, hltPhase2L3MuonHighPtTripletStepHitTriplets, hltPhase2L3MuonHighPtTripletStepSeedLayers, hltPhase2L3MuonHighPtTripletStepSeeds, hltPhase2L3MuonHighPtTripletStepTrackCandidates, hltPhase2L3MuonHighPtTripletStepTrackCutClassifier, hltPhase2L3MuonHighPtTripletStepTrackingRegions, hltPhase2L3MuonHighPtTripletStepTracks, hltPhase2L3MuonHighPtTripletStepTracksSelectionHighPurity, hltPhase2L3MuonInitialStepSeeds, hltPhase2L3MuonInitialStepTrackCandidates, hltPhase2L3MuonInitialStepTrackCutClassifier, hltPhase2L3MuonInitialStepTracks, hltPhase2L3MuonInitialStepTracksSelectionHighPurity, hltPhase2L3MuonMerged, hltPhase2L3MuonPixelTracks, hltPhase2L3MuonPixelTracksHitDoublets, hltPhase2L3MuonPixelTracksHitQuadruplets, hltPhase2L3MuonPixelTracksSeedLayers, hltPhase2L3MuonPixelTracksTrackingRegions, hltPhase2L3MuonPixelVertices, hltPhase2L3Muons, hltPhase2L3MuonsEcalIsodR0p3dRVeto0p000, hltPhase2L3MuonsHcalIsodR0p3dRVeto0p000, hltPhase2L3MuonsHgcalLCIsodR0p2dRVetoEM0p00dRVetoHad0p02minEEM0p00minEHad0p00, hltPhase2L3MuonsNoID, hltPhase2L3MuonsTrkIsoRegionalNewdR0p3dRVeto0p005dz0p25dr0p20ChisqInfPtMin0p0Cut0p07, hltPhase2L3OIMuCtfWithMaterialTracks, hltPhase2L3OIMuonTrackCutClassifier, hltPhase2L3OIMuonTrackSelectionHighPurity, hltPhase2L3OISeedsFromL2Muons, hltPhase2L3OITrackCandidates, hltPhase2PixelFitterByHelixProjections, hltPhase2PixelTrackFilterByKinematics, hltRpcRecHits, process.hltOnlineBeamSpotDevice, process.siPhase2Clusters, process.siPixelClusterShapeCache, process.siPixelClustersSoA, process.siPixelClusters, process.siPixelRecHitsSoA, process.siPixelRecHits, trackerClusterCheck))

    return process

def customizeHLTforAlpakaTrackingOnly(process):
    process.HLT_TrackingOnly = cms.Path(process.HLTBeginSequence+process.itLocalRecoSequence+process.hltPhase2PixelTracksSequence+process.HLTEndSequence)
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
    #process = customizeHLTforAlpakaPaths(process)  # not working yet
    process = customizeHLTforAlpakaTrackingOnly(process)
    return process