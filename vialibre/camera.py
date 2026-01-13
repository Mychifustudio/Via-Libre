from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3, NodePath
from math import exp


class Camera(DirectObject):
    def __init__(self, target: NodePath, showbase: ShowBase = None):
        self.target: NodePath = target
        self.base = showbase if showbase else base

        #----- Position variables declaration ------#
        self.cameraOffset = Vec3(0)

        #----- FOV variables declaration -----------#
        self.fov = 50
        self.zoomLevel = 0
        self.maxZoomOut = 5
        self.zoomInSpeed = 3
        self.zoomOutSpeed = .2

        #----- LookAhead variables declaration -----#
        self.lookAhead = Vec3(0)
        self.smoothingAhead = 3
        self.smoothingBack = .5
        self.maxLookAhead = .25       

        #----- Initate the camera ------------------#
        self.setupCamera()

    def setPos(self, pos: Point3):
        self.camPivot.setPos(pos)

    def setP(self, pitch: float):
        self.base.camera.setP(pitch)

    def setOffset(self, offset: Vec3):
        self.cameraOffset = offset

    def setupCamera(self):
        self.camPivot = self.base.render.attach_new_node('camPivot')
        self.base.camera.reparent_to(self.camPivot)

    def calculateCameraPos(self, dt, movementVector: Vec3, lastMovement: Vec3):
        """Calculates a new position for the camera.

        Args:
            dt (float): Delta Time
            movementVector (Vec3): Current computed movement vector
            lastMovement (Vec3): Movement vector computed last frame

        Returns:
            Point3: Calculated camera position
        """
        currentLookAhead = self.lookAhead
        if movementVector.length() >= lastMovement.length() and lastMovement.length() > 0:
            targetLookAhead = movementVector * self.maxLookAhead
            smoothing = self.smoothingAhead
        else:
            targetLookAhead = Vec3(0)
            smoothing = self.smoothingBack

        self.lookAhead = self.powLerp(currentLookAhead, targetLookAhead, dt, smoothing)

        return self.target.getPos() + self.cameraOffset + self.lookAhead

    def powLerp(self, current, target, dt, smoothTime):
        if smoothTime <= 0:
            return target
        return current + (target - current) * (1 - exp(-dt / smoothTime))

    def updateFov(self, dt, isMoving):
        self.zoomLevel = self.maxZoomOut if isMoving else 0

        targetFov = self.fov + self.zoomLevel
        currentFov = self.base.camLens.getFov()[0]

        if targetFov > currentFov:
            smoothingSpeed = self.zoomOutSpeed
        else:
            smoothingSpeed = self.zoomInSpeed

        currentFov += (targetFov - currentFov) * (1 - exp(-smoothingSpeed * dt))

        # self.camLens.setFov(currentFov + (targetFov - currentFov) * min(zoomSpeed * dt, 1))
        self.base.camLens.setFov(currentFov)