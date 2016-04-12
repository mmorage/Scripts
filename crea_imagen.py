#!/usr/bin/env python

import sys,os,string
import pyraf
from pyraf import iraf
from iraf import images,tv,sleep,imutil,imgeom,blkrep,imcopy,imdelete

imagen=sys.argv[1]

iraf.imcopy(input=imagen+'[1]',output="test.fits")
iraf.blkrep(input="test.fits",output=imagen+'_GMOS',b1=12,b2=1)

for i in range (1,13):
#    print i
   if i < 2:
#        print i
       iraf.imcopy(input=imagen+'['+str(i)+']',output=imagen+'_GMOS.fits[1:'+str(288)+',*]')
       #    if i>1 and i<12:
   else:
#        print i,i
       iraf.imcopy(input=imagen+'['+str(i)+']',output=imagen+'_GMOS.fits['+str((i-1)*288)+':'+str((i)*288)+',*]')
#    if i>12:    
#        iraf.imcopy(input=imagen+'['+str(i)+']',output=imagen+'_GMOS.fits['+str(i*288)+':'+str((i+1)*288)+',*]')

iraf.imdelete("test.fits")
