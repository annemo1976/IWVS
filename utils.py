"""
utility fcts for the verification
"""
import numpy as np
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
import sys

def identify_outliers(time,ts,ts_ref=None,hs_ll=None,hs_ul=None,dt=None):
    """
    time -> time series to check neighbour values
    ts -> time series to be checked for outliers
    ts_ref -> time series to compare to (optional)
    hs_ll -> hs lower limit over which values are checked
    hs_ul -> values over limit are being rejected
    """
    if hs_ll is None:
        hs_ll = 1
    if hs_ul is None:
        hs_ll = 30
    std_ts = np.nanstd(ts)
    mean_ts = np.nanmean(ts)
    # forward check
    idx_a = []
    for i in range(1,len(ts)):
        # transform to z
        if len(ts)<25:
            z = (ts[i] - np.nanmean(ts[:]))/np.nanstd(ts[:])
        elif i<13:
            z = (ts[i] - np.nanmean(ts[0:25]))/np.nanstd(ts[0:25])
        elif (i>=13 and i<(len(ts)-12)):
            z = (ts[i] - np.nanmean(ts[i-12:i+12]))/np.nanstd(ts[i-12:i+12])
        elif i>len(ts)-12:
            z = ((ts[i] - np.nanmean(ts[(len(ts-1)-25):-1]))
                /np.nanstd(ts[(len(ts-1)-25):-1]))
        #if (time[i]-time[i-1]).total_seconds()<2:
        if (time[i]-time[i-1])<2:
            #reject if value triples compared to neighbor
            # reject if greater than twice std (>2z)
            if ( ts[i] > hs_ll and ((ts[i-1] >= 3. * ts[i]) or (z>2)) ):
                idx_a.append(i)
        elif (ts[i] > 1. and z>2):
            idx_a.append(i)
    # backward check
    idx_b = []
    for i in range(0,len(ts)-1):
        # transform to z
        if len(ts)<25:
            z = (ts[i] - np.nanmean(ts[:]))/np.nanstd(ts[:])
        elif i<13:
            z = (ts[i] - np.nanmean(ts[0:25]))/np.nanstd(ts[0:25])
        elif (i>=13 and i<len(ts)-12):
            z = (ts[i] - np.nanmean(ts[i-12:i+12]))/np.nanstd(ts[i-12:i+12])
        elif i>len(ts)-12:
            z = ((ts[i] - np.nanmean(ts[(len(ts-1)-25):-1]))
                /np.nanstd(ts[(len(ts-1)-25):-1]))
        #if (time[i+1]-time[i]).total_seconds()<2:
        if (time[i+1]-time[i])<2:
            #reject if value triples compared to neighbor
            # reject if greater than twice std (>2z)
            if ( ts[i] > hs_ll and ((ts[i+1] <= 1/3. * ts[i]) or (z>2)) ):
                idx_b.append(i)
        elif (ts[i] > 1. and z>2):
            idx_b.append(i)
    idx_c = []
    for i in range(len(ts)):
        # reject if hs>hs_ul
        if ts[i]>hs_ul:
            idx_c.append(i)
    idx = np.unique(np.array(idx_a + idx_b + idx_c))
    if len(idx)>0:
        print(str(len(idx)) 
                + ' outliers detected of ' 
                + str(len(time)) 
                + ' values')
        return idx
    else:
        print('no outliers detected')
        return []

def grab_PID():
    """
    function to retrieve PID and display it to be able to kill the 
    python program that was just started
    """
    import os
    # retrieve PID
    PID = os.getpid()
    print ("\n")
    print ("PID - with the license to kill :) ")
    print (str(PID))
    print ("\n")
    return

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def rmsd(a,b):
    '''
    root mean square deviation
    if nans exist the prinziple of marginalization is applied
    '''
    a,b = np.array(a),np.array(b)
    comb = a + b
    idx = np.array(range(len(a)))[~np.isnan(comb)]
    a1=a[idx]
    b1=b[idx]
    n = len(a1)
    diff2 = (a1-b1)**2
    msd = diff2.sum()/n
    rmsd = np.sqrt(msd)
    return msd, rmsd

def scatter_index(obs,model):
    msd,rmsd = rmsd(obs,model)
    SI = rmsd/np.nanmean(obs)*100.
    return SI

def corr(a,b):
    '''
    root mean square deviation
    if nans exist the prinziple of marginalization is applied
    '''
    a,b = np.array(a),np.array(b)
    comb = a + b
    idx = np.array(range(len(a)))[~np.isnan(comb)]
    a1=a[idx]
    b1=b[idx]
    corr = np.corrcoef(a1,b1)[1,0]
    return corr

def bias(a,b):
    """
    if nans exist the prinziple of marginalization is applied
    """
    a,b = np.array(a),np.array(b)
    comb = a + b
    idx = np.array(range(len(a)))[~np.isnan(comb)]
    a1=a[idx]
    b1=b[idx]
    N = len(a1)
    bias = np.sum(a1-b1)/N
    return bias

def mad(a,b):
    """
    mean absolute deviation
    if nans exist the prinziple of marginalization is applied
    """
    a,b = np.array(a),np.array(b)
    comb = a + b
    idx = np.array(range(len(a)))[~np.isnan(comb)]
    a1=a[idx]
    b1=b[idx]
    N = len(a1)
    mad = np.sum(np.abs(a1-b1))/N
    return mad

def runmean(vec,win,mode=None):
    """
    input:  vec = vector of values to me smoothed
            win = window length
            mode= string: left, centered, right
    """
    if mode is None:
        mode='centered'
    out = np.zeros(len(vec))*np.nan
    length = len(vec)-win+1
    if mode=='left':
        count = win-1
        start = win-1
        for i in range(length):
            out[count] = np.mean(vec[count-start:count+1])
            count = count+1
    elif mode=='centered':
        count = win/2
        start = win/2
        for i in range(length):
            if win%2==0:
                sys.exit("windo length needs to be odd!")
            else:
                out[count] = np.mean(vec[count-start:count+start+1])
                count = count+1
    elif mode=='right':
        count = 0
        for i in range(length):
            out[count] = np.mean(vec[i:i+win])
            count = count+1
    return out

def bootstr(a,reps):
    """
    input:    - is a time series of length n
              - reps (number of repetitions)
    output:   - an array of dim n x m where
                m is the number of repetitions
              - indices of draws
    """
    n = len(a)
    b = np.random.choice(a, (n, reps))
    bidx = np.zeros(b.shape) * np.nan
    for i in range(len(a)):
        tmp = np.where(b==a[i])
        bidx[tmp[0],tmp[1]] = i
        del tmp
    return b, bidx.astype('int')

def marginalize(a,b=None):
    if b is None:
        a = np.array(a)
        return a[~np.isnan[a]]
    else:
        a,b = np.array(a),np.array(b)
        comb = a + b
        idx = np.array(range(len(a)))[~np.isnan(comb)]
        a1=a[idx]
        b1=b[idx]
        return a1,b1,idx

