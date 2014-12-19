#!/usr/bin/python

import sys
from PIL import Image, ExifTags
img = Image.open(sys.argv[1])
data = {
    ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in ExifTags.TAGS
}

print data


# print "Shot:", img.