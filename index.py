import csv, pexif

##### Step 1: Get CLI arguments? #####

images = []

### Step 2: Go through all images files in the folder, for each image, try to find geo data ###

images_with_geo = []
for fname in images:
    with pexif.JpegFile.fromFile(fname) as i:
        try:
            print i.get_geo()
            images_with_geo.append(i)
        except Exception as e:
            print fname, "has no GEO info"


### Step 3: For every image with geo data, register it in a CSV file (we do not need a DB, CSV is more readable...) ###

### Step 4: For every image, create a thumbnail in the specified folder, to be used by the web UI:
