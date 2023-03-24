import FWCore.ParameterSet.Config as cms
# validation & dqm modules 
from HLTrigger.Configuration.phase2TrackingValidation_cff import *

def customisePhase2HLTForTrackingOnly(process):
    
    process.TrackMon_gentk  = TrackMon_gentk.clone()
    process.TrackSplitMonitor = TrackSplitMonitor.clone()
    process.TrackerCollisionSelectedTrackMonCommongeneralTracks = TrackerCollisionSelectedTrackMonCommongeneralTracks.clone()
    process.dqmInfoTracking = dqmInfoTracking.clone()
    process.pvMonitor = pvMonitor.clone()

    # Sim Track/Tracking particle associator to clusters
    process.tpClusterProducer = tpClusterProducer.clone()
    # Utility to associate the number of layers to TPs
    process.trackingParticleNumberOfLayersProducer = trackingParticleNumberOfLayersProducer.clone()
    # TP to Track association
    # The associator itself
    process.quickTrackAssociatorByHits = quickTrackAssociatorByHits.clone()
    # The association to pixel tracks
    process.trackingParticlePixelTrackAssociation = trackingParticlePixelTrackAssociation.clone()
    # The association to general track
    process.trackingParticleGeneralTrackAssociation = trackingParticleGeneralTrackAssociation.clone()

    #The validators
    process.trackValidatorPixelTrackingOnly = trackValidatorPixelTrackingOnly.clone()
    process.trackValidatorGeneralTrackingOnly = trackValidatorGeneralTrackingOnly.clone()
    
    #Associating the vertices to the sim PVs
    process.VertexAssociatorByPositionAndTracks = VertexAssociatorByPositionAndTracks.clone()
    # ... and for pixel vertices
    process.VertexAssociatorByPositionAndTracksPixel = VertexAssociatorByPositionAndTracksPixel.clone()

    #The vertex validator
    process.vertexAnalysis = vertexAnalysis.clone()

    #Baseline tracking path
    process.HLTTrackingV61Path = cms.Path(process.HLTTrackingV61Sequence)

    process.RawToDigiTask = cms.Task(process.ecalDigisTask, process.ecalPreshowerDigis, process.hcalDigis, process.hgcalDigis, process.muonCSCDigis, process.muonDTDigis, process.muonGEMDigis)
    process.calolocalrecoTask = cms.Task(process.hcalGlobalRecoTask,process.ecalLocalRecoTask, process.hcalLocalRecoTask)

    process.hrecoTask = cms.Task(process.RawToDigiTask, process.calolocalrecoTask)
    process.localSeq = cms.Sequence(process.hrecoTask) #For the moment no MTD,process.mtdRecoTask)
    process.localPath = cms.Path(process.localSeq)

    process.vertexRecoTask = cms.Task(process.ak4CaloJetsForTrk, process.initialStepPVTask, process.offlinePrimaryVertices, process.trackRefsForJetsBeforeSorting, process.trackWithVertexRefSelectorBeforeSorting, process.unsortedOfflinePrimaryVertices,process.goodOfflinePrimaryVertices)

    process.vertexRecoSeq = cms.Sequence(process.vertexRecoTask) ## No MTD : ,process.vertex4DrecoTask)
    process.vertexRecoPath = cms.Path(process.vertexRecoSeq)

    #DQM
    process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
        dataset = cms.untracked.PSet(
            dataTier = cms.untracked.string('DQMIO'),
            filterName = cms.untracked.string('')
        ),
        fileName = cms.untracked.string('file:Phase2HLT_DQM.root'),
        outputCommands = process.DQMEventContent.outputCommands,
        splitLevel = cms.untracked.int32(0)
    )
    process.DQMoutput_step = cms.EndPath(process.DQMoutput)
    process.dqm = cms.Task(process.pvMonitor, process.TrackSplitMonitor,process.dqmInfoTracking,process.TrackerCollisionSelectedTrackMonCommongeneralTracks,process.TrackMon_gentk)
    process.dqm_step = cms.EndPath(process.dqm)

    #Validation
    process.tracksValidation = cms.Sequence(process.trackValidatorGeneralTrackingOnly + process.trackValidatorPixelTrackingOnly)# + process.vertexAnalysis)
    process.tracksValidationTruth = cms.Task(process.VertexAssociatorByPositionAndTracksPixel,process.VertexAssociatorByPositionAndTracks, process.quickTrackAssociatorByHits, process.tpClusterProducer, process.trackingParticleNumberOfLayersProducer, process.trackingParticleGeneralTrackAssociation,process.trackingParticlePixelTrackAssociation)
    process.validation = cms.Sequence(process.tracksValidation,process.tracksValidationTruth)
    process.validation_step = cms.EndPath(process.validation)
    

    ##Local Reco
    process.localPath = cms.Path(process.RawToDigiTask,process.localrecoTask)

    process.schedule = cms.Schedule(*[
        #process.l1tReconstructionPath,
        process.localPath,
        process.HLTTrackingV61Path,
        process.vertexRecoPath,
        process.validation_step,
        process.dqm_step,
        process.DQMoutput_step
        ],tasks=[process.patAlgosToolsTask])
        
    return process
