#ifndef CondTools_DQM_DQMSummaryReader_h
#define CondTools_DQM_DQMSummaryReader_h

#include "CondFormats/DQMObjects/interface/DQMSummary.h"
#include "CondTools/DQM/interface/TestBase.h"

class DQMSummaryReader : virtual public TestBase {
public:
  DQMSummaryReader(const std::string& connectionString, const std::string& user, const std::string& pass);
  ~DQMSummaryReader() override;
  void run() override;
  DQMSummary readData(const std::string& table, /*const std::string & column,*/ const long long r_number);

private:
  std::string m_tableToRead;
  //std::string m_columnToRead;
  std::string m_connectionString;
  std::string m_user;
  std::string m_pass;
};

#endif
