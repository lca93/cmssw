#ifndef DataFormats_SiPixelDigiSoA_interface_alpaka_SiPixelDigisSoACollection_h
#define DataFormats_SiPixelDigiSoA_interface_alpaka_SiPixelDigisSoACollection_h

#include <cstdint>

#include <alpaka/alpaka.hpp>

#include "DataFormats/Portable/interface/alpaka/PortableCollection.h"
#include "DataFormats/SiPixelDigiSoA/interface/SiPixelDigisDevice.h"
#include "DataFormats/SiPixelDigiSoA/interface/SiPixelDigisHost.h"
#include "HeterogeneousCore/AlpakaInterface/interface/CopyToHost.h"
#include "HeterogeneousCore/AlpakaInterface/interface/config.h"

namespace ALPAKA_ACCELERATOR_NAMESPACE {

  using SiPixelDigisSoACollection =
      std::conditional_t<std::is_same_v<Device, alpaka::DevCpu>, SiPixelDigisHost, SiPixelDigisDevice<Device>>;

}  // namespace ALPAKA_ACCELERATOR_NAMESPACE

namespace cms::alpakatools {
  template <typename TDevice>
  struct CopyToHost<SiPixelDigisDevice<TDevice>> {
    template <typename TQueue>
    static auto copyAsync(TQueue &queue, SiPixelDigisDevice<TDevice> const &srcData) {

      printf("METADATA: %d NDIGIS: %d DIFF: %d\n",srcData.view().metadata().size(),srcData.nDigis(),srcData.view().metadata().size()-srcData.nDigis());
      
      SiPixelDigisHost dstData(srcData.nDigis(), queue);
      
      alpaka::memcpy(queue, dstData.buffer(), srcData.buffer());
      dstData.setNModulesDigis(srcData.nModules(), srcData.nDigis());

      auto digi_view = dstData.view();
      for(int i = 0; i<srcData.view().metadata().size();i++)
          printf("Host: %d %d %d %d %d \n",i,digi_view[i].rawIdArr(),digi_view[i].clus(),digi_view[i].pdigi(),digi_view[i].adc());

      alpaka::wait(queue);
      return dstData;
    }
  };
}  // namespace cms::alpakatools

ASSERT_DEVICE_MATCHES_HOST_COLLECTION(SiPixelDigisSoACollection, SiPixelDigisHost);

#endif  // DataFormats_SiPixelDigiSoA_interface_alpaka_SiPixelDigisSoACollection_h
