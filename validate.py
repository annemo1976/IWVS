#!/usr/bin/env python
from datetime import datetime, timedelta
from satmod import sentinel_altimeter as sa
from stationmod import station_class as sc
from stationmod import matchtime, get_model
from satmod import get_model2
from satmod import validate
from utils import identify_outliers
import os
import argparse
from argparse import RawTextHelpFormatter
import sys

# parser
parser = argparse.ArgumentParser(
    description="""
Validate a wave model (mwam4, mwam8, ARCMFC) against observations 
(platform, satellite, buoys). Examples:
./validate.py -m ARCMFC -fc 2018080200 -sat s3a # files 24h init steps
./validate.py -m ARCMFC -fc 2018080218 -sat s3a # files 24h init steps
./validate.py -m mwam8 -fc 2018080218 -sat s3a # files 12h init steps
./validate.py -m mwam4 -fc 2018080218 -sat s3a # files 6h init steps
# Problems with leadtime e.g.:
./validate.py -m mwam8 -fc 2018080218 -lt 12 -sat s3a # 12h
./validate.py -m mwam4 -fc 2018080218 -lt 6 -sat s3a #  6h
    """,
    formatter_class = RawTextHelpFormatter
    )
parser.add_argument("-m", metavar='model',
    help="model/region to check (mwam4,mwam8,ARCMFC)")
parser.add_argument("-lt", metavar='leadtime', type=int,
    help="leadtime in hours")
parser.add_argument("-fc", metavar='fcdate',
    help="forecasted date to check")
parser.add_argument("-sd", metavar='startdate',
    help="start date of time period to be evaluated")
parser.add_argument("-ed", metavar='enddate',
    help="end date of time period to be evaluated")
parser.add_argument("-plat", metavar='platform',
    help="name of platform")
parser.add_argument("-sat", metavar='satellite',
    help="name of satellite")
parser.add_argument("-buoy", metavar='buoy',
    help="name of buoy")
parser.add_argument("--diag",
    help="make diagnostics")
parser.add_argument("--show",
    help="show figures")
parser.add_argument("--save", metavar='outpath',
    help="save figure(s)")

args = parser.parse_args()
print ("Parsed arguments: ",args)

# setup
if (args.lt is None and args.fc is not None):
    fc_date = datetime(int(args.fc[0:4]),int(args.fc[4:6]),
                int(args.fc[6:8]),int(args.fc[8:10]))
    timewin = 30
    init_date = fc_date
elif (args.lt is not None and args.fc is not None):
    fc_date = datetime(int(args.fc[0:4]),int(args.fc[4:6]),
                int(args.fc[6:8]),int(args.fc[8:10]))
    init_date = fc_date - timedelta(hours=args.lt)
    timewin = 0

if (args.ed is None and args.sd is not None):
    sdate = datetime(int(args.sd[0:4]),int(args.sd[4:6]),
                int(args.sd[6:8]),int(args.sd[8:10]))
    edate = sdate
elif (args.ed is not None and args.sd is not None):
    sdate = datetime(int(args.sd[0:4]),int(args.sd[4:6]),
                int(args.sd[6:8]),int(args.sd[8:10]))
    edate = datetime(int(args.ed[0:4]),int(args.ed[4:6]),
                int(args.ed[6:8]),int(args.ed[8:10]))
if (args.fc is None and args.sd is None):
    sys.exit("-> Error: A date or time period needs to be given!")
if (args.plat is None and args.sat is None and args.buoy is None):
    sys.exit("-> Error: A source of observations needs to be given!")
if (args.m is None):
    sys.exit("-> Error: A model to validate needs to be given!")

if args.sat == 's3a':
    # get model collocated values
    sa_obj = sa(fc_date,timewin=timewin,region=args.m)
    results_dict = get_model2(sa_obj,args.m,init_date,fc_date)
    valid_dict=validate(results_dict)
    print valid_dict

if args.plat is not None:
    sc_obj = sc(args.plat,sdate,edate)
    ctime, cidx = matchtime(fc_date,fc_date,sc_obj.time,sc_obj.basedate)
