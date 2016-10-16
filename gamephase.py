#!python  -u

import math

import pickle
import copy
import random

import pyglet
import pyglet.gl as gl
import pyglet.window.key as key

import timevars as tv
import graphics
import xsect
import config

import gameelements
from gameassets import GameAssets
import healthbar

from zombie import Zombie
from fam import Fam

class GamePhase(object):
    """ Abstract base class for one phase of a game."""
    def __init__(self,  gameElements, windowProps, evtSrc):
        super(GamePhase, self).__init__()
        # You can create all the objects you need for this game phase

    def start(self):
        # Called when game phase becomes active
        pass

    def update(self, dt, userInput):
        # Called every game-tick when active
        # Returns:
        #    Either 'None' to indicate that this phase is still active,
        #    or an instance of the next Game Phase.
        #    This implements our state machine!
        pass        

    def draw(self, window):
        # Called every draw-tick when active. 
        # Make OpenGL calls here, but leave the stack the way you found it.
        pass        

    def delete(self):
        # Called after update returns next Game Phase.
        # A chance to free up resources (OpenGL stuff?)
        pass        




class Hole(object):
    """docstring for Hole"""
    def __init__(self, posX, posY):
        super(Hole, self).__init__()
        ga = GameAssets.Instance()
        self.image = ga.getImage('hole')
        self.sprite = pyglet.sprite.Sprite(self.image)
        self.posX = posX
        self.posY = posY

    def update(self, dt):
        pass

    def draw(self):
        self.sprite.x = self.posX
        self.sprite.y = self.posY
        self.sprite.draw()

    def containsPoint(self, position):
        rx = self.image.width / 2.0
        ry = self.image.height / 2.0
        dx = (position[0] - self.posX) / rx
        dy = (position[1] - self.posY) / ry
        return (dx * dx + dy * dy) < 1.0




class ChasePhase(GamePhase):
    def __init__(self, windowProps, evtSrc):
        #super(GamePhase, self).__init__()
        self.windowProps = windowProps
        self.evtSrc = evtSrc
        self.wallPolygons = xsect.PolygonList()

        #print vars(windowProps)

        self.gameElements = gameelements.GameElements(windowProps)
        self.gameElements.populateGame( GameAssets.Instance() )


        ga = GameAssets.Instance()

        #Make tiled background
        self.grassBatch = pyglet.graphics.Batch()
        #spritelist is to prevent garbage collection
        self.spritelist = []

        graphics.tileRegion(self.grassBatch, self.spritelist, ga.getImage('background'),
            (0, windowProps.windowWidth), (0, windowProps.windowHeight))

        #create walls
        self.wallImgBatch = pyglet.graphics.Batch()

        self.addWall( (200,250), (100,400))
        self.addWall( (600,650), (100,350))


        self.zombies = [Zombie(random.randint(500, 850), random.randint(100, 300)) for i in range(0,4)]
        self.holes = [Hole(random.randint(250, 1800), random.randint(250, 850)) for i in range (0, 3)]
        self.fam = Fam(100, 100)

        w, h = windowProps.windowWidth, windowProps.windowHeight
        self.wallPolygons.add(xsect.Polygon((0,0),(w,0)))
        self.wallPolygons.add(xsect.Polygon((w,0),(w,h)))
        self.wallPolygons.add(xsect.Polygon((w,h),(0,h)))
        self.wallPolygons.add(xsect.Polygon((0,h),(0,0)))

        self.healthBar = healthbar.HealthBar(100, 100)

    def addWall(self, xRange, yRange):
        brk = GameAssets.Instance().getImage('wall')
        graphics.tileRegion(self.wallImgBatch, self.spritelist, brk, xRange, yRange)

        x0,x1 = xRange
        y0,y1 = yRange

        p = xsect.Polygon(
            (x0,y0),
            (x1,y0),
            (x1,y1),
            (x0,y1)
            )

        self.wallPolygons.add(p)

    def start(self):
        pass


    def update(self, dt, userInput):
        for zombie in self.zombies:
            if zombie.status == zombie.ST_DONE:
                continue
            zombie.update(dt, self.fam.getPosition(), self.wallPolygons)
        self.fam.update(dt, userInput, self.wallPolygons)

        #check holes
        for zombie in self.zombies:
            if self.fellInHole(zombie.getPosition()):
                zombie.status = Zombie.ST_DONE

        if self.fellInHole(self.fam.getPosition()):
            raise Exception ("You were a mega spoon")


        if userInput.keys[key.P]:
            self.fam.adjustHealth(-1)
        if userInput.keys[key.O]:
            self.fam.adjustHealth(+1)

        totalDamage = 0
        for zombie in self.zombies:
            if zombie.status == zombie.ST_CHASING:
                totalDamage += zombie.computeDamage(self.fam.getPosition(), self.fam.getRadius())

        self.fam.adjustHealth(-totalDamage * dt)

        self.healthBar.setValue(self.fam.getHealth())

    def draw(self, window):
        ga = GameAssets.Instance()
        self.grassBatch.draw()

        self.wallImgBatch.draw()

        for hole in self.holes:
            hole.draw()
        self.fam.draw()
        for zombie in self.zombies:
            zombie.draw()


        gl.glPushMatrix()
        gl.glTranslatef( 100, 100, 0 )
        
        self.healthBar.draw()

        gl.glPopMatrix()


    def fellInHole(self, position):
        for hole in self.holes:
            if hole.containsPoint(position):
                return hole

        return None






