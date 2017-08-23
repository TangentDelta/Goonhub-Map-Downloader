from PIL import Image
from random import randint
import os.path
import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlretrieve

urlCogMap = ("http://goonhub.com/images/maps/cogmap/z1/","http://goonhub.com/images/maps/cogmap2/z3/")
urlDestiny = ("http://goonhub.com/images/maps/destiny/z1/","http://goonhub.com/images/maps/cogmap2/z3/")

for y in range(0,8):
	for x in range(0,8):
		print("Fetching "+str(x)+","+str(y))
		if not os.path.isfile("cogmap-"+str(x)+"-"+str(y)+"-1.png"):
			urlretrieve(urlCogMap[1-1]+str(y)+","+str(x)+".png","cogmap-"+str(x)+"-"+str(y)+"-1.png")
		if not os.path.isfile("cogmap-"+str(x)+"-"+str(y)+"-3.png"):
			urlretrieve(urlCogMap[2-1]+str(y)+","+str(x)+".png","cogmap-"+str(x)+"-"+str(y)+"-3.png")
		if not os.path.isfile("destiny-"+str(x)+"-"+str(y)+"-1.png"):
			urlretrieve(urlDestiny[1-1]+str(y)+","+str(x)+".png","destiny-"+str(x)+"-"+str(y)+"-1.png")
		if not os.path.isfile("destiny-"+str(x)+"-"+str(y)+"-3.png"):
			urlretrieve(urlDestiny[2-1]+str(y)+","+str(x)+".png","destiny-"+str(x)+"-"+str(y)+"-3.png")


spaceImg = Image.open("space.png")
spacePixels = spaceImg.load()





if os.path.isfile("spacemap.png"):
	print("Found space map. Loading in...")
	spaceMapImg = Image.open("spacemap.png")
	spaceMapPixels = spaceMapImg.load()
else:
	print("Generating space...")
	spaceMapImg = Image.new( 'RGBA', (8*1200,8*1200), (0,0,0,255))
	spaceMapPixels = spaceMapImg.load()
	for y in range(0,300):
		for x in range(0,300):
			spaceMapY = randint(0,6)
			spaceMapX = randint(0,10)
			for pixelY in range(0,32):
				for pixelX in range(0,32):
					spaceMapPixels[(x*32)+pixelX,(y*32)+pixelY]=spacePixels[pixelX+(spaceMapX*32),pixelY+(spaceMapY*32)]
	spaceMapImg.save("spacemap.png")

def stitchImage( mapName,levelZ,finalMapName ):
	print("Constructing map: "+finalMapName)
	img = spaceMapImg.copy()
	pixels = img.load()

	for y in range(0,8):
		for x in range(0,8):
			#print("Tiling "+str(x)+","+str(y))
			print("Opening: "+mapName+"-"+str(x)+"-"+str(y)+"-"+str(levelZ)+".png")
			tileImg = Image.open(mapName+"-"+str(x)+"-"+str(y)+"-"+str(levelZ)+".png")
			tilePixels = tileImg.load()
			for pixelY in range((1200*y),(1200*(y+1))):
				for pixelX in range((1200*x),(1200*(x+1))):
					#print(str(tilePixels[pixelX-(1200*x),pixelY-(1200*y)]))
					if tilePixels[pixelX-(1200*x),pixelY-(1200*y)][3] == 255:
						pixels[pixelX,pixelY] = tilePixels[pixelX-(1200*x),pixelY-(1200*y)]
	img.save(finalMapName)


stitchImage( "cogmap",1,"cogmap-1.png")
stitchImage( "cogmap",3,"cogmap-3.png")
stitchImage( "destiny",1,"destiny-1.png")
stitchImage( "destiny",3,"destiny-3.png")
#img.show()