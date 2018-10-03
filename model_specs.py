"""
file to specify model specifications such that models can be added 
and data can be imported easily
"""

from datetime import datetime, timedelta

model_dict={'ARCMFC':
            {'Hs':'VHM0',
            'lons':'lon',
            'lats':'lat',
            'rotlons':'rlon',
            'rotlats':'rlat',
            'time': 'time',
            'path':('/lustre/storeA/project/'
                    + 'copernicus/sea/mywavewam8r625/arctic/'),
            #'file_template':'%Y%m%d_MyWaveWam8r625_b%Y%m%d.nc',
            'file_template':'_MyWaveWam8r625_b%Y%m%d.nc',
            'basetime':datetime(1970,1,1),
            'units_time':'seconds since 1970-01-01 00:00:00',
            'delta_t':'0000-00-00 (01:00:00)'
            },
        'ARCMFCnew':
            {'Hs':'VHM0',
            'lons':'longitude',
            'lats':'latitude',
            'rotlons':'rlon',
            'rotlats':'rlat',
            'time': 'time',
            'path':('/lustre/storeB/users/anac/HINDCAST2017/BETAMAX1.20/'),
            'file_template':'%Y%m%d00.nc',
            'basetime':datetime(1970,1,1),
            'units_time':'seconds since 1970-01-01 00:00:00',
            'delta_t':'0000-00-00 (01:00:00)'
            },
        'mwam4':
            {'Hs':'hs',
            'lons':'longitude',
            'lats':'latitude',
            'rotlons':'rlon',
            'rotlats':'rlat',
            'time': 'time',
            'path_template':('/lustre/storeB/immutable/' +  
                           'archive/projects/metproduction/' + 
                           'DNMI_WAVE/%Y/%m/%d/'),
            'path':('/lustre/storeB/immutable/archive/' + 
                    'projects/metproduction/DNMI_WAVE/'),
            #'file_template':'MyWave_wam4_WAVE_%Y%m%dT%HZ.nc',
            'file_template':'MyWave_wam4_WAVE_%Y%m%dT%HZ.nc',
            'basetime':datetime(1970,1,1),
            'units_time':'seconds since 1970-01-01 00:00:00',
            'delta_t':'0000-00-00 (01:00:00)'
            }
        }
