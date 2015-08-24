from direct.task.Task import Task
from panda3d.core import Vec3
from panda3d.core import Lens, OrthographicLens, PerspectiveLens, LensNode
import sys,os

class Camera_Controller:
	
	def __init__(self,base):

		self.base = base
		self.base.disableMouse()		

		x_win = self.base.win.getXSize()
		y_win = self.base.win.getYSize()
		aspect_win = float(x_win)/float(y_win)

		self.active_lens = 0

		self.ortho_lens = OrthographicLens()
		self.ortho_lens.setAspectRatio(aspect_win)
		self.ortho_lens.setNearFar(1.0,100.0)

		self.persp_lens = PerspectiveLens()
		self.persp_lens.setAspectRatio(aspect_win)
		self.persp_lens.setNearFar(1.0,100.0)

		self.lenses = [self.persp_lens, self.ortho_lens]

		self.lens_locked = False
		self.set_lens(lens=0)
		self.lens_locked = False


		self.set_view(Vec3(20.0,0.0,0.0))

		self.old_x = None
		self.old_y = None


		self.keys = [0,0,0,0,0,0,0]
		self.base.taskMgr.add(self.control_camera, "camera-task")


		self.base.accept("1", self.setKeys, [0, 1])
		self.base.accept("1-up", self.setKeys, [0, 0])
		self.base.accept("2", self.setKeys, [1, 1])
		self.base.accept("2-up", self.setKeys, [1, 0])
		self.base.accept("3", self.setKeys, [2, 1])
		self.base.accept("3-up", self.setKeys, [2, 0])
		self.base.accept("shift-mouse3",self.setKeys,[3,1])
		self.base.accept("mouse3-up",self.setKeys,[3,2])
		self.base.accept("shift-mouse1",self.setKeys,[4,1])
		self.base.accept("mouse1-up",self.setKeys,[4,2])
		self.base.accept("5", self.setKeys, [5, 1])
		self.base.accept("5-up", self.setKeys, [5, 2])
		self.base.accept("shift-mouse2", self.setKeys, [6, 1])
		self.base.accept("mouse2-up", self.setKeys, [6, 2])
   
	#switch upon which buttons are pressed with if statements 
	def setKeys(self, btn, value):
 		self.keys[btn] = value

	def set_view(self, position):
		self.pos = Vec3(position)
		self.base.cam.setPos(self.pos)
		self.base.cam.lookAt(0.0,0.0,0.0)
		self.hpr = self.base.cam.getHpr()


	def set_lens(self,lens):
		if not self.lens_locked:
			self.active_lens = lens
			self.base.cam.node().setLens(self.lenses[self.active_lens])
			self.lens_locked = True

	def get_mouse_delta(self):

			md = self.base.win.getPointer(0)
			x = md.getX()
			y = md.getY()

			d_x = None
			d_y = None

			if self.old_x == None or self.old_y == None:
				self.old_x = x
				self.old_y = y
			else:
				d_y = (y - self.old_y) 
				d_x = (x - self.old_x)
				self.old_x = x
				self.old_y = y

			return (d_x, d_y)

	def control_camera(self,task):

		if self.keys[0]:
			self.set_view(Vec3(20.0,0.0,0.0))

		if self.keys[1]:
			self.set_view(Vec3(0.0,20.0,0.0))

		if self.keys[2]:
			self.set_view(Vec3(0.0,0.0,20.0))

		if self.keys[3] == 1:
			pan_speed = 0.005

			(d_x,d_y) = self.get_mouse_delta()

			if (d_x != None) and (d_y != None):
				up = self.base.cam.getMat().getRow3(2)
				side = self.base.cam.getMat().getRow3(0)
				d_up = up * d_y * pan_speed
				d_side = side * -d_x * pan_speed
				self.pos = self.pos + d_up + d_side
				self.base.cam.setPos(self.pos)

		if self.keys[3] == 2:
			self.old_x = None
			self.old_y = None
			self.setKeys(3,0)


		if self.keys[4] == 1:
			rotate_speed = 0.05

			(d_x,d_y) = self.get_mouse_delta()

			if (d_x != None) and (d_y != None):
				self.hpr = self.hpr + Vec3(-d_x * rotate_speed ,-d_y * rotate_speed ,0)
				self.base.cam.setHpr(self.hpr)

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

		if self.keys[6] == 1:
			zoom_speed = 0.01

			(d_x,d_y) = self.get_mouse_delta()

			if (d_y != None):
				if self.active_lens == 0:
					forward = self.base.cam.getMat().getRow3(1)
					d_forward = forward * d_y * zoom_speed
					self.pos = self.pos + d_forward
					self.base.cam.setPos(self.pos)

				if self.active_lens == 1:
					zoom_level = self.ortho_lens.getFilmSize()
					z_x = max(zoom_level.x + d_y * zoom_speed, 0.1)
					z_y = z_x*0.75
					self.ortho_lens.setFilmSize(z_x , z_y)

		if self.keys[6] == 2:
			self.old_x = None
			self.old_y = None
			self.setKeys(6,0)

		return Task.cont