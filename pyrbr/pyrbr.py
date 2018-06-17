import datetime
import pytz
import numpy
import logging
import sys
import argparse
import pkg_resources
import yaml
import codecs
import numpy as np

# Get the version
version_file = pkg_resources.resource_filename('pycnv','VERSION')

with open(version_file) as version_f:
   version = version_f.read().strip()


# Setup logging module
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logger = logging.getLogger('pyrbr')


class pyrbr():
    """A RBR parsing object

    Author: Peter Holtermann (peter.holtermann@io-warnemuende.de)

    Usage:
       >>>filename='test.txt'
       >>>rbr = pyrbr(filename)

    Args:
       filename: The name of the datafile
       verbosity: 
       timezone: The timezone the time data is saved in

    """
    
    def __init__(self,filename,encoding='windows-1253',verbosity=logging.DEBUG,timezone=pytz.UTC):
        """
        """
        logger.setLevel(verbosity)
        logger.info(' Opening file: ' + filename)
        
        self.filename = filename
        self.timezone = timezone
        data = self.read_rbr(filename,encoding=encoding)
        self.data = data

    def read_rbr(self,fname,encoding='windows-1253'):
        print('Opening ' + str(fname))
        f = codecs.open(fname, "r", encoding = encoding)
        i = 0
        data = {}
        FLAG_DATA = False
        for li in f:
            i += 1
            #print(i)
            l = " ".join(li.split()).replace('\n','').replace('\r','')
            #print(l)        
            if(len(l) > 0):
                if(FLAG_DATA):
                    if(len(l) > 2):
                        #03-Mar-2018 15:00:08.000
                        tstr = l.split(" ")[0] + ' ' + l.split(" ")[1]

                        try:
                            date_tmp = datetime.datetime.strptime(tstr,"%d-%b-%Y %H:%M:%S.%f")
                        except:
                            date_tmp = datetime.datetime.strptime(tstr,"%Y-%m-%d %H:%M:%S.%f")

                            
                        data['t'].append(date_tmp.replace(tzinfo=self.timezone))
                        for fi in range(2,len(data['fields'])):
                            fl = data['fields'][fi]
                            dstr = l.split(" ")[fi]
                            Ttmp = float(dstr)                                            
                            data[fl].append(Ttmp)

                        #print(date_tmp,Ttmp)
                    else:
                        print('No more data ...')
                        break
                else:
                    if('Firmware' in l):
                        data['firmware'] = l.split('=')[1].replace('\n','').replace('\r','')
                    if('Serial' in l):
                        data['serial'] = l.split('=')[1].replace('\n','').replace('\r','')

                    if('Date & Time' in l):
                        data['fields'] = ['Date','Time']
                        data['fields'].extend(l.split(" ")[3:])
                        for fi in range(2,len(data['fields'])):
                            fl = data['fields'][fi]                        
                            data[fl] = []

                        data['t'] = []                        
                        FLAG_DATA = True


                #if(i == 40):
                #    break


        data['t'] = np.asarray(data['t'])
        #data['tn'] = pl.date2num(data['t'])
        for fi in range(2,len(data['fields'])):
            fl = data['fields'][fi]
            data[fl] = np.asarray(data[fl])        


        return data
