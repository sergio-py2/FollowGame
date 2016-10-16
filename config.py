#!python -u

from singleton import Singleton

@Singleton
class Config(object):
    """ Configuration file. """

    def __init__(self):
        #super(GameAssets, self).__init__()
        pass

    def getUpdateFPS(self):
        return 60.0

    def getDrawFPS(self):
        return 60.0

