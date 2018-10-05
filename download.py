#!/usr/bin/env python
import time
from datetime import datetime as dt
from datetime import datetime, timedelta
from satmod import get_remotefiles

satpath_ftp_014_001 = ('/Core/'
                        + 'WAVE_GLO_WAV_L3_SWH_NRT_OBSERVATIONS_014_001/'
                        + 'dataset-wav-alti-l3-swh-rt-global-s3a/'
                        )
satpath_lustre = '/lustre/storeA/project/fou/om/altimeter/'

now=dt.now()

#sdate = dt(now.year,now.month,now.day)-timedelta(days=1)
# use two days to create some redundancy
sdate = dt(now.year,now.month,now.day)-timedelta(days=2)
edate = dt(now.year,now.month,now.day)
#sdate = dt(2018,8,31)
#edate = dt(2018,10,1)


start_time = time.time()
sa_obj = get_remotefiles(satpath_ftp_014_001,satpath_lustre,
            sdate,edate,timewin=30,corenum=8,download=True)
time1 = time.time() - start_time
print("Time used for collecting data: ", time1, " seconds")
