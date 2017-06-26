import re
import sys
import pandas as pd
import math
import Image, ImageDraw, ImageFont, ImageFilter

width = 3000 
height = 3000

image = Image.new('RGB', (width, height), (0,0,0))
draw = ImageDraw.Draw(image)

print "read file\n"
df1 = pd.read_csv("./data/predPaths_test.txt", header=None, names=["pathid","taxi_id","lat","lon","busy","dtime"])

i=0

for row in df1.itertuples(index=False):
    x=row[3]
    y=row[2]

    xmin=103.45
    ymin=30.19
    k=3000/0.92
    draw.point(((x-xmin)*k,height-(y-ymin)*k), fill=(255,255,0))

    if i%10000 == 0:
        sys.stdout.flush()
        sys.stdout.write("#")
    
i=i+1  

image.save('map_test.jpg', 'jpeg');

