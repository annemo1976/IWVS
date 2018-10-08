#!/usr/bin/env python

# import libraries
from datetime import datetime, timedelta
from satmod import sentinel_altimeter as sa
import argparse

# parser
parser = argparse.ArgumentParser(
    description="""
Check Sentinel-3a data. Example:
./check_S3a.py -r ARCMFC -sd 2018080112 -ed 2018080718 -m -a --show --save
    """
    )
parser.add_argument("-r",
    help="region to check")
parser.add_argument("-sd",
    help="start date of time period to check")
parser.add_argument("-ed",
    help="end date of time period to check")
parser.add_argument("-m",
    help="make map",action='store_const',const=True)
parser.add_argument("-a",
    help="compute availability",action='store_const',const=True)
parser.add_argument("--show",
    help="show figure",action='store_const',const=True)
parser.add_argument("--save",
    help="save figure(s)",action='store_const',const=None)

args = parser.parse_args()
print ("arguments entered are: ",args)

# setup
sdate = datetime(int(args.sd[0:4]),int(args.sd[4:6]),
                int(args.sd[6:8]),int(args.sd[8:10]))
if args.ed is None:
    timewin = 30
    edate = sdate
else:
    edate = datetime(int(args.ed[0:4]),int(args.ed[4:6]),
                    int(args.ed[6:8]),int(args.ed[8:10]))
    timewin = 0

# get data
sa_obj = sa(sdate,edate=edate,timewin=timewin,region=args.r,mode="ARCMFC")

# plot
if bool(args.m)==True:
    sa_obj.quip(region=args.r,show=bool(args.show),save=bool(args.save))

# check availability
if bool(args.a)==True:
    freqlst,datelst=sa_obj.bintime()
    sa_obj.plotavail(datelst,freqlst,show=bool(args.show),save=bool(args.save))
