from CRABClient.UserUtilities import config as Configuration
from CRABAPI.RawCommand import crabCommand

import os, sys
import json
import argparse
parser = argparse.ArgumentParser('''Submit jobs to skim events for VdM tasks.\n
The script reads time ranges, run ranges and lumisections from LUMI json files. 
The bunch crossings list is provided as an external argument.\n
Each submission should correspond to a single dataset and a single VdM configuration (json file).\n
The crab task is created block-wise to reduce the tape-recall time.\n
The output consists of events falling in the time ranges specified in the json file, 
matching the given bunch crossing numbers.\n
[!] the output is saved in /store/user/$USER/BeamSpot/
''')
parser.add_argument('--input'         , required=True             , help='timestamp file from lumi')
parser.add_argument('--storage'       , default='T3_IT_MIB'       , help='storage site')
parser.add_argument('--dataset'       , required=True             , help='input dataset')
parser.add_argument('--bunchcrossings', required=True             , help='list of bunchcrossings to select', nargs='+')
parser.add_argument('--workarea'      , default='TimeBX_skim'     , help='crab work area')
parser.add_argument('--dryrun'        , action='store_true'       , help='don\'t run CRAB')
parser.add_argument('--streams'       , default=10, type=int      , help='number of streams for fetching the block list')

args = parser.parse_args()

class Scan:
  '''main class for building a scan object from a LUMI POG json file.
  A Scan instance identifies a particular scan effort (eg. diagonal X coordinate).
  '''
  def __init__(self, label, json, number):
    self.label  = os.path.basename(label).strip('.json')
    self.main   = json
    self.index  = number
    self.scan   = self.main['Scans'][self.index]
    self.runn   = self.main['Run'  ][self.index]
    self.points = [Point(scan=self, index=i) for i in range(self.scan['NumPoints'])]
    self.times  = ','.join(p.times  for p in self.points)

class Point:
  ''' class for building a scan point object. 
  A Point instance identifies a beam step in a scan effort.
  '''
  QUERYFILE         = 'dasgoclient --query=\"file dataset={D} run={R} lumi={L}\"'
  QUERYBLOCK_BYFILE = 'dasgoclient --query=\"block file={F}\"'
  def __init__(self, scan, index):
    self.scan     = scan
    self.index    = index
    self.lumib    = self.scan.scan['LSStartTimes'][self.index]
    self.lumie    = self.scan.scan['LSStopTimes' ][self.index]
    self.timeb    = self.scan.scan['StartTimes'  ][self.index]
    self.timee    = self.scan.scan['StopTimes'   ][self.index]
    self.lumis    = set([l for l in range(self.lumib, self.lumie+1)])
    self.times    = '{B}:{E}'.format(B=self.timeb, E=self.timee)

def popen(cmd): return tuple(l.strip('\n') for l in os.popen(cmd).readlines())
def fetch_blocks(points):
  ''' Qeries needed files (by dataset, run and lumi) from DAS.\n
  Use the file list to query the needed blocks.'''
  from multiprocessing import Pool
  pool = Pool(args.streams)
  FILES   = 'dasgoclient --query="file dataset={D} run={R} lumi={L}"'
  BLOCKS  = 'dasgoclient --query="block file={F}"'
  SIZE    = 'dasgoclient --query="block={B} | grep block.size"'

  sys.stdout.write("Fetching blocks...") ; sys.stdout.flush()
  queriesF  = list(set([FILES.format(D=args.dataset, R=p.scan.runn, L=l) for p in points for l in p.lumis]))
  files     = set(_ for f in pool.map(popen, queriesF) for _ in f)
  queriesB  = [BLOCKS.format(F=f) for f in files]
  blocks    = set(_ for b in pool.map(popen, queriesB) for _ in b)
  queriesS  = [SIZE.format(B=b) for b in blocks]
  size      = sum([int(_) for s in pool.map(popen, queriesS) for _ in s])
  sys.stdout.write("\rFetching blocks...done\n") ; sys.stdout.flush()
  print('''{F} files found, {B} blocks will be added to the crab task ({S} GB)'''.format(F=len(files), B=len(blocks), S=size>>30))
  return blocks

lumijson  = json.load(open(args.input, 'r'))
scans     = [Scan(label=os.path.basename(args.input).strip('.json'), json=lumijson, number=s['ScanNumber']-1) for s in lumijson['Scans']]
points    = [p for s in scans for p in s.points]

JOBNAME     = '_'.join([args.dataset.split('/')[1], os.path.basename(args.input).strip('.json')])
RUNSTRING   = ','.join(str(s.runn)  for s in scans)
TIMESTRING  = ','.join(s.times      for s in scans)
BUNCHSTRING = ','.join(b for b in args.bunchcrossings)
OUTPUT      = '/store/user/{}/BeamSpot/'.format(os.environ['USER'])

config = Configuration()
config.General.workArea         = args.workarea
config.General.requestName      = JOBNAME
config.General.transferOutputs  = True
config.JobType.pluginName       = 'Analysis'
config.Data.publication         = False
config.Data.useParent           = False
config.Data.inputDBS            = 'global'
config.Data.splitting           = 'FileBased' if args.dryrun else 'Automatic'
config.Data.unitsPerJob         = 2700
config.Data.inputDataset        = args.dataset
config.Data.runRange            = RUNSTRING
config.Site.storageSite         = args.storage
config.JobType.psetName         = 'EventSkimming_byTime_byBX.py'
config.Data.outLFNDirBase       = '/store/user/{U}/BeamSpot'.format(U=os.environ['USER'])
config.Data.inputBlocks         = list(fetch_blocks(points))
config.JobType.pyCfgParams = [
  "bunchcrossing={}".format(BUNCHSTRING),
  "timerange={}"    .format(TIMESTRING) ,
]

crabCommand('submit', config=config, dryrun=args.dryrun)