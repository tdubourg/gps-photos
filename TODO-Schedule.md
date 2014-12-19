## TODO / Schedule

### Map with images displayed at their geotagged location

- Loop through images and index them by reading their EXIF data - DONE
- Generate thumbnails - DONE (TODO: change their size?)
- Register thumbnails location for every image - DONE
- Load this data from JS - DONE
- Use GG Maps API in order to display dots and thumbnails of images at their geotagged location - DONE: But changing the size
of the thumbnails could help


### Use time-neighboring photos in order to suggest location to non-geotagged photos (typically, digital cameras)

- Index photos in a data structure that allows to do closest neighbors search. If we convert dates into timestamps, a simple 
sorted array might do the trick? To be researched...
- For every photo that has no GPS tags, search the closest neigHbor in time (/!\ CONVERT EVERYTHING TO THE SAME TIMEZONE (
Greenwich, for instance) IN ORDER FOR PHOTOS TAKENS AT 1PM IN CET+1 TO BE CONSIDERED NEIGHBORS PHOTOS TAKEN AT 2PM IN CET+2).
- Apply the tag of the closest photo to the non tagged photo, if less than a given threshold of time. 


### Refine the method

Analyze sequences of photos: 
- 10 photos taken at 1h interval in a given geo area and then a photo taken 4 hours later 
without a location is likely to have been taken in a place not too far away from the previous ones
- If photos are taken every one day only, then all photos taken on the same day are likely to be taken in a similar area, but
photos taken from different days may be from totally different places:
    - If photos show a big difference in location between days, then a lonely photo on another day might be totally 
    different... ? Who knows?!?!
