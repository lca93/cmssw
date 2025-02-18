#ifndef Geometry_HGCalCommonData_HGCalCellOffset_h
#define Geometry_HGCalCommonData_HGCalCellOffset_h

#include <cmath>
#include <cstdint>
#include <array>
#include <memory>
#include "Geometry/HGCalCommonData/interface/HGCalCell.h"

class HGCalCellOffset {
public:
  HGCalCellOffset(double waferSize,
                  int32_t nFine,
                  int32_t nCoarse,
                  double guardRingOffset_,
                  double mouseBiteCut_,
                  double sizeOffset_);

  std::pair<double, double> cellOffsetUV2XY1(int32_t u, int32_t v, int32_t placementIndex, int32_t type);
  std::pair<double, double> cellOffsetUV2XY1(
      int32_t u, int32_t v, int32_t placementIndex, int32_t type, int32_t partialType);
  double cellAreaUV(int32_t u, int32_t v, int32_t placementIndex, int32_t type, bool reco);
  double cellAreaUV(int32_t u, int32_t v, int32_t placementIndex, int32_t type, int32_t partialType, bool reco);

private:
  const double sqrt3_ = std::sqrt(3.0);
  const double sqrt3By2_ = (0.5 * sqrt3_);
  std::array<std::array<std::array<double, 6>, 6>, 2> offsetX, offsetY;
  std::array<std::array<std::array<double, 6>, 25>, 2> offsetPartialX, offsetPartialY;
  int32_t ncell_[2];
  double cellX_[2], cellY_[2], fullArea[2], cellArea[2][6], cellAreaPartial[2][25];
  std::unique_ptr<HGCalCell> hgcalcell_;
};

#endif
