#!/usr/bin/env python
 
import sys,os,string

import astropy
from astropy.io import fits
import numpy as np 
import pyfits
import scipy
from scipy import ndimage



#  
#  NOTA: Se asume que la imagen esta corregida por Bias y Flat! 
#        Image FLAT and BIAS corrected!   
#
#  NOTA2: Cosmicos y lineas generan problemas en el fit del continuum
#  Se cambio spline3 por legendre en  continuum 
#        Cosmics sometimes create problems, better run first la_cosmic
#
#  NOTA3: Crea muchas imagenes extra REGION_*
#         It creates many images REGION_*
#        
#  NOTA4: Requiere ureka 
#         NEEDS UREKA!!!  
#
#  USE: 
#  python Amp5.py imagen.fits
#
#  Output: imagen_Amp5.fits
#
#
## V 1.2 M.Mora 26.08.2015
#  Changes:
#  Spline3 order 1--->legendre order 3
#  se mejora el fiteo :) No molestan los cosmicos
#  Added  ,'sci',0 en getdata. No hay necesidad de copiar la imagen.fits[sci]  :)
# 
# Se agrego '[sci]'en el continuum que se hace sobre el Amp5
# Ver: CONTINUUM CCD ORIGINAL SALTANDOSE LA REGION DEL Amp5
#   
# Imagen final truncada el .fits
#
#
#
#

imagen_in=sys.argv[1]
#loading the image
header=pyfits.getheader(imagen_in)
imagen=pyfits.getdata(imagen_in,'sci',0)

imagen2=pyfits.getdata(imagen_in,'sci',0)
imagen3=pyfits.getdata(imagen_in,'sci',0)
imagen4=pyfits.getdata(imagen_in,'sci',0)
imagen5=pyfits.getdata(imagen_in,'sci',0)
imagen6=pyfits.getdata(imagen_in,'sci',0)
imagen7=pyfits.getdata(imagen_in,'sci',0)
imagen8=pyfits.getdata(imagen_in,'sci',0)
imagen9=pyfits.getdata(imagen_in,'sci',0)
imagen10=pyfits.getdata(imagen_in,'sci',0)
imagenB=pyfits.getdata(imagen_in,'sci',0)
imagenC=pyfits.getdata(imagen_in,'sci',0)

#Truncando el .fits para la imagen final
imagen_end=imagen_in[:-5]
print imagen_end

#exit()


imagen_no=imagen
imagen_no2=imagen2
imagen_no3=imagen3
imagen_no4=imagen4
imagen_no5=imagen5
imagen_no6=imagen6
imagen_no7=imagen7
imagen_no8=imagen8
imagen_no9=imagen9
imagen_no10=imagen10
imagen_noB=imagenB
imagen_noC=imagenC

print len(imagen)
print len(imagen2)
print len(imagen3)
print len(imagen4)
print len(imagen5)
print len(imagen6)



#NOTA: No estoy usando image_no en las asignaciones
# de valor ni len(imagen) en el for porque crea 
#la primera OK pero las segundas las crea en blanco.
# No se por que!!!!


#Separando por regiones

for i in range (len(imagenB)):
    for j in range(3132):


        #Region 1

        if (j > 1054) and (j<1311) and (i>0) and (i< 447):
            imagen_noB[i,j]=imagen[i,j] 
            imagen_no2[i,j]=1
        else:
            imagen_noB[i,j]=0#
            imagen_no2[i,j]=0#


pyfits.writeto("REGION_1_ORIG_resto0.fits",imagen_noB,header)
pyfits.writeto("REGION_1_ZERO_resto1.fits",imagen_no2,header)
            

#Region 2

for i in range (len(imagen2)):
    for j in range(3132):
 
        if (j > 1054) and (j < 1174) and (i>446) and (i<705):  
            imagen_no3[i,j]=imagen[i,j] 
            imagen_no4[i,j]=1 
        else:
            imagen_no3[i,j]=0
            imagen_no4[i,j]=0


pyfits.writeto("REGION_2_ORIG_resto0.fits",imagen_no3,header)
pyfits.writeto("REGION_2_ZERO_resto1.fits",imagen_no4,header)




#Region 3

for i in range (len(imagen3)):
    for j in range(3132):
 
        if (j > 1175) and (j < 1311) and (i>446) and (i<705):  
            imagen_no5[i,j]=imagen[i,j] 
            imagen_no6[i,j]=1 
        else:
            imagen_no5[i,j]=0
            imagen_no6[i,j]=0



