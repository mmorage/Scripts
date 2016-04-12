#!/usr/bin/env python
#############################
#
# importing systems and iraf
#
############################

import sys,os,string
import glob
from subprocess import call
import pyraf
from pyraf import iraf
from iraf import system, sleep
from iraf import images,tv,display




files= [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith(('.fits')):
        if f.startswith(('S')):
            print f
            images.tv.display (f+'[1]', 1)
            #    images.tv.display (seeim, 1)
            raw_input("Press Enter to continue...")





###########################
#
# Displaying all images.  ds9 Needs to be open!! 
#
###########################

#
#FILE=open('delme.tmp','r')  # Opening the file, only read
#lines=FILE.readlines()    # Reading lines
#FILE.close()              # Closing the file

#for line in lines:
#    seeim=line.strip()  # <-- cuts the "\n" at the end of each line in the archive
#    images.tv.display (seeim+'[1]', 1)
#    images.tv.display (seeim, 1)
#    raw_input("Press Enter to continue...")
#    sleep(2)
