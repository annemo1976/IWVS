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

# parser
parser = argparse.ArgumentParser(
    description="""
Validate a wave model (mwam4, mwam8, ARCMFC) against observations 
(platform, satellite, buoys). Example:
./validate.py -m ARCMFC -fc 2018080218 -sat s3a
./validate.py -m mwam4 -fc 2018080218 -lt 6 -sat s3a
    """,
    formatter_class = RawTextHelpFormatter
    )
parser.add_argument("-m", metavar='model',
    help="model/region to check (mwam4,mwam8,ARCMFC)")
parser.add_argument("-lt", metavar='leadtime', type=int,
    help="leadtime in hours")
parser.add_argument("-fc", metavar='fcdate',
    help="forecasted date to check")
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
fc_date = datetime(int(args.fc[0:4]),int(args.fc[4:6]),
                int(args.fc[6:8]),int(args.fc[8:10]))
if args.lt is None:
    timewin = 30
    init_date = fc_date
else:
    init_date = fc_date - timedelta(hours=args.lt)
    timewin = 0

if args.sat == 's3a':
    # get model collocated values
    sa_obj = sa(fc_date,timewin=timewin,region=args.m)
    results_dict = get_model2(sa_obj,args.m,init_date,fc_date)
    print results_dict
    valid_dict=validate(results_dict)
    print valid_dict

if args.plat is not None:
    sc_obj = sc(args.plat,sdate,edate)
    ctime, cidx = matchtime(fc_date,fc_date,sc_obj.time,sc_obj.basedate)