pyfits.writeto("REGION_3_ORIG_resto0.fits",imagen_no5,header)
pyfits.writeto("REGION_3_ZERO_resto1.fits",imagen_no6,header)


#Region 4

for i in range (len(imagen4)):
    for j in range(3132):
 
        if (j > 1054) and (j < 1174) and (i>704) and (i<2089):  
            imagen_no7[i,j]=imagen[i,j] 
            imagen_no8[i,j]=1 
        else:
            imagen_no7[i,j]=0
            imagen_no8[i,j]=0


pyfits.writeto("REGION_4_ORIG_resto0.fits",imagen_no7,header)
pyfits.writeto("REGION_4_ZERO_resto1.fits",imagen_no8,header)



#Region 5

for i in range (len(imagen5)):
    for j in range(3132):
 
        if (j > 1173) and (j < 1311) and (i>704) and (i<2089):  
            imagen_no9[i,j]=imagen[i,j] 
            imagen_no10[i,j]=1 
        else:
            imagen_no9[i,j]=0
            imagen_no10[i,j]=0

pyfits.writeto("REGION_5_ORIG_resto0.fits",imagen_no9,header)
pyfits.writeto("REGION_5_ZERO_resto1.fits",imagen_no10,header)





for i in range (len(imagenC)):
    for j in range(3132):


        #Amp5 

        if (j > 1054) and (j<1311): 
            imagen_noC[i,j]=1
        else:
            imagen_noC[i,j]=0#



pyfits.writeto("REGION_Amp5_resto0.fits",imagen_noC,header)






from pyraf import iraf
from iraf import onedspec,continuum,imutil,imarith


############# CONTINUUM###############

