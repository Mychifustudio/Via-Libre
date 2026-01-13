from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from vialibre.camera import Camera
from math import degrees, atan2

class Player(DirectObject):
    def __init__(self, showbase: ShowBase = None):
        self.base = showbase if showbase else base

        # ----- Setup Keys ----- #
        self.accept('raw-w', self.updateKeyMap, ['forward', True])
        self.accept('raw-w-up', self.updateKeyMap, ['forward', False])
        self.accept('raw-a', self.updateKeyMap, ['left', True])
        self.accept('raw-a-up', self.updateKeyMap, ['left', False])
        self.accept('raw-s', self.updateKeyMap, ['backward', True])
        self.accept('raw-s-up', self.updateKeyMap, ['backward', False])
        self.accept('raw-d', self.updateKeyMap, ['right', True])
        self.accept('raw-d-up', self.updateKeyMap, ['right', False])

        # ----- Setup KeyMap ----- #
        self.keyMap = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
        }

        # ----- Setup Player ----- #
        self.player = self.base.render.attachNewNode('player')

        self.modelNode = self.player.attachNewNode('player-model')
        
        self.model = self.base.loader.loadModel('./assets/dog.bam')
        self.model.setScale(self.model.getScale())
        self.model.reparentTo(self.modelNode)

        self.heading = 0

        # ----- Setup Camera ----- #
        self.camera = Camera(self.player)
        self.camera.setOffset(Vec3(0, -10, 10))
        self.camera.setP(-10)

        # ----- Setup Movements ----- #
        self.movementVector = Vec3(0)
        self.lastMovement = Vec3(0)
        self.playerSpeed = 10
        self.turnSpeed = 10.0 # Higher = snappier, lower = smoother

    def update(self, dt):
        forward = Vec3(0, 1, 0)
        right = Vec3(1, 0, 0)

        self.movementVector = Vec3(0)

        if self.keyMap['forward']:
            self.movementVector += forward
        if self.keyMap['backward']:
            self.movementVector -= forward
        if self.keyMap['right']:
            self.movementVector += right 
        if self.keyMap['left']:
            self.movementVector -= right

        self.movementVector.normalize()

        if self.movementVector.length() > self.lastMovement.length():
            self.modelNode.lookAt(self.modelNode.getPos() + self.movementVector)

        for axis in range(3):
            maxSpeedTime = .5 if self.movementVector[axis] else .08
            self.movementVector[axis] = self.camera.powLerp(self.lastMovement[axis], self.movementVector[axis], dt, maxSpeedTime)
        self.lastMovement = self.movementVector
        
        self.player.setPos(self.player.getPos() + self.movementVector * self.playerSpeed * dt)
        

        self.base.camera.lookAt(self.base.camera.getPos() - self.camera.cameraOffset)
        self.camera.setPos(self.camera.calculateCameraPos(dt, self.movementVector, self.lastMovement))
        self.camera.updateFov(dt, any(self.keyMap.values()))
        
        self.lastMovement = self.movementVector
    
    def updateKeyMap(self, key, value):
        self.keyMap[key] = value