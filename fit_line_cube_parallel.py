#!/User/bin/env python
#importing system commands

import sys,os,string

#scientific packages
import pyfits
import scipy
from scipy.optimize import curve_fit, leastsq
import numpy as np
from numpy import random, exp,sqrt
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting, polynomial

#time
import time
# Paralel python
#import pp

start_time1 = time.time()
start_time2 = time.time()




#print len(imagen_in)

#Nota: z is the first element= lambfa
#for z in range (len(imagen)):

####
#
#   Funcion lee_spectra
#   lee un spectrum y lo deja como x e y
#
#
#
#####

#def definition():
#    global Lee_cubo
#    Lee_cubo=12
#def imagen_in():
#global imagen_in
#    imagen_in=sys.argv[1]
imagen_in=sys.argv[1]
l_min_izq=float(sys.argv[2])
l_max_izq=float(sys.argv[3])

l_min_der=float(sys.argv[4])
l_max_der=float(sys.argv[5])

guess_line=float(sys.argv[6])
guess_FWHM=float(sys.argv[7])

orden_pol=float(sys.argv[8])

FILE_OUT=sys.argv[9]

#print imagen_in,sys.argv[1]

def ajusta(x_cube,y_cube,imagen_in,l_min_izq,l_max_izq,l_min_der,l_max_der,guess_line,guess_FWHM,orden_pol):
#def ajusta(x_cube,y_cube,orden_pol): 
   #scientific packages
    import pyfits
    import scipy
    from scipy.optimize import curve_fit, leastsq
    import numpy as np
    from numpy import random, exp,sqrt
    import matplotlib.pyplot as plt
    from astropy.modeling import models, fitting, polynomial
#    global imagen_in
    
#    imagen_in=sys.argv[1]

