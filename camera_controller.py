from direct.task.Task import Task
from panda3d.core import Vec3
from panda3d.core import Lens, OrthographicLens, PerspectiveLens, LensNode
import sys,os

class Camera_Controller:
	
	def __init__(self,base):

		self.base = base
		self.base.disableMouse()		

		self.set_view_front()

		self.active_lens = 0

		self.ortho_lens = OrthographicLens()
		self.ortho_lens.setFilmSize(12, 9)

		self.persp_lens = PerspectiveLens()
		self.persp_lens.setFilmSize(12, 9)

		self.lenses = [self.persp_lens, self.ortho_lens]

		self.set_lens(lens=0)
		self.lens_locked = False

		self.old_x = None
		self.old_y = None


		self.keys = [0,0,0,0,0,0]
		self.base.taskMgr.add(self.control_camera, "camera-task")


		self.base.accept("1", self.setKeys, [0, 1])
		self.base.accept("1-up", self.setKeys, [0, 0])
		self.base.accept("2", self.setKeys, [1, 1])
		self.base.accept("2-up", self.setKeys, [1, 0])
		self.base.accept("3", self.setKeys, [2, 1])
		self.base.accept("3-up", self.setKeys, [2, 0])
		self.base.accept("shift-mouse2",self.setKeys,[3,1])
		self.base.accept("mouse2-up",self.setKeys,[3,2])
		self.base.accept("shift-mouse1",self.setKeys,[4,1])
		self.base.accept("mouse1-up",self.setKeys,[4,2])
		self.base.accept("5", self.setKeys, [5, 1])
		self.base.accept("5-up", self.setKeys, [5, 2])

   
	#switch upon which buttons are pressed with if statements 
	def setKeys(self, btn, value):
 		self.keys[btn] = value

	def set_view_front(self):
		self.pos = Vec3(5.0,0.0,0.0)
		self.base.camera.setPos(self.pos)
		self.base.camera.lookAt(0.0,0.0,0.0)
		self.hpr = self.base.camera.getHpr()

	def set_view_side(self):
		self.pos = Vec3(0.0,5.0,0.0)
		self.base.camera.setPos(self.pos)
		self.base.camera.lookAt(0.0,0.0,0.0)
		self.hpr = self.base.camera.getHpr()

	def set_view_top(self):
		self.pos = Vec3(0.0,0.0,5.0)
		self.base.camera.setPos(self.pos)
		self.base.camera.lookAt(0.0,0.0,0.0)
		self.hpr = self.base.camera.getHpr()

	def set_lens(self,lens):
		if not self.lens_locked:
			self.active_lens = lens
			self.base.cam.node().setLens(self.lenses[self.active_lens])
			self.lens_locked = True


	def control_camera(self,task):

		if self.keys[0]:
			self.set_view_front()

		if self.keys[1]:
			self.set_view_side()

		if self.keys[2]:
			self.set_view_top()


		if self.keys[3] == 1:
			pan_speed = 0.01

			md = self.base.win.getPointer(0)
			x = md.getX()
			y = md.getY()

			if self.old_x == None or self.old_y == None:
				self.old_x = x
				self.old_y = y
			else:
				d_x = (x - self.old_x) * pan_speed
				d_y = (y - self.old_y) * pan_speed
				self.old_x = x
				self.old_y = y
				self.pos = self.pos + Vec3(d_x,d_y,0)
				self.base.camera.setPos(self.pos)

		if self.keys[3] == 2:
			self.old_x = None
			self.old_y = None
			self.setKeys(3,0)


		if self.keys[4] == 1:
			rotate_speed = 0.05

			md = self.base.win.getPointer(0)
			x = md.getX()
			y = md.getY()

			if self.old_x == None or self.old_y == None:
				self.old_x = x
				self.old_y = y
			else:
				d_x = (x - self.old_x) * rotate_speed
				d_y = (y - self.old_y) * rotate_speed
				self.old_x = x
				self.old_y = y
				self.hpr = self.hpr + Vec3(d_x,d_y,0)
				self.base.camera.setHpr(self.hpr)

		if self.keys[4] == 2:
			self.old_x = None
			self.old_y = None
			self.setKeys(4,0)

		if self.keys[5] == 1:
			lens = (self.active_lens + 1) % 2
			self.set_lens(lens)

		if self.keys[5] == 2:
			self.lens_locked = False
			self.keys[5] = 0

		return Task.cont