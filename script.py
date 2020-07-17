#!/usr/bin/env python

# Author: William Staudenmeier
# Models: Jeff Styers, Reagan Heller, Alice
# Based off Roaming Ralph tutorial for Panda3D
# This automates movement by the computer
# The penguin is placed at random places in the world, and the Panda needs to find him before the blizzard


from setuptools import setup
import direct
import numpy
#import tensorflow
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollisionHandlerPusher, CollisionSphere
from panda3d.core import Filename, AmbientLight, DirectionalLight
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from panda3d.core import CollideMask
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
import random
import sys
import os
import math
from direct.showbase.ShowBase import ShowBase
from panda3d.core import TextNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import LPoint3, LVector3
from panda3d.core import Filename
from panda3d.physics import BaseParticleEmitter, BaseParticleRenderer
from panda3d.physics import PointParticleFactory, SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce, DiscEmitter
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText
import sys




px = random.randint(-12, 15)
py = random.randint(-70,-55)



# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text="Where are you, Penguin Cool?", style=1, fg=(1, 1, 1, 1), scale=.07,
                        parent=base.a2dBottomRight, align=TextNode.ARight,
                        pos=(-0.1, 0.09), shadow=(0, 0, 0, 1))


class RoamingPenguinDemo(ShowBase):
    def __init__(self):
        # Set up the window, camera, etc.
        ShowBase.__init__(self)

        # This is used to store which keys are currently pressed.
        self.keyMap = {
            "left": 0,
            "right": 0,
            "forward": 0,
            "backward": 0,
            "cam-left": 0,
            "cam-right": 0,
        }

    

        ###########################################################################

        self.environ = loader.loadModel("models/world")
        self.environ.reparentTo(render)

        # We do not have a skybox, so we will just use a sky blue background color
        #self.setBackgroundColor(0.53, 0.80, 0.92, 1)
        self.setBackgroundColor(.1, .1, .1, 1)
        # Create the main character, person

        #personStartPos = self.environ.find("**/start_point").getPos()
        #self.person = Actor("models/panda",
         #                  {"run": "models/panda-walk",
          #                  "walk": "models/panda-walk"})

        person2StartPos = self.environ.find("**/start_point").getPos()
        self.person2 = Actor("models/passenger_penguin",
                           {"run": "models/passenger_penguin",
                            "walk": "models/passenger_penguin"})

       
        self.person2.reparentTo(render)
        self.person2.setScale(.1)
   
        self.person2.setPos(person2StartPos + (px, py, 1))


        person3StartPos = self.environ.find("**/start_point").getPos()
        self.person3 = Actor("models/MagicBunny",
                           {"run": "models/MagicBunny",
                            "walk": "models/MagicBunny"})

        #px = random.randint(-1,1)
        #py = random.randint(-1,1)


        self.person3.reparentTo(render)
        self.person3.setScale(.04)
        #self.person.setPos(personStartPos + (0, 0, 2))
        self.person3.setPos(person3StartPos + (px/1.5+3, py/2, 0))

        personStartPos = self.environ.find("**/start_point").getPos()
        self.person = Actor("models/panda",
                           {"run": "models/panda-walk",
                            "walk": "models/panda-walk"})


        self.person.reparentTo(render)
        self.person.setScale(.1)
        self.person.setPos(personStartPos + (0, 0, 1.5))
        self.person.loop("run")


        arenaStartPos = self.environ.find("**/start_point").getPos()
        self.arena = Actor("models/FarmHouse")


        self.arena.reparentTo(render)
        self.arena.setScale(.1)
        self.arena.setPos(arenaStartPos + (-1, 0, 0))


        arena2StartPos = self.environ.find("**/start_point").getPos()
        self.arena2 = Actor("models/fence")


        self.arena2.reparentTo(render)
        self.arena2.setScale(5.9)
        self.arena.setPos(arenaStartPos + (px, py-12, 1))
        self.arena2.setPos(arenaStartPos + (8, 5, -1))


        arena2StartPos = self.environ.find("**/start_point").getPos()
        self.arena3 = Actor("models/gate")


        self.arena3.reparentTo(render)
        self.arena3.setScale(.01)

        self.arena3.setPos(arenaStartPos + (px/2+random.randint(12,15), py/2, -1))

        self.arena4 = Actor("models/FarmHouse")
        self.arena4.reparentTo(render)
        self.arena4.setScale(.1)

        self.arena4.setPos(arenaStartPos + (px/3-random.randint(18,22), py/3, -1))


        self.arena5 = Actor("models/gate")
        self.arena5.reparentTo(render)
        self.arena5.setScale(.008)

        self.arena5.setPos(arenaStartPos + (px/1.2-9, py/1.2, -1))

        #####################################################################################################################################
        base.enableParticles()
        self.t = loader.loadModel("teapot") # for the particle enhancer
        self.t.setScale(10)
        self.t.setPos(-10, -20, -1)
        self.t.reparentTo(render)
        #self.setupLights()
        self.p = ParticleEffect()
        self.p.setScale(1000)
        self.loadParticleConfig('smoke.ptf') # looks like a storm at night
        self.p.setScale(20)




        #################################################3

        # Create a floater object, which floats 2 units above person.  We
        # use this as a target for the camera to look at.

        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(self.person)
        self.floater.setZ(2.0)

        # Accept the control keys for movement and rotation


        taskMgr.add(self.move, "moveTask")

        # Set up the camera
        self.disableMouse()
        self.camera.setPos(self.person.getX(), self.person.getY() + 10, 2)

        self.cTrav = CollisionTraverser()

    
        self.personCol = CollisionNode('person')
        self.personCol.addSolid(CollisionSphere(center=(0, 0, 2), radius=1.5))
        self.personCol.addSolid(CollisionSphere(center=(0, -0.25, 4), radius=1.5))
        self.personCol.setFromCollideMask(CollideMask.bit(0))
        self.personCol.setIntoCollideMask(CollideMask.allOff())
        self.personColNp = self.person.attachNewNode(self.personCol)
        self.personPusher = CollisionHandlerPusher()
        self.personPusher.horizontal = True

        self.personPusher.addCollider(self.personColNp, self.person)
        self.cTrav.addCollider(self.personColNp, self.personPusher)

        
        self.personGroundRay = CollisionRay()
        self.personGroundRay.setOrigin(0, 0, 9)
        self.personGroundRay.setDirection(0, 0, -1)
        self.personGroundCol = CollisionNode('personRay')
        self.personGroundCol.addSolid(self.personGroundRay)
        self.personGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.personGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.personGroundColNp = self.person.attachNewNode(self.personGroundCol)
        self.personGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.personGroundColNp, self.personGroundHandler)

        self.camGroundRay = CollisionRay()
        self.camGroundRay.setOrigin(0, 0, 9)
        self.camGroundRay.setDirection(0, 0, -1)
        self.camGroundCol = CollisionNode('camRay')
        self.camGroundCol.addSolid(self.camGroundRay)
        self.camGroundCol.setFromCollideMask(CollideMask.bit(0))
        self.camGroundCol.setIntoCollideMask(CollideMask.allOff())
        self.camGroundColNp = self.camera.attachNewNode(self.camGroundCol)
        self.camGroundHandler = CollisionHandlerQueue()
        self.cTrav.addCollider(self.camGroundColNp, self.camGroundHandler)

       
   

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.3, .3, .3, .2))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection((-5, -5, -5))
        directionalLight.setColor((.2, .2, .2, 1))
        directionalLight.setSpecularColor((.1, .1, .1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight))

    def loadParticleConfig(self, filename):
        # Start of the code from steam.ptf
        self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(filename))
    
        self.p.start(self.t)
        self.p.setPos(3.000, 0.000, 2.250)




    # Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value


    def move(self, task):

      
        dt = globalClock.getDt()
       

        #z = abs(py)
        self.person.setX(self.person, 4 * dt)
        self.person.setX(self.person, -4 * dt)

        ## this is how the Panda finds his friend

        if px < 0 :
            #if self.person.getPos() - self.person2.getPos() < (0, 0, 0) :
            if self.person.getY() - self.person2.getY() < 6 :
            #self.person.getPos(personStartPos + (0, py, 1.5))
                self.person.setY(self.person, 0 * dt)
                self.person.stop()
                self.person.pose("walk", 5)
                self.isMoving = False
            else:
                self.person.setY(self.person, py * dt)
                self.person.setX(self.person, px * dt)
                self.person.setH(self.person, px/(abs(px)+6)* dt)
        else:
            if self.person.getY() - self.person2.getY() < 6 :
            #self.person.getPos(personStartPos + (0, py, 1.5))
                self.person.setY(self.person, 0 * dt)
                self.person.stop()
                self.person.pose("walk", 5)
                self.isMoving = False
            else:
                self.person.setY(self.person, py * dt)
                self.person.setX(self.person, px * dt)
                self.person.setH(self.person, px/(abs(px)+6)* dt)


        if self.keyMap["cam-left"]:
            self.camera.setX(self.camera, -20 * dt)
        if self.keyMap["cam-right"]:
            self.camera.setX(self.camera, +20 * dt)

       
        camvec = self.person.getPos() - self.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if camdist > 10.0:
            self.camera.setPos(self.camera.getPos() + camvec * (camdist - 10))
            camdist = 10.0
        if camdist < 5.0:
            self.camera.setPos(self.camera.getPos() - camvec * (5 - camdist))
            camdist = 5.0

    

        entries = list(self.personGroundHandler.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        for entry in entries:
            if entry.getIntoNode().getName() == "terrain":
                self.person.setZ(entry.getSurfacePoint(render).getZ())

     

        entries = list(self.camGroundHandler.entries)
        entries.sort(key=lambda x: x.getSurfacePoint(render).getZ())

        for entry in entries:
            if entry.getIntoNode().getName() == "terrain":
                self.camera.setZ(entry.getSurfacePoint(render).getZ() + 3.5)
        if self.camera.getZ() < self.person.getZ() + 4.0:
            self.camera.setZ(self.person.getZ() + 4.0)

       
        self.camera.lookAt(self.floater)

        return task.cont


demo = RoamingPenguinDemo()
demo.run()