#    l_min_izq=float(sys.argv[2])
#    l_max_izq=float(sys.argv[3])     
#    l_min_der=float(sys.argv[4])
#    l_max_der=float(sys.argv[5])
#    guess_line=float(sys.argv[6])
#    guess_FWHM=float(sys.argv[7])    
#    orden_pol=float(sys.argv[8])
    

    def Lee_cubo(spectra,XX,YY):
        global imagen
        imagen=pyfits.getdata(spectra,header=False)
        header=pyfits.getheader(spectra)
        
        #print len(imagen)
        #empty array
        Lambda_t=[]
        Flux_t=[]
    
    
        for i in range (len(imagen)):
            y=imagen[i][XX][YY]
            #        x=i*header['CDELT1']+header['CRVAL1']
            x=i*header['CD3_3']+header['CRVAL3']
            Lambda_t.append(float(imagen[i][XX][YY]))
            #Flux_t.append(float(i*header['CDELT1']+header['CRVAL1']))
            Flux_t.append(float(i*header['CD3_3']+header['CRVAL3']))
            #print x,y

        Flux=np.array(Lambda_t)
        Lambda=np.array(Flux_t)
        x=Lambda
        y=Flux
        return x,y


    ##########################
    ##
    ## Funcion Region
    ## Toma una region de un espectro entre
    ## un minimo lambda y un maximo lambda
    ## x e y corresponden a lamba y cuentas o flujo
    ##
    ###########################
    #
    def region(minimo,maximo,x,y):
        xar=[]
        yar=[]
        for i in range(len(x)):
            if (x[i] > minimo) and (x[i] <maximo):
                xar.append(float(x[i]))
                yar.append(float(y[i]))
            
        xar=np.array(xar)
        yar=np.array(yar)
        return xar,yar


    #########################
    #
    # Funcion Region_discontinuo
    # Toma dos regiones de un espectro separadoas entre
    # un minimo lambda y un maximo lambda a la izquierda y un 
    # un minimo lambda y un maximo lambda a la deracha de la emission o obsorption 
    # x e y corresponden a lamba y cuentas (o flujo)
    #
    ##########################

    def region_discontinua(minimo1,maximo1,minimo2,maximo2,x,y):
        xar=[]
        yar=[]
        for i in range(len(x)):
            if ((x[i] > minimo1) and (x[i] <maximo1)) or ((x[i] > minimo2) and (x[i] <maximo2)):
                xar.append(float(x[i]))
                yar.append(float(y[i]))
            
        xar=np.array(xar)
        yar=np.array(yar)
        return xar,yar

    #######
    # poly_fit, fitea un polinomio a datos
    # xp e yp correspondend a x e y a ser fiteado
    #
    # en este caso corresponden al x e y del output de la
    # region discontinua
    #
    #
    #######

    def poly_fit(xp,yp,grado_pol):
    
        t_init = polynomial.Polynomial1D(degree=int(grado_pol))
        fit_t = fitting.LevMarLSQFitter()
        t = fit_t(t_init, xp, yp)
        return t


    #calclulo original
        

    
    x_sci,y_sci=Lee_cubo(imagen_in,x_cube,y_cube)
    x=x_sci 
    y=y_sci 
    xspec_o,yspec_o=region(l_min_izq,l_max_der,x,y)

    #################



    ###Fitting regions with a polynomio


    x_cont_o,y_cont_o=region_discontinua(l_min_izq,l_max_izq,l_min_der,l_max_der,x,y)


    #cont1=poly_fit(xa1,ya1,12)
    #cont2=poly_fit(xa2,ya2,12)
    cont3_o=poly_fit(x_cont_o,y_cont_o,orden_pol)
    
    #print cont1
    #print cont2
    
    #res1= -cont1(xa1)+ ya1
    #res2= -cont2(xa2)+ ya2
    res3_o= -cont3_o(x_cont_o)+ y_cont_o
    
    #se aplica el polinomio al espectro en la zona de interes
    res4_o= -cont3_o(xspec_o)+yspec_o
    
    #####################
    #
    # Normalization!!!
    #
    ######################
    res4_oN= yspec_o/cont3_o(xspec_o)
    
    
    ######################
    
    
    ################
    
    #iteracion 1
    t_init4_o = models.Gaussian1D(amplitude=1, mean=guess_line, stddev=guess_FWHM)
    fit_t4_o = fitting.LevMarLSQFitter()
    t4_o = fit_t4_o(t_init4_o, xspec_o, res4_o)
    
    a_science=t4_o.mean.value
    b_science=t4_o.stddev.value
    Amplitud=t4_o.amplitude.value
    
#    Redefiniendo: de acuerdo al FWHM

    #xspec_o,yspec_o=region(l_min_izq,l_max_der,x,y)    
    #x_cont_o,y_cont_o=region_discontinua(l_min_izq,l_max_izq,l_min_der,l_max_der,x,y)
    #cont3_o=poly_fit(x_cont_o,y_cont_o,orden_pol)
    #res4_o= -cont3_o(xspec_o)+yspec_o

    import numpy
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    import math
        
    CWt= t4_o.mean.value
    FWHMt=2*sqrt(2*math.log(2))*t4_o.stddev.value
    At=t4_o.amplitude.value


    xspec_o,yspec_o=region(CWt-5*FWHMt,CWt+5*FWHMt,x,y)    
    x_cont_o,y_cont_o=region_discontinua(CWt-5*FWHMt,CWt-3*FWHMt,CWt+3*FWHMt,CWt+5*FWHMt,x,y)
    cont3_o=poly_fit(x_cont_o,y_cont_o,orden_pol)
    res4_o= -cont3_o(xspec_o)+yspec_o


    #iteracion 1
    t_init4_o = models.Gaussian1D(amplitude=Amplitud, mean=a_science, stddev=b_science)
    fit_t4_o = fitting.LevMarLSQFitter()
    t4_o = fit_t4_o(t_init4_o, xspec_o, res4_o)

    a_science=t4_o.mean.value
    b_science=t4_o.stddev.value
    Amplitud=t4_o.amplitude.value
    
    
    #iteracion 2 para gaussiana
    t_init4_o = models.Gaussian1D(amplitude=Amplitud, mean=a_science, stddev=b_science)
    fit_t4_o = fitting.LevMarLSQFitter()
    t4_o = fit_t4_o(t_init4_o, xspec_o, res4_o)
    
    residuo_o=-t4_o(xspec_o)+res4_o
    
    #print "resultados",t_init4,t4
    #print "resultados",t4_o
    a_science=t4_o.mean.value
    b_science=t4_o.stddev.value
    c_science_amplitude=t4_o.amplitude.value
    
    #Aplicando FWHM guess
    guess_FWHM_gauss=-float(-b_science)
    #print guess_FWHM_gauss
    #exit(0)
    
    
    ##print t4.mean
    Lambda_gauss_fit_sci="{:10.3f}".format(a_science)
    Sigma_gauss_fit_sci="{:10.3f}".format(b_science)
    #print  Lambda_gauss_fit_sci, Sigma_gauss_fit_sci
    #print a ,b
    
    central_wavelenght = t4_o.mean.value
    FWHM=t4_o.stddev.value
    Amplitude=t4_o.amplitude.value
    
        
    
    import numpy
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    import math
    
    # Define model function to be used to fit to the data above:
    def gauss(x, *p):
        A, mu, sigma = p
        return A*numpy.exp(-(x-mu)**2/(2.*sigma**2))
    
        
    CW= t4_o.mean.value
    FWHM=2*sqrt(2*math.log(2))*t4_o.stddev.value
    A=t4_o.amplitude.value
    
