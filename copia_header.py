#!/usr/bin/env python


import sys,os,string

import astropy
from astropy.io import fits 
from astropy.wcs import WCS
import numpy as np
from numpy import random
import scipy
from scipy import ndimage
import math
from pyraf import iraf
import pyfits 


##copia header de una imagen a otra

imagen_header=sys.argv[1]
imagen=sys.argv[2]
imagen_out=sys.argv[3]


header=pyfits.getheader(imagen_header)

imagen_no_header=pyfits.getdata(imagen,0)

pyfits.writeto(imagen_out,imagen_no_header,header)


