#!python -u

from singleton import Singleton
import math

import pyglet

@Singleton
class GameAssets(object):
    """ Loads images, sounds, etc. from files and holds them as pyglet-compatible
        objects. """

    def __init__(self):
        #super(GameAssets, self).__init__()
        pass

    def loadAssets(self):
        self.images = {}
        self.sounds = {}

        self.loadStdImage('fam.png', 'fam')
        self.loadStdImage('notfam.jpg', 'zom')
        self.loadStdImage('hole-trimmed.png', 'hole')
        self.loadStdImage('wall.png', 'wall')
        self.loadStdImage('target-32.png', 'target')
        i = self.loadStdImage('scaled-tile-grass.png', 'background')
        i.anchor_x = 0
        i.anchor_y = 0

    def loadStdSound(self, fileName, tag):
        s = pyglet.resource.media(fileName)
        self.sounds[tag] = pyglet.media.StaticSource(s)
        return s

    def getSound(self, tag):
        return self.sounds[tag]


    def loadStdImage(self, fileName, tag):
        # Loads the image and puts the anchor in the center.
        # You can re-set the center if that default isn't right.
        img = pyglet.resource.image("resources/" + fileName)
        img.anchor_x = img.width//2
        img.anchor_y = img.height//2
        self.images[tag] = img
        return img

    def getImage(self, tag):
        return self.images[tag]