#    def Momentos(x,*p)
    
    
    #INTEGRAL
    from scipy import integrate
    #def myfunc(x, a, b):
    #    return (x**b) + a
    # 
    ## These are the arguments that will be passed as a and b to myfunc()
    args = A,CW,FWHM
    #print args
    # 
    ## Integrate myfunc() from 0.5 to 1.5
    #print  CW,CW-4*FWHM, CW+4*FWHM,FWHM
    #results = integrate.quad(gauss, min(x_sci), max(x_sci), args)
    results = integrate.romberg(gauss, CW-5*FWHM, CW+5*FWHM, args)
    
    #print results, gauss(CW-4*FWHM,A,CW,FWHM), gauss(CW+4*FWHM,A,CW,FWHM), gauss(CW+4*FWHM,A,CW,FWHM)*(CW+4*FWHM-(CW-4*FWHM))
    
    

    #print x_cube,y_cube,A,CW,FWHM,results
#    print  Lambda_gauss_fit_sci, Sigma_gauss_fit_sci

    #plt.plot(xspec_o,res4_o, 'c-',lw=1,label='gaus')
    #plt.plot(xspec_o,t4_o(xspec_o),'r-', lw=2,label='gauss')
    #plt.pause(0.005)
    #plt.clf()
    RESULTADO=int(x_cube),int(y_cube),float(A),float(CW),float(FWHM),float(results)
    return RESULTADO[0],RESULTADO[1],RESULTADO[2],RESULTADO[3],RESULTADO[4],RESULTADO[5]


#import joblib
#from joblib import Parallel,delayed
import pp
job_server=pp.Server()

f=open(FILE_OUT,'w')

#import ndarray

#ajusta(20,20)
for i in range (0,48,4):
    for j in range(0,33):
        f1=job_server.submit(ajusta,(i,j,imagen_in,l_min_izq,l_max_izq,l_min_der,l_max_der,guess_line,guess_FWHM,orden_pol))
        f2=job_server.submit(ajusta,(i+1,j,imagen_in,l_min_izq,l_max_izq,l_min_der,l_max_der,guess_line,guess_FWHM,orden_pol))
        f3=job_server.submit(ajusta,(i+2,j,imagen_in,l_min_izq,l_max_izq,l_min_der,l_max_der,guess_line,guess_FWHM,orden_pol))
        f4=job_server.submit(ajusta,(i+3,j,imagen_in,l_min_izq,l_max_izq,l_min_der,l_max_der,guess_line,guess_FWHM,orden_pol))
        val1=np.array(f1())
        #print val1
        lala= "\n"
        f.write(str(int(i))+' '+str(int(j))+' ')
        val1.tofile(f,sep=" ")
        f.write(lala)
