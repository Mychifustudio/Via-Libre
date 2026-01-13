from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties
from panda3d.core import load_prc_file_data
from panda3d.core import DirectionalLight
# from direct.gui.OnscreenImage import OnscreenImage
# from panda3d.core import TransparencyAttrib

from panda3d.core import CardMaker, PNMImage, Texture
import random
from panda3d.core import AntialiasAttrib

from vialibre.player import Player

load_prc_file_data('', 'sync-video f\nshow-frame-rate-meter t')
load_prc_file_data('','win-size 1280 720')
load_prc_file_data('', 'client-sleep 0.001')
load_prc_file_data('', 'framebuffer-multisample 1\nmultisamples 2')

class Test(ShowBase):
    def __init__(self, fStartDirect=True, windowType=None):
        super().__init__(fStartDirect, windowType)

        self.render.setAntialias(AntialiasAttrib.MMultisample)

        self.disable_mouse()

        self.player = Player()

        props = WindowProperties()
        props.setCursorHidden(True)
        self.win.requestProperties(props)

        self.accept("escape", self.userExit)

        self.generateGround()

        self.smooth_dt = None

        self.setupLights()

        self.taskMgr.add(self.update, 'update')

    def smoothDt(self, dt):
        if self.smooth_dt is None:
            self.smooth_dt = dt
        else:
            self.smooth_dt += (dt - self.smooth_dt) * 0.05
        return self.smooth_dt

    def update(self, task):
        # dt = self.smoothDt(globalClock.getDt())
        dt = globalClock.getDt() # pyright: ignore[reportUndefinedVariable]

        self.player.update(dt)

        return task.cont

    def generateGround(self):
        size = 256  # texture resolution
        img = PNMImage(size, size)

        for x in range(size):
            for y in range(size):

                r = 0.25 + random.uniform(-0.05, 0.05)
                g = 0.7  + random.uniform(-0.1, 0.1)
                b = 0.25 + random.uniform(-0.05, 0.05)

                r = min(max(r, 0), 1)
                g = min(max(g, 0), 1)
                b = min(max(b, 0), 1)

                img.setXel(x, y, r, g, b)

        texture = Texture("groundTexture")
        texture.load(img)
        texture.setWrapU(Texture.WM_repeat)
        texture.setWrapV(Texture.WM_repeat)

        cm = CardMaker("ground")
        cm.setFrame(-50, 50, -50, 50)
        cm.setUvRange((0, 0), (10, 10))

        ground = self.render.attachNewNode(cm.generate())
        ground.setP(-90)
        ground.setZ(0)
        ground.setTexture(texture)

    def setupLights(self):
        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

    # def setResolution(self):
    #     properties = WindowProperties()
    #     properties.setSize(self.pipe.getDisplayWidth(), self.pipe.getDisplayHeight())
    #     properties.setUndecorated(True)
    #     self.win.requestProperties(properties)

app = Test()
app.run()