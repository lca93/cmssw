import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelClustersSoA = cms.EDProducer('SiPixelRawToClusterPhase2@alpaka',
    mightGet = cms.optional.untracked.vstring,
    IncludeErrors = cms.bool(True),
    UseQualityInfo = cms.bool(False),
    clusterThreshold_layer1 = cms.int32(4000),
    clusterThreshold_otherLayers = cms.int32(4000),
    VCaltoElectronGain      = cms.double(1),  # all gains=1, pedestals=0
    VCaltoElectronGain_L1   = cms.double(1),
    VCaltoElectronOffset    = cms.double(0),
    VCaltoElectronOffset_L1 = cms.double(0),
    InputLabel = cms.InputTag('rawDataCollector'),
    Regions = cms.PSet(
        inputs = cms.optional.VInputTag,
        deltaPhi = cms.optional.vdouble,
        maxZ = cms.optional.vdouble,
        beamSpot = cms.optional.InputTag
    ),
    CablingMapLabel = cms.string(''),
    # autoselect the alpaka backend
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string('')
    )
)