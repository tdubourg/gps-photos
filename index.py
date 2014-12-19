#!/usr/bin/python

"""
    /!\/!\/!\/!\ THE DB FILE WILL BE OVERWRITTEN /!\/!\/!\/!\/!\
    This file takes as arguments: a folder to be indexed and a "DB" file to be used to store the results in.

    It will then look for image files (*.jpg and *.JPEG (case insensitive) only for now), try to extract geotags from
    exif data using pexif python module.

    Then index things away (see todo for more details?)
"""

# Those modules are not necessarily installed on the machine so we import them as early as possible in order to avoid
# having the program crash because of missing dependencies only when it executes the function, but rather as soon as
# it imports the current file/module

from PIL import Image
import csv, pexif
from multiprocessing import cpu_count

# And this module is used in several functions so we import it once for all
import os

DBG = True

def log(*args):
    if DBG:
        for s in args:
            print s,
        print ""

CLI_ARGS = [
    "path_to_folder_to_index",
    "path_to_db.csv"
]

ALLOWED_EXTENSIONS      = ["jpg", "  jpeg"]

POOL_SIZE               = cpu_count() * 3 / 2
DATA_SET_SIZE           = None
BATCH_SIZE              = None
WORKERS_SORT_OF_QUEUE   = None
THUMBNAIL_SIZE          = 128, 128
THUMBNAIL_FOLDER        = "./ui/thumbs/"  # TODO change that

def thumbnail_worker(start_val):
    for x in WORKERS_SORT_OF_QUEUE[start_val:start_val + BATCH_SIZE]:
        log("Processing image", x, "for thumbnailing...")
        
        im = Image.open(x[0])
        im.thumbnail(THUMBNAIL_SIZE)
        im.save(x[1])
        log("Finished", x)
    return True

def thumbnail_path(fpath):
    image_fname = os.path.basename(fpath)
    return os.path.join(THUMBNAIL_FOLDER, image_fname)

def main(argv):
    from glob import glob
    from multiprocessing import Pool
    from time import time

    ##### Step 1: Get CLI arguments? #####

    argc = len(argv)
    if argc <= len(CLI_ARGS):
        print "Usage: %s"  % argv[0], ' '.join(CLI_ARGS)
        print "Currently missing parameters arguments:", ' '.join(CLI_ARGS[len(argv)-1:])
        exit()

    folder      = os.path.abspath(argv[1])
    log("Argument folder passed:", argv[1])
    log("Folder extracted:", folder)
    if not os.path.isdir(folder):
        print "Invalid folder, please retry."
    db_fname    = argv[2]

    db_f = open(db_fname, "w+")
    db_w = csv.writer(db_f)
    ## /!\/!\ CHECK WHETHER IT IS long, lat OR lat, long /!\/!\ ##
    db_w.writerow(["file_original_location", "time", "lat", "long", "thumb_path"])

    ### Step 2: Go through all images files in the folder, for each image, try to find geo data ###

    images = []

    for ext in ALLOWED_EXTENSIONS:
        log("Currently dealing with ext:", ext)
        # Note: Here, we are assuming usage a *real* filesystem, that is to say case-sensitive
        # If using Mac or Windows filesystems, just deal with your ***** yourself...
        pattern = os.path.join(folder, "*." + ext.lower())
        log("Currently globbing with pattern:", pattern)
        images.extend(glob(pattern))
        
        pattern = os.path.join(folder, "*." + ext.upper())
        log("Currently globbing with pattern:", pattern)
        images.extend(glob(pattern))

    log("Image paths found:", images)

    thumbs_to_be_generated = []
    for fname in images:
        with open(fname, 'r') as fi:
            i = pexif.JpegFile.fromFd(fi)
            try:
                geo = i.get_geo()
            except Exception:
                log(fname, "has no GEO info")
                continue  # Skip the rest, no geo data

            ### Step 3: For every image with geo data, register it in a CSV file (we do not need a DB, CSV is more readable...) ###
            thumb_path = thumbnail_path(fname)
            db_w.writerow([
                fname,
                -1, # TODO
                geo[0],
                geo[1],
                thumb_path,
            ])
            thumbs_to_be_generated.append((fname, thumb_path))

    ### Step 4: For every image, create a thumbnail in the specified folder, to be used by the web UI:
    # TODO: To be handled by a forked process (danger: forkbomb if many images?)
    # Should we fork a unique process and... Hey, wait, the Multiprocessing module is made for that
    # just allocate a pool of CPU * 1.5 workers, feed them with stuff to do, wait for termination! 
    global DATA_SET_SIZE, BATCH_SIZE, WORKERS_SORT_OF_QUEUE
    WORKERS_SORT_OF_QUEUE = thumbs_to_be_generated
    
    DATA_SET_SIZE = len(WORKERS_SORT_OF_QUEUE)
    BATCH_SIZE = DATA_SET_SIZE / POOL_SIZE
    if BATCH_SIZE is 0:
        BATCH_SIZE = 1
    
    log("Generating workers pool...")
    p = Pool(processes=POOL_SIZE)
    start_values = range(0, DATA_SET_SIZE, BATCH_SIZE)
    log("Start values:", start_values)
    t0 = time()
    p.map(thumbnail_worker, start_values)
    p.close()
    p.join()
    log("Workers finished in %.3f." % (time()-t0))


if __name__ == '__main__':
    import sys
    main(sys.argv)