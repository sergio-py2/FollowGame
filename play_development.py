#!python
#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7-32 -u


from __future__ import division

import sys

import follow_game

if len(sys.argv) > 1 and sys.argv[1] == '-f':
    windowOpts = {'fullscreen': True}
else:
    windowOpts = {'width': 1200, 'height': 600}

follow_game.play(windowOpts)