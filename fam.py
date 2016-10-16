
import math

import pyglet
import pyglet.window.key as key

import xsect
import timevars as tv

from gameassets import GameAssets
import config


class Fam(object):
    """docstring for Fam"""
    def __init__(self, posX, posY):
        super(Fam, self).__init__()
        ga = GameAssets.Instance()
        self.sprite = pyglet.sprite.Sprite(ga.getImage('fam'))
        self.posX = posX
        self.posY = posY
        self.radius = ga.getImage('fam').width / 2
        self.strength = 100
        self.targetPosition = (0, 0)
        self.targetVelocityFollower = tv.Follower2D()
        self.targetVelocityFollower.setDecayRate(0.95, 0.3, config.Config.Instance().getUpdateFPS())
        self.targetSprite = pyglet.sprite.Sprite(ga.getImage('target'))
        self.maxSpeed = 130.0
        self.health = 100


    def update(self, dt, userInput, walls):
        self.targetPosition = userInput.mousePosition
        start, end = self.getDesiredMoveTargetedVelocity(dt, userInput)
        #move = xsect.Move((self.posX, self.posY), (self.posX + mv[0], self.posY + mv[1]))
        move = xsect.Move(start, end)
        hits = xsect.disc_move_x_polygon_list(self.radius, move, walls)
        if not hits:
            self.posX = move.endPoint[0]
            self.posY = move.endPoint[1]
            return
        #there was a hit
        hit = hits[0]
        tailMove = move.submove(hit.moveParameter - 0.00001, 1.0)
        moveMod, _ = xsect.bounceMoveOffHit(tailMove, hit, rebound = 0.0)
        #print(type(moveMod))
        self.posX = moveMod.endPoint[0]
        self.posY = moveMod.endPoint[1]

        '''print("hit")
        print(hit.moveParameter)
        print(end)'''

    def getDesiredMoveXXX(self, dt, keys):
        speed = 100.0

        if keys[key.R]:
            speed = 500.0

        dx, dy = 0.0, 0.0

        if keys[key.LEFT]:
            dx = -1.0

        if keys[key.RIGHT]:
            dx = 1.0
        
        if keys[key.UP]:
            dy = 1.0

        if keys[key.DOWN]:
            dy = -1.0


        r = math.sqrt(dx * dx + dy *dy)

        if r > 0:
            dx /= r
            dy /= r

        return(dt * speed * dx, dt * speed * dy)

    def getDesiredMoveTargetedVelocity(self, dt, userInput):
        start = (self.posX, self.posY)

        speed = 0.70 * self.maxSpeed
        keys = userInput.keys
        if keys[key.R]:
            speed = 3.04 * self.maxSpeed


        t = xsect.vecMinus(self.targetPosition, start)
        targetDir, targetDistance = xsect.polarizeVector(t)
        self.targetVelocityFollower.setTarget( 
            (speed*targetDir[0], speed*targetDir[1]) )

        self.targetVelocityFollower.update(dt)
        velocity = self.targetVelocityFollower.getValue()

        end = (self.posX + dt*velocity[0], self.posY + dt*velocity[1])

        return start, end

    def draw(self):
        self.sprite.x = self.posX
        self.sprite.y = self.posY
        self.sprite.draw()

        self.targetSprite.x = self.targetPosition[0]
        self.targetSprite.y = self.targetPosition[1]
        self.targetSprite.draw()

    def getPosition(self):
        return (self.posX, self.posY)

    def getHealth(self):
        return self.health

    def adjustHealth(self, delta):
        self.health += delta
        self.health = tv.clamp(0, self.health, 100)

    def getRadius(self):
        return self.radius
