import FWCore.ParameterSet.Config as cms

hltPhase2SiPixelDigis = cms.EDProducer('SiPixelDigiErrorsFromSoAAlpaka',
    digiErrorSoASrc = cms.InputTag('hltPhase2SiPixelClustersSoA'),
    fmtErrorsSoASrc = cms.InputTag('hltPhase2SiPixelClustersSoA'),
    CablingMapLabel = cms.string(''),
    UsePhase1 = cms.bool(True),
    ErrorList = cms.vint32(29),
    UserErrorList = cms.vint32(40)
)
