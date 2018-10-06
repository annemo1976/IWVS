from datetime import datetime, timedelta
from satmod import sentinel_altimeter as sa
sdate = datetime(2018,9,1)
edate = datetime(2018,9,10)
sa_obj = sa(sdate,edate=edate,timewin=0,region="ARCMFC")
freqlst,datelst=sa_obj.bintime()
sa_obj.plotavail(datelst,freqlst,show=True)
