import urllib2
from bs4 import BeautifulSoup
import os
import arcpy

resp = urllib2.urlopen( 'https://coast.noaa.gov/htdata/raster1/imagery/ORR_NY_NJ_2014_6203/' )
soup = BeautifulSoup( resp.read() )
links = soup.find_all( 'a' )  #p is an array of all hyperlink tags

for link in links: # Processing each link and getting the url value
    url = link.get( 'href' ) 
    if url.startswith('NewYork/UTM18_ImageTiles/'):
        fName = url.split('UTM18_ImageTiles/',1)[1]
        url = r'https://coast.noaa.gov/htdata/raster1/imagery/ORR_NY_NJ_2014_6203/' + url
        f = urllib2.urlopen(url)
        data = f.read()
        
        output = os.path.join('D:\NOAA\Ortho', fName)
        with open(output, "wb") as code:
            code.write(data)
            print str(url) + " saved"
'''
after download .tif raster steps below
'''            
rasterList = []
walk = arcpy.da.Walk('D:\NOAA\Ortho', topdown=True)  

for subdir, dirs, files in walk:
    for filename in files:
        fullpath = os.path.join(subdir, filename)
        basename, extension = os.path.splitext(fullpath)
        if extension.lower() == ".tif":
            rasterList.append(fullpath)
        
print rasterList

arcpy.MosaicToNewRaster_management(rasterList, 'C:\Users\m_downin\Desktop\NOAA\Raster\NYC.gdb', 'Pypy','','','',3)