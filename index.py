#!/usr/bin/python

"""
    /!\/!\/!\/!\ THE DB FILE WILL BE OVERWRITTEN /!\/!\/!\/!\/!\
    This file takes as arguments: a folder to be indexed and a "DB" file to be used to store the results in.

    It will then look for image files (*.jpg and *.JPEG (case insensitive) only for now), try to extract geotags from
    exif data using pexif python module.

    Then index things away (see todo for more details?)
"""

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

ALLOWED_EXTENSIONS = ["jpg", "  jpeg"]

def main(argv):
    import csv, pexif
    from glob import glob
    import os

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

    ### Step 2: Go through all images files in the folder, for each image, try to find geo data ###

    images = []

    for ext in ALLOWED_EXTENSIONS:
        log("Currently dealing with ext:", ext)
        # Note: Here, we are assuming usage a *real* filesystem, that is to say case-sensitive
        # If using Mac or Windows filesystems, just deal with your ***** yourself...
        pattern = os.path.join(folder, "*." + ext.lower())
        log("Currently globbing with pattern:", ext)
        images.extend(glob(pattern))
        
        pattern = os.path.join(folder, "*." + ext.upper())
        log("Currently globbing with pattern:", ext)
        images.extend(glob(pattern))

    log("Image paths found:", images)

    images_with_geo = []
    for fname in images:
        with open(fname, 'r') as fi:
            i = pexif.JpegFile.fromFd(fi)
            try:
                print i.get_geo()
                images_with_geo.append(i)
            except Exception:
                print fname, "has no GEO info"


    ### Step 3: For every image with geo data, register it in a CSV file (we do not need a DB, CSV is more readable...) ###

    ### Step 4: For every image, create a thumbnail in the specified folder, to be used by the web UI:


if __name__ == '__main__':
    import sys
    main(sys.argv)