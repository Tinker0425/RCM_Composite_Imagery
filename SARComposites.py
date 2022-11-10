#################
# KT - 11/4/22
# Goal is to grab RCM & Sentinel composites
# 
###############
### only on first go of opening Miniforge
### pip install gdown
###
### Must name month file i.e. 'November_2022'
### Must name day file i.e. '04Nov22'
###
#################

import gdown
from datetime import date
import datetime
from bs4 import BeautifulSoup
import requests
import re
import os.path


### First get the current date names for strings
today = date.today()
print(today)
year = today.strftime("%Y")
yr = today.strftime("%y")
month = today.strftime("%B")
mon = today.strftime("%b")
day = today.strftime("%d")

### Second get the Julian Date String
def datestdtojd (stddate):
    sdtdate = stddate.timetuple()
    jdate = sdtdate.tm_yday
    return(jdate)

juliandate = str(datestdtojd(today))
print(juliandate)

### Third, create string of filenames
Beaufort_RCMgrab = "^Beaufort_RCM_NRCS_Composite_"+year+juliandate
Beaufort_S1grab = "^Beaufort_S1_NRCS_Composite_"+year+juliandate
Bering_RCMgrab = "^Bering_RCM_NRCS_Composite_"+year+juliandate
Bering_S1grab = "^Bering_S1_NRCS_Composite_"+year+juliandate
Chukchi_RCMgrab = "^Chukchi_RCM_NRCS_Composite_"+year+juliandate
Chukchi_S1grab = "^Chukchi_S1_NRCS_Composite_"+year+juliandate
Seas = [Beaufort_RCMgrab, Beaufort_S1grab, Bering_RCMgrab, Bering_S1grab, Chukchi_RCMgrab, Chukchi_S1grab]

### Forth, grab the correct files from the website
url = 'https://www.star.nesdis.noaa.gov/socd/mecb/sar/AKDEMO_products/COMPOSITE_TIFF/HIRES/'
url_request = requests.get(url)
html_text = url_request.text
soup = BeautifulSoup(html_text, 'html.parser')

for sea in Seas:
    for link in soup.findAll('a', attrs={'href': re.compile(sea)}):
        print(link.get('href'))
        filename_tiff = str(link.get('href'))
        full_url = url+filename_tiff
        output = 'I:\\IMAGERY\\SarImages_Daily\\'+month+'_'+year+'\\'+day+mon+yr+'\\'+filename_tiff
        print(output)
        if os.path.exists(output):
            print('File exists')
        else:
            print('Please wait for file to download')
            gdown.download(full_url, output, quiet=False)
            
