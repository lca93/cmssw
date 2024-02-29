import FWCore.ParameterSet.Config as cms

hltPixelTracksSoA = cms.EDProducer('CAHitNtupletAlpakaPhase2@alpaka',
    pixelRecHitSrc = cms.InputTag('hltSiPixelRecHitsSoA'),
    CPE = cms.string('PixelCPEFastParams'),
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
        522, 730, 730, 522, 626,
        626, 522, 522, 626, 626,
        626, 522, 522, 522, 522,
        522, 522, 522, 522
    ),
    maxNumberOfDoublets = cms.uint32(524288),
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
        chi2MaxPt = cms.double(10),
        chi2Coeff = cms.vdouble(0.9, 1.8),
        chi2Scale = cms.double(8),
        tripletMinPt = cms.double(0.5),
        tripletMaxTip = cms.double(0.3),
        tripletMaxZip = cms.double(12),
        quadrupletMinPt = cms.double(0.3),
        quadrupletMaxTip = cms.double(0.5),
        quadrupletMaxZip = cms.double(12)
    ),
    # autoselect the alpaka backend
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    )
)