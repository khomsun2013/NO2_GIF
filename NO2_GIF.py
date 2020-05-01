# python NO2_GIF.py
#
# Note: modify dataDir to your current folder
#       downloand nc file from https://s5phub.copernicus.eu/dhus/#/home
#
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import glob
import netCDF4 as nc4
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

dataDir = '/Users/Khomsun/Downloads/' 
m=0
names=[]
files = glob.glob(dataDir+'*.nc')
output = 'NO2_Project.gif'
for f in files:
	datafile = nc4.Dataset(f,'r')
	lat = np.array(datafile.groups['PRODUCT']['latitude'][:])
	lon = np.array(datafile.groups['PRODUCT']['longitude'][:])
	no2 = np.array(datafile.groups['PRODUCT']['nitrogendioxide_tropospheric_column'][:])
	no2max = np.max(no2[:])
	no2min = np.min(no2[:])
	view_lat = lat[np.logical_and(no2 >= no2min, no2 < no2max)]
	view_lon = lon[np.logical_and(no2 >= no2min, no2 < no2max)]
	my_dpi = 96 
	w = 1920
	h = 1080
	print(len(view_lon))
	plt.figure(figsize=(w/my_dpi, h/my_dpi), dpi=my_dpi)
	#map = Basemap(projection='cyl', llcrnrlon=-68,llcrnrlat=-19.155622,urcrnrlon=80,urcrnrlat=19.253133,resolution='i')
	map = Basemap(projection='cyl',resolution='i')
	x, y = map(view_lon, view_lat)
	map.plot(x, y, 'o', markersize=1,color='grey',alpha=0.01)
	#map.etopo()
	map.drawcoastlines(color='black')
	map.drawcountries(color='black')
	plt.savefig('img{:02d}.png'.format(m), bbox_inches='tight',dpi=my_dpi)
	names.append('img{:02d}.png'.format(m))
	m+=1
images = [Image.open(fn) for fn in names]
images[0].save(output,save_all=True,append_images=images[1:],duration=500,loop=0)
for f in glob.glob("img*.png"):
	os.remove(f)
