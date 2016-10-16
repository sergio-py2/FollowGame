
import math

import pyglet

import xsect
import timevars as tv

from gameassets import GameAssets


class Zombie(object):
    """docstring for Zombie"""
    ST_CHASING, ST_FALLING, ST_DONE = 1, 2, 3
    def __init__(self, posX, posY):
        super(Zombie, self).__init__()
        ga = GameAssets.Instance()
        self.sprite = pyglet.sprite.Sprite(ga.getImage('zom'))
        self.posX = posX
        self.posY = posY
        self.radius = ga.getImage('zom').width / 2
        self.maxDamage = 20 #points per second

        self.zombieSpeedCurve = tv.PLInterpolator([(0, 230), (250, 95),
            (500,95), (750, 80), (800, 15), (3000, 10)])

        self.status = Zombie.ST_CHASING

    def update(self, dt, famPosition, walls):
        mv = self.getDesiredMove(dt, famPosition)
        move = xsect.Move((self.posX, self.posY), (self.posX + mv[0], self.posY + mv[1]))
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


    def getDesiredMove(self, dt, famPosition):
        dx = famPosition[0] - self.posX
        dy = famPosition[1] - self.posY

        r = math.sqrt(dx * dx + dy *dy)

        if r < 1.0:
            return (0.0, 0.0)

        if r > 0:
            dx /= r
            dy /= r

        '''if r < 300.0:
            speed = 120.0

        elif r < 700.0:
            speed = 85.0

        else:
            speed = 5.0'''

        speed = self.zombieSpeedCurve(r)

        dtravel = speed * dt
        if dtravel > r:
            dtravel = r

        return (dtravel * dx, dtravel * dy)


    def draw(self):
        self.sprite.x = self.posX
        self.sprite.y = self.posY
        if self.status == Zombie.ST_CHASING:
            self.sprite.draw()
        elif self.status == Zombie.ST_FALLING:
            pass
        elif self.status == Zombie.ST_DONE:
            pass
        else:
            print("unrecognized zombie status")

    def getPosition(self):
        return (self.posX, self.posY)

    def computeDamage(self, famPosition, famRadius):
        dx = self.posX - famPosition[0]
        dy = self.posY - famPosition[1]

        dist = math.sqrt(dx * dx + dy * dy)
        hit = dist / (famRadius + self.radius)

        if hit > 1:
            return 0.0
        return (1 - hit) * self.maxDamage
