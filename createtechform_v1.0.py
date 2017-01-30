#!/usr/bin/env python

##
#
# Based in createformv12.pl
#  
##

import xml.etree.ElementTree as ET
import os,sys,string
import numpy as np
from lxml.etree import parse as lparse

#read each xml file into an array


files= [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if f.endswith(('.xml')):
        print f
        file_out=f[:-3]+'txt' 
        print file_out

test=sys.argv[1]



ltree= lparse(test)
tree = ET.parse(test) #setup ETread
root = tree.getroot() #define root 
#get PI name
for pi in root.iter('pi'):
    pilastname= pi.find('lastName').text
    piname=pi.find('firstName').text
    email=pi.find('email').text

for proposal in root.iter('proposal'):
    Title=proposal.find('title').text



#arrays
partner=[]
tiempo_req=[]
tiempo_min=[]

tiempo_req3=[]
tiempo_min3=[]

for proposalClass in root.iter('proposalClass'):
    for queue in proposalClass.iter('queue'): 
        #print queue.tag, queue.attrib
        Too= queue.get('tooOption')  #asking if it is a ToO
        
        for ngo in queue.iter('ngo'):
            #time per partner
            partner.append(ngo.find('partner').text)
            for request in ngo.iter('request'): 
                tiempo_req.append(request.find('time').text)
                tiempo_min.append(request.find('minTime').text)
                                          
            for response in ngo.iter('response'):
                for receipt in response.iter('receipt'):
                    ID=receipt.find('id').text


##############
#
# classical mode, not tested
#
############

#    for queue in proposalClass.iter('classical'): 
#        #print queue.tag, queue.attrib
#        #Too= classical.get('tooOption')  #asking if it is a ToO
#        
#        for classical in queue.iter('classical'):
#            #time per partner
#            partner.append(classical.find('partner').text)
#            for request in classical.iter('request'): 
#                tiempo_req.append(request.find('time').text)
#                tiempo_min.append(request.find('minTime').text)
#                                          
#            for response in classical.iter('response'):
#                for receipt in response.iter('receipt'):
#                    ID=receipt.find('id').text


# Band 3 time: I do not know the partner distribution
        for band3request in queue.iter('band3request'):
            tiempo_req3.append(band3request.find('time').text)
            tiempo_min3.append(band3request.find('minTime').text)





Requested_instruments=[]
insturment_mode=[]
k={}
d=[]
Nombre=[]
for blueprints in root:
    key=blueprints.tag
    if blueprints.getchildren(): 
        for child in blueprints:
            if blueprints.tag == 'blueprints':
                key += '/'+ child.tag
                k.update({key: child.text})
                lala=key
            for children1 in child:
                children1.getchildren()
                #print children1
                instrument_mode=" "
                key2=children1.tag
                for children2 in children1:
                    children2.getchildren()
                    if children2.tag =='name':
                        
                        Nombre.append(children2.text) 
                        #print children2.tag
                        #print children2.text
                        d.append({key2: children2.text})
                        instrument_mode=d#'\n'




out_put_file=open(file_out,'w')

#print instrument_mode


#print piname, pilastname
#print email
#print Title
#print Time_band12
#print Too
#print partner
#print IDpri
#
#


# output to a file

temp=sys.stdout                   
sys.stdout =open("gemseeing.tmp",'w')       # redirect all output to the file
        
        


print  "PRIMARY TECHNICAL ASSESSMENT FORM"
print  "Please keep the format of this form so that it is machine readable. "
print  "Although parts are pre-filled, please check these and correct if necessary."
print  "============================================================ "

print  "Gemini Partner (AR/AU/BR/CA/CL/GS/US/UH): ", '/'.join(partner) 
#for i in range (len (partner)): print partner[i]+" "

print  "NGO Proposal ID:" + ID

print  "Assessor Code: ";

print  "Title:" + Title

print  "PI: " +piname, pilastname
print  "PI email:"+email
print  "============================================================ ";
print  "TECHNICAL ASSESSMENT SUMMARY";
print "TECHNICAL ASSESSMENT SUMMARY";
print "Overall Grade: ";
print "[1. OK ";
print "2. minor problems, fixed with or without PI iteration ";
print "3. major problems, fixed after iteration with the PI ";
print "4. major problems, not fixed] ";
print "Keyword summary of major issues to be highlighted to the TAC: ";
print "============================================================ ";

print  "OBSERVATIONAL DETAILS ";

print  "Mode:"

#print  "Telescope: $telescope[$j] ";

print  "Instrument(s)/Mode(s):" 
for n in range(len (Nombre)):
    print Nombre[n]
#print d

#print  "LASER: $laser[$j] ";

print  "ToO:", Too
#print  "[Please check whether target is transient and flag here if necessary.] ";
 
#print  "Suitable for poor weather: ";
 #                 
print "============================================================";
print "REQUESTED TIMES";		
#print '%20s '
print  '                    Time Request       Minimum Time Request'
print   ""
for k in range (len(tiempo_req)):
    print partner[k],"                ",       tiempo_req[k],"                ",      tiempo_min[k]
print  "-------------------------------------------------------";
#print "Total";               
tiempo_req_arr=np.asarray(tiempo_req,np.float)
tiempo_min_arr=np.asarray(tiempo_min,np.float)

print "Total              ",       sum(tiempo_req_arr),"                ",      sum(tiempo_min_arr)

tiempo_req_arr3=np.asarray(tiempo_req3,np.float)
tiempo_min_arr3=np.asarray(tiempo_min3,np.float)

#print "here" ,tiempo_req_arr3,tiempo_min_arr3

if tiempo_req_arr3.size:
    print "-------------------------------------------------------";
    print  "BAND 3 REQUESTED TIMES:";	
    for k in range (len(tiempo_req3)):
        print "Total                ",       tiempo_req3[k],"                ",      tiempo_min3[k]
    print "-------------------------------------------------------";
else:
    print "-------------------------------------------------------";
    print  "BAND 3 NOT REQUESTED";	



print  "============================================================ \n";
print  "DETAILED ASSESSMENT ";

print  "Is the RA/Dec appropriate for the semester & instrument? \n";  
print  "(Check http://www.gemini.edu/node/11950 )";

print  "------------------------------------------------------------ ";

print  "Is the instrument configuration appropriate to get the desired data? \n";
print  "(Component availability, resolution requirements, field-of-view, \n";
print  "readout mode, AO setup, mid-IR chop & nod.) ";

print  "------------------------------------------------------------ ";

print  "Will the exposure time reach the desired S/N? ";

print  "------------------------------------------------------------ ";

print  "Is the requested time correct? Have overheads & auxiliary \n";
print  "observations been correctly included? \n";
print  "(Acquisition, offsets, pre-imaging, sky frames, detector readout, & \n";
print  "non-baseline calibrations.) ";

print  "------------------------------------------------------------ ";

print  "Are there viable guide stars in the requested observing \n";
print  "conditions? ";

print  "------------------------------------------------------------ ";

print  "Are the specified observing conditions appropriate?  \n";
print  "If not, why? \n";
print  "[Please ensure you update the .xml file with any changed conditions.] ";

print  "------------------------------------------------------------ ";

print  "Has the PI specified particular airmass constraints in the proposal? \n";
print  "If so, are they justified? ";

print  "------------------------------------------------------------ ";

print  "Are any of the observations time-critical or requesting unusual \n";
print  "observing modes? ";

print  "------------------------------------------------------------ ";

print  "If Band 3 consideration is indicated, are the specified observations \n";
print  "feasible? Have the Band 3 observing conditions been set correctly? ";

print  "------------------------------------------------------------ ";

print  "Are the Band 3 total and minimum requested times appropriate in such \n";
print  "conditions? ";

print  "------------------------------------------------------------ ";

print  "What was the outcome of the duplication check? ";

print  "------------------------------------------------------------ ";

print  "If this is a classical time request, has a backup program been \n";
print  "specified? Is the backup program viable? Have secondary observing \n";
print  "constraints been specified for the backup program? ";

print  "------------------------------------------------------------ ";

print  "Additional Notes (eg. Iteration with PI, longer summary, etc) \n";
print  "[Optional] ";

print  "============================================================ \n";
print  "TECHNICAL FEEDBACK TO THE PI \n";
print  "[Optional] ";

print  "============================================================ \n";
sys.stdout.close()                          # closing the file
sys.stdout=temp                   
