#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7-32

from __future__ import division

#import os
import sys

import pyglet
import pyglet.gl as gl

import pyglet.window.key as key


import gamephase
import gameelements

from gameassets import GameAssets

import config



# Objects that just hold a bunch of attributes
class Attributes(object):
    pass

# Define the application class

class Application(object):
    """
    Application maybe with multiple windows. Should be a Singleton.
    Does little for now but it's where communication between / coordination
    of multiple windows would happen.
    """
    def __init__(self, windowOpts):
        super(Application, self).__init__()

        js = None
            

        #windowOpts = {'width': 1200, 'height': 500}
        #windowOpts = {'fullscreen': True}

        self.window = GameWindow(js, **windowOpts)

    def update(self, dt):
        self.window.update(dt)

class WindowProps(object):
    """Properties of a GameWindow, suitable for passing around without
        passing the full window."""
    
    def __init__(self):
        pass

class GameWindow(pyglet.window.Window):
    """A single window with a game taking place inside it"""
    
    def __init__(self, joystick, **kwargs):
        # These might not do anything here.
        #gl.glClearColor(0.0, 0.0, 0.0, 0.0)
        #gl.glEnable( gl.GL_BLEND)
        #gl.glBlendFunc( gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        super(GameWindow, self).__init__(**kwargs)        
        
        if not self.fullscreen:
            self.set_location(20,35)

        self.set_vsync(True)
        self.set_mouse_visible(False)

        self.gameTime = 0.0

        props = WindowProps()
        props.windowWidth     = self.width
        props.windowHeight    = self.height
        self.props = props

        self.userInput = Attributes()

        self.userInput.joystick = joystick
        self.userInput.keys = key.KeyStateHandler()
        self.userInput.mousePosition = (0, 0)
        self.push_handlers(self.userInput.keys)

        self.gamePhase = gamephase.ChasePhase( props, self )
        #self.gamePhase = gamephase.PlayTimePhase( props, self )
        #self.gamePhase = gamephase.LeaderBoardPhase( props, self, (1,2,3) )
        #s = random.randint(5,500)
        #self.gamePhase = gamephase.LeaderBoardPhase(props, self, (None, 'MA', s))

        self.gamePhase.start()


        # I think extending Window automatically has this as a handler
        #self.push_handlers(self.on_key_press)

    def on_mouse_motion(self, x, y, dx, dy):
        #print "on_mouse_motion", x, y, dx, dy
        self.userInput.mousePosition = (x,y)

    def on_key_pressXXX(self, symbol, modifiers):
        pass
        #print "GameWindow.on_key_press", symbol
        #if self.keys[key.Q]:
            #print "State is %s" % gGeoData.get('state', 'unknown')
        #    pyglet.app.exit()        
    

    # --------------------------------------------
    #     Most of the game logic goes here
    # --------------------------------------------

    def update(self, dt):
        # Ctrl-Q always lets you abort.
        k = self.userInput.keys
        if k[key.Q] and (k[key.LCTRL] or k[key.RCTRL]):
            pyglet.app.exit()        

        self.gameTime += dt
        
        gp = self.gamePhase.update(dt, self.userInput)

        if gp is None:
            return

        # Switch to new game phase
        self.gamePhase.delete()
        gp.start()

        self.gamePhase = gp

            
    def on_draw(self):
        gl.glEnable (gl.GL_BLEND)
        gl.glEnable (gl.GL_LINE_SMOOTH)
        gl.glHint (gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE)
        self.clear()
        self.gamePhase.draw(self)




def play(windowOpts):
    ga = GameAssets.Instance()
    ga.loadAssets()

    app = Application(windowOpts)


    pyglet.clock.set_fps_limit(config.Config.Instance().getDrawFPS())
    #pyglet.clock.schedule_interval(update, 1/60.)
    pyglet.clock.schedule_interval(app.update, 1/config.Config.Instance().getUpdateFPS())

    pyglet.app.run()


if __name__ == '__main__':
    main()

