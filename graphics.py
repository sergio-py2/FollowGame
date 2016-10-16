import pyglet

def tileRegion(batch, spritelist, image, xRange, yRange):
    # adds required tiles to batch
    # returns list of tiles created
    tileList = []

    x = xRange[0]
    while x < xRange[1]:

        y = yRange[0]
        while y < yRange[1]:
            w = min(image.width, xRange[1] - x)
            h = min(image.height, yRange[1] - y)

            if w < image.width or h < image.height:
                usableImg = image.get_region(x=0, y=0, width=w, height=h)
            else:
                usableImg = image

            sp = pyglet.sprite.Sprite(usableImg, x, y, batch=batch)
            tileList.append(sp)

            #print(w, h, x, y)
            
            # Always save a copy to stop rogue garbage collection
            spritelist.append(sp) 

            y += image.height

        x += image.width

    return tileList