#        lala.tofile(f,sep=" ")
                #f.write(val1)

        f.write(str(int(i+1))+' '+str(int(j))+' ')
        val2=np.array(f2())
        val2.tofile(f,sep=" ")
        f.write(lala)
        #f.write(val2)
#        f.write(val+ '\n' )
        #f.write(val)
#        print val
        
        f.write(str(int(i+2))+' '+str(int(j))+' ')
        val3=np.array(f3())
        val3.tofile(f,sep=" ")
        f.write(lala)
        #f.write(val3)
#        f.write(val+ '\n' )
        #f.write(val)
#        print val
        
        f.write(str(int(i+3))+' '+str(int(j))+' ')
        val4=np.array(f4())
        val4.tofile(f,sep=" ")
        f.write(lala)
        #f.write(val4)
#        f.write(val+ '\n' )
        #f.write(val)
#        print val
        #np.savetxt(f,val2)
        #np.savetxt(f,val3)
        #np.savetxt(f,val4)






f.close()

#ajusta(20,21)
#ajusta(20,22)
#ajusta(20,23)

#ajusta(x_cube2,ycube2) for (x_cube,y_cube) in [(x_cube,y_cube) for x_cube in range(49) for y_cube in range(33)]))
#for (i,j) in [(i,j) for i in range(x) for j in range(y)]

#Parallel(n_jobs=4,verbose=5)(delayed(ajusta(x_cube,y_cube) for (x_cube,y_cube) in [(x_cube,y_cube) for x_cube in range(49) for y_cube in range(33)]))
#Parallel(n_jobs=4,verbose=5)((ajusta(x_cube,20)) for (x_cube) in range(49))


#import pp
#ppservers = ()
#ncpus=4
#job_server = pp.Server(ncpus,ppservers=ppservers)#
##
#job_server = pp.Server(ppservers=ppservers)
#print "Starting pp with", job_server.get_ncpus(), "workers aka CPUs"
#
#jobs=[(input,job_server.submit(ajusta,(x_cube,20,))) for x_cube in range(49)]
#
##CUBOX=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)
##jobs=[(input,job_server.submit,(ajusta,(input,20,('subprocess',)))) for input in CUBOX]
#jobs=[(input,job_server.submit(ajusta,(input,20,,(),))) for input in CUBOX]
#jobs=[(input,job_server.submit(ajusta,(input,20,sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]),float(sys.argv[8])))) for input in CUBOX]


#for input, job in jobs:
 #   print "executing job N", input, "is", job()

#jobs=[(input,job_server.submit(ajusta,(x_cube2,ycube2,input,))) for input in Amplific]
#jobs=job_server.submit(ajusta(x_cube,20) for  x_cube in range(49))



#range(100000))
#ajusta,(x_cube2,ycube2,input,)))


#ppservers = ()
#ppservers = ("10.0.0.1",)

#if len(sys.argv) > 1:
#    ncpus = int(sys.argv[2])
#    # Creates jobserver with ncpus workers
#    job_server = pp.Server(ncpus, ppservers=ppservers)
#else:
#    # Creates jobserver with automatically detected number of workers
#    job_server = pp.Server(ppservers=ppservers)#

#job_server = pp.Server(ppservers=ppservers)

#print "Starting pp with", job_server.get_ncpus(), "workers aka CPUs"
#
#jobs=[]
##loop over the data cube:
#for y_cube2 in range(33):
#    for x_cube2 in range (49):##
#
#        #jobs.append(job_server.submit(ajusta,(x_cube2,y_cube2)))#
#
#        input=job_server.submit(ajusta,(x_cube2,y_cube2))#
#
#for input, job in jobs:
#    print "executing job N", input, "is", job()
#
##part_sum1 =([job() for job in jobs])#
#
##jobs=[(input,job_server.submit(ajusta,(x_cube2,ycube2,input,))) for input in Amplific]
#

#job_server.print_stats()



print "Total execution time: %.2f min" % ((time.time() - start_time1)/60)