iraf.continuum(input="REGION_1_ORIG_resto0.fits",output="REGION_1_ORIG_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='1056:1309',naverag='3',functio='legendre',order='4',low_rej='3',high_rej='3',niterate='10',ask='no' )


iraf.continuum(input="REGION_2_ORIG_resto0.fits",output="REGION_2_ORIG_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='1056:1172',naverag='3',functio='legendre',order='4',low_rej='3',high_rej='3',niterate='10',ask='no' )


iraf.continuum(input="REGION_3_ORIG_resto0.fits",output="REGION_3_ORIG_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='1178:1309',naverag='3',functio='legendre',order='4',low_rej='3',high_rej='3',niterate='10',ask='no' )

iraf.continuum(input="REGION_4_ORIG_resto0.fits",output="REGION_4_ORIG_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='1056:1172',naverag='3',functio='legendre',order='4',low_rej='3',high_rej='3',niterate='10',ask='no' )

iraf.continuum(input="REGION_5_ORIG_resto0.fits",output="REGION_5_ORIG_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='1178:1309',naverag='3',functio='legendre',order='4',low_rej='3',high_rej='3',niterate='10',ask='no' )





################# CONTINUUM CCD ORIGINAL SALTANDOSE LA REGION DEL Amp5


iraf.continuum(input=imagen_in+'[sci]',output=imagen_in+"_CONT.fits",lines="*",band="*",type='fit',replace='no',interac='no',sample='725:1016,1327:1669',naverag='3',functio='spline3',order='1',low_rej='3',high_rej='3',niterate='10',ask='no' )

####  MULTIPLICANDO TODAS LAS REGIONES PARA QUE QUEDEN SOLO LAS REGIONES DE INTERES

iraf.imarith(operand1="REGION_1_ORIG_CONT.fits", op="*",operand2="REGION_1_ZERO_resto1.fits",result="REGION1_MULT.fits")
iraf.imarith(operand1="REGION_2_ORIG_CONT.fits", op="*",operand2="REGION_2_ZERO_resto1.fits",result="REGION2_MULT.fits")
iraf.imarith(operand1="REGION_3_ORIG_CONT.fits", op="*",operand2="REGION_3_ZERO_resto1.fits",result="REGION3_MULT.fits")
iraf.imarith(operand1="REGION_4_ORIG_CONT.fits", op="*",operand2="REGION_4_ZERO_resto1.fits",result="REGION4_MULT.fits")
iraf.imarith(operand1="REGION_5_ORIG_CONT.fits", op="*",operand2="REGION_5_ZERO_resto1.fits",result="REGION5_MULT.fits")



###Sumando todas las regiones...=Amp5 
iraf.imarith(operand1="REGION1_MULT.fits", op="+",operand2="REGION2_MULT.fits",result="REGION12_TEMP.fits")
iraf.imarith(operand1="REGION12_TEMP.fits", op="+",operand2="REGION3_MULT.fits",result="REGION123_TEMP.fits")
iraf.imarith(operand1="REGION123_TEMP.fits", op="+",operand2="REGION4_MULT.fits",result="REGION1234_TEMP.fits")
iraf.imarith(operand1="REGION1234_TEMP.fits", op="+",operand2="REGION5_MULT.fits",result="REGION12345_TEMP.fits")



# Multiplicando continuum Amp5 por region Amp5 (Mata el resto del CCD con 0 y deja solo el Amp5)  

iraf.imarith(operand1="REGION_Amp5_resto0.fits", op="*",operand2=imagen_in+"_CONT.fits",result="REGION_Amp5_TEMP.fits")

#resta
iraf.imarith(operand1="REGION_Amp5_TEMP.fits", op="-",operand2="REGION12345_TEMP.fits",result="PSEUDO_FLAT_TEMP.fits")


#agregando diferencia al original !!! Hora de la verdad!

iraf.imarith(operand1="PSEUDO_FLAT_TEMP.fits", op="+",operand2=imagen_in+'[sci]',result=imagen_end+"_Corrected.fits")


#Borrando los archivos creados
print "Borrando archivos creados, deleting files  REGION_...."


os.remove("REGION_1_ZERO_resto1.fits")
os.remove("REGION_1_ORIG_resto0.fits")
os.remove("REGION_2_ORIG_resto0.fits")
os.remove("REGION_2_ZERO_resto1.fits")
os.remove("REGION_3_ZERO_resto1.fits")
os.remove("REGION_3_ORIG_resto0.fits")
os.remove("REGION_4_ZERO_resto1.fits")
os.remove("REGION_4_ORIG_resto0.fits")
os.remove("REGION_5_ZERO_resto1.fits")
os.remove("REGION_5_ORIG_resto0.fits")
os.remove("REGION_Amp5_resto0.fits")
os.remove("REGION_1_ORIG_CONT.fits")
os.remove("REGION_2_ORIG_CONT.fits")
os.remove("REGION_3_ORIG_CONT.fits")
os.remove("REGION_4_ORIG_CONT.fits")
os.remove("REGION_5_ORIG_CONT.fits")
os.remove("REGION1_MULT.fits")
os.remove("REGION2_MULT.fits")
os.remove("REGION3_MULT.fits")
os.remove("REGION4_MULT.fits")
os.remove("REGION5_MULT.fits")
os.remove("REGION12_TEMP.fits")
os.remove("REGION123_TEMP.fits")
os.remove("REGION1234_TEMP.fits")
os.remove("REGION12345_TEMP.fits")
os.remove("REGION_Amp5_TEMP.fits")
os.remove("PSEUDO_FLAT_TEMP.fits")






##########################################################
#
# Copiando la imagen corregida dentro de la correcta
# en formato gemini.
#
##########################################################


imagen_end=imagen_in[:-5]

result_END=imagen_end+"_Corrected.fits"

FILE_TEMP=imagen_end+"_tmp.fits"


imagen_header_original=sys.argv[1]   # Imagen Original con todos los headers, la misma usada para la correccion del amp5
imagen_Corre=imagen_end+"_Corrected.fits"          # Output de la correccion de amp5, NAME_Corrected.fits

#copiando el archivo
import shutil
shutil.copyfile(imagen_header_original,FILE_TEMP)

pyfits.info(imagen_header_original)
pyfits.info(FILE_TEMP)
pyfits.info(imagen_in)

imagen_header2= FILE_TEMP # deben ser igual al de imagen_header

header=pyfits.getheader(FILE_TEMP)
header2=pyfits.getheader(FILE_TEMP,2)

  
imagen_no_header=pyfits.getdata(imagen_Corre,header=False)



from pyfits import update
pyfits.update(imagen_header2,imagen_no_header,ext=2)
pyfits.update(imagen_header2,imagen_no_header,header2,2)

###copiando resultado final

FILE_FIN=imagen_end+'_Amp5.fits'
#copiando el archivo
import shutil
shutil.copyfile(FILE_TEMP,FILE_FIN)

#Final Sanity check

pyfits.info(FILE_FIN)




print "Gracias por usar M.Mora scripts!!"
print "mmora at astro.puc.cl"



