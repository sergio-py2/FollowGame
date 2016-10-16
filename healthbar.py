#!python -u

import math
import colorsys

import pyglet
import pyglet.gl as gl

import timevars as tv

paaaaass = 0


class HealthBar(object):
    """bar that shows health/stamina"""
    def __init__(self, fullScale, currentValue):
        super(HealthBar, self).__init__()
        self.width = 50.0
        self.height = 800.0
        self.fullScale = fullScale
        self.currentValue = currentValue

        self.mainBar = None

        self.hueCurve = tv.PLInterpolator((
            (0,12), 
            (0.15 * fullScale, 12), 
            (0.20 * fullScale, 60),
            (0.35 * fullScale, 60),
            (0.40 * fullScale, 140),
            (fullScale,140)))


        self.lightnessCurve = tv.PLInterpolator((
            (0, 50),
            (0.20 * fullScale, 50),
            (0.33 * fullScale, 30),
            (fullScale, 30)
            ))      

        #needs to be last in constructor
        self.setValue(currentValue)  

    def setValue(self, value):
        if int(value) == self.currentValue and self.mainBar is not None:
            return

        self.currentValue = int(value)
        if self.currentValue < 0:
            self.currentValue = 0
        if self.currentValue > self.fullScale:
            self.currentValue = self.fullScale

        verts = []
        colors = []

        visibleNodes = [n for n in self.hueCurve.getNodes() if n < self.currentValue]
        visibleNodes.append(self.currentValue)

        for val in visibleNodes:
            hue = self.hueCurve(val)
            lightness = self.lightnessCurve(val)
            (red, green, blue) = colorsys.hls_to_rgb(hue/360.0, lightness/100.0, 1.0)

            y = float(val) / self.fullScale * self.height
            verts += [0, y, self.width, y]
            colors += [int(255*red),int(255*green),int(255*blue)] * 2

        if self.mainBar is not None:
            self.mainBar.delete()

        self.mainBar = pyglet.graphics.vertex_list(len(verts)//2,
            ('v2f', verts),
            ('c3B', colors)
            )

        textColor = colors[-3: ]
        textColor.append(255)
        self.label = pyglet.text.Label(str(self.currentValue),
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.width//2, y=float(self.currentValue) / self.fullScale * self.height,
                          anchor_x='center', anchor_y='bottom',
                          color=textColor)
    def draw(self):
        self.mainBar.draw(pyglet.gl.GL_QUAD_STRIP)
        self.label.draw()

    def update(self, dt, userInput):
        paaaaass