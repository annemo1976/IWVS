#!/usr/bin/env python
import sys
import time
from datetime import datetime, timedelta
import calendar
from satmod import sentinel_altimeter as sa
from satmod import validate
from copy import deepcopy
import numpy as np
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from utils import grab_PID
from stationmod import matchtime
from satmod import get_model2
import os
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(
    description="""
Program to validate model (mwam4,mwam8,ARCMFC) against stations
or Sentinel-3a.
    """
    )
parser.add_argument("-m", 
    help="Model to be evaluated (mwam4, mwam8, ARCMFC)")
parser.add_argument("-p", 
    help="Observations to evaluate against (platform)")
parser.add_argument("-s",  
    help="Observations to evaluate against (sentinel)")
parser.add_argument("-b",
    help="Observations to evaluate against buoy")
parser.add_argument("-sd", help="start date")
parser.add_argument("-ed", help="end date")
args = parser.parse_args()
print args
