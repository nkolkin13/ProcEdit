from direct.task.Task import Task
from panda3d.core import Vec3
from panda3d.core import Lens, OrthographicLens, PerspectiveLens, LensNode
from input_listener import *
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


		#these are pointers
		self.keys = self.base.keyboard_reader.keys
		self.key_map = self.base.keyboard_reader.key_map

		self.base.taskMgr.add(hold_caller(trigger=self.keys, index=self.key_map['shift-mouse1'], value=1, init_handle=None, loop_handle=self.pan_camera, cleanup_handle=self.mouse_delta_cleanup), 'pan_camera_task')
		self.base.taskMgr.add(hold_caller(trigger=self.keys, index=self.key_map['shift-mouse3'], value=1, init_handle=None, loop_handle=self.rotate_camera, cleanup_handle=self.mouse_delta_cleanup), 'rotate_camera_task')
		self.base.taskMgr.add(hold_caller(trigger=self.keys, index=self.key_map['shift-mouse2'], value=1, init_handle=None, loop_handle=self.zoom_camera, cleanup_handle=self.mouse_delta_cleanup), 'zoom_camera_task')

		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_front , trigger = self.keys, index = self.key_map['1'], value=1), 'camera_preset_front_task')
		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_side , trigger = self.keys, index = self.key_map['2'], value=1), 'camera_preset_side_task')
		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_top , trigger = self.keys, index = self.key_map['3'], value=1), 'camera_preset_top_task')

		#TODO: allow switching perspective
		#self.base.taskMgr.add( delta_caller(handle = self.switch_perspective , trigger = self.keys, index = self.key_map['5'], value=1), 'camera_switch_perspective_task')


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

	def mouse_delta_cleanup(self):
			self.old_x = None
			self.old_y = None

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

	def pan_camera(self):
		pan_speed = 0.005

		(d_x,d_y) = self.get_mouse_delta()

		if (d_x != None) and (d_y != None):
			up = self.base.cam.getMat().getRow3(2)
			side = self.base.cam.getMat().getRow3(0)
			d_up = up * d_y * pan_speed
			d_side = side * -d_x * pan_speed
			self.pos = self.pos + d_up + d_side
			self.base.cam.setPos(self.pos)

	def zoom_camera(self):
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

	def rotate_camera(self):
		rotate_speed = 0.05

		(d_x,d_y) = self.get_mouse_delta()

		if (d_x != None) and (d_y != None):
			self.hpr = self.hpr + Vec3(-d_x * rotate_speed ,-d_y * rotate_speed ,0)
			self.base.cam.setHpr(self.hpr)

	def set_viewpoint_front(self):
		self.set_view(Vec3(20.0,0.0,0.0))

	def set_viewpoint_side(self):
		self.set_view(Vec3(0.0,20.0,0.0))

	def set_viewpoint_top(self):
		self.set_view(Vec3(0.0,0.0,20.0))

	def switch_perspective(self):
		lens = (self.active_lens + 1) % 2
		self.set_lens(lens)

