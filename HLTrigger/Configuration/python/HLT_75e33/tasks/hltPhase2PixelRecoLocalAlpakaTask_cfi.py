import FWCore.ParameterSet.Config as cms

from ..modules.hltPhase2ESPSiPixelCablingSoA                    import *
from ..modules.hltPhase2ESPSiPixelGainCalibrationForHLTSoA_cfi  import *
from ..modules.hltPhase2ESPPixelCPEFastParams_cfi               import *
from ..modules.hltPhase2OnlineBeamSpotDevice_cfi                import *
from ..modules.hltPhase2SiPixelClustersSoA_cfi                  import *
from ..modules.hltPhase2SiPixelClusters_cfi                     import *
from ..modules.hltPhase2SiPixelClustersCache_cfi                import *
from ..modules.hltPhase2SiPixelDigis_cfi                        import *
from ..modules.hltPhase2SiPixelRecHitsSoA_cfi                   import *
from ..modules.hltPhase2SiPixelRecHits_cfi                      import *

hltPhase2DoLocalPixelTask = cms.ConditionalTask(
  hltPhase2OnlineBeamSpotDevice,
  hltPhase2SiPixelClustersSoA,
  hltPhase2SiPixelClusters,
  hltPhase2SiPixelClustersCache,
  hltPhase2SiPixelDigis,
  hltPhase2SiPixelRecHitsSoA,
  hltPhase2SiPixelRecHits,
  #hltPhase2ESPSiPixelCablingSoA,
  #hltPhase2ESPSiPixelGainCalibrationForHLTSoA,
  #hltPhase2ESPPixelCPEFastParams,
)