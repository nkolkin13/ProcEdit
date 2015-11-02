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

		self.active_lens = 1

		self.ortho_lens = OrthographicLens()
		self.ortho_lens.setAspectRatio(aspect_win)
		self.ortho_lens.setNearFar(1.0,100.0)

		self.persp_lens = PerspectiveLens()
		self.persp_lens.setAspectRatio(aspect_win)
		self.persp_lens.setFov(5.0)
		self.persp_lens.setNearFar(1.0,100.0)

		self.lenses = [self.persp_lens, self.ortho_lens]

		self.set_lens(lens=self.active_lens)


		self.set_view(Vec3(50.0,50.0,50.0))

		self.old_x = None
		self.old_y = None

		self.zoom_speed = 0.05
		self.pan_speed = 0.005
		self.rotate_speed = 0.1

		#these are pointers
		self.keys = self.base.keyboard_reader.keys
		self.key_map = self.base.keyboard_reader.key_map

		#registering camera functions
		self.base.taskMgr.add(hold_caller_multikey(trigger=self.keys, indices=[self.key_map['shift'], self.key_map['mouse2']], values=[1,1], init_handle=None, loop_handle=self.pan_camera, cleanup_handle=self.mouse_delta_cleanup), 'pan_camera_task')
		self.base.taskMgr.add(hold_caller_multikey(trigger=self.keys, indices=[self.key_map['control'], self.key_map['shift'], self.key_map['mouse2']], values=[0, 0,1], init_handle=None, loop_handle=self.rotate_camera_fixed_pivot, cleanup_handle=self.mouse_delta_cleanup), 'rotate_camera_task')
		self.base.taskMgr.add(hold_caller_multikey(trigger=self.keys, indices=[self.key_map['control'], self.key_map['mouse2']], values=[1,1], init_handle=None, loop_handle=self.zoom_camera, cleanup_handle=self.mouse_delta_cleanup), 'rotate_camera_task')


		#register camera presets
		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_front , trigger = self.keys, index = self.key_map['1'], value=1), 'camera_preset_front_task')
		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_side , trigger = self.keys, index = self.key_map['2'], value=1), 'camera_preset_side_task')
		self.base.taskMgr.add( delta_caller(handle = self.set_viewpoint_top , trigger = self.keys, index = self.key_map['3'], value=1), 'camera_preset_top_task')

		#register switching perspective
		#TODO: currently disabled because perspective camera is stupid and should feel bad
		#self.base.taskMgr.add( delta_caller(handle = self.switch_perspective , trigger = self.keys, index = self.key_map['5'], value=1), 'camera_switch_perspective_task')

		#makes the zoom level of the orthographic camera more reasonable
		self.fixed_zoom_camera(10.0)


	def set_view(self, position):
		self.pos = Vec3(position)
		self.base.cam.setPos(self.pos)
		self.pivot = Vec3(0.0,0.0,0.0)
		self.base.cam.lookAt(0.0,0.0,0.0)
		self.hpr = self.base.cam.getHpr()


	def set_lens(self,lens):

		old_pos = self.base.cam.getPos()
		self.active_lens = lens
		self.base.cam.node().setLens(self.lenses[self.active_lens])
		self.base.cam.setPos(old_pos)

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
		pan_speed = self.pan_speed

		(d_x,d_y) = self.get_mouse_delta()

		if (d_x != None) and (d_y != None):
			up = self.base.cam.getMat().getRow3(2)
			side = self.base.cam.getMat().getRow3(0)
			d_up = up * d_y * pan_speed
			d_side = side * -d_x * pan_speed
			self.pos = self.pos + d_up + d_side
			self.pivot = self.pivot + d_up + d_side
			self.base.cam.setPos(self.pos)

	def zoom_forward(self):
		self.fixed_zoom_camera(self.zoom_speed)

	def zoom_backward(self):
		self.fixed_zoom_camera(-self.zoom_speed)

	def fixed_zoom_camera(self, zoom_speed):
		if self.active_lens == 0:
			forward = self.base.cam.getMat().getRow3(1)
			d_forward = forward * zoom_speed
			self.pos = self.pos + d_forward
			self.base.cam.setPos(self.pos)

		if self.active_lens == 1:
			zoom_level = self.ortho_lens.getFilmSize()
			z_x = max(zoom_level.x + zoom_speed, 0.1)
			z_y = z_x*0.75
			self.ortho_lens.setFilmSize(z_x , z_y)

	def zoom_camera(self):
		zoom_speed = self.zoom_speed

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

	def rotate_camera_fixed_location(self):
		rotate_speed = self.rotate_speed

		(d_x,d_y) = self.get_mouse_delta()

		if (d_x != None) and (d_y != None):
			self.hpr = self.hpr + Vec3(-d_x * rotate_speed ,-d_y * rotate_speed ,0)
			self.base.cam.setHpr(self.hpr)

	def rotate_camera_fixed_pivot(self):

		pivot = self.pivot

		rotate_speed = self.rotate_speed

		(d_x,d_y) = self.get_mouse_delta()

		if (d_x != None) and (d_y != None):
			up = self.base.cam.getMat().getRow3(2)
			side = self.base.cam.getMat().getRow3(0)
			d_up = up * d_y * rotate_speed
			d_side = side * -d_x * rotate_speed
			old_length = self.pos.length()
			self.pos = self.pos + d_up + d_side
			self.pos = self.pos / self.pos.length() * old_length
			print self.pos.length()
			self.base.cam.setPos(self.pos)
			self.base.cam.lookAt(pivot)

	def set_viewpoint_front(self):
		self.set_view(Vec3(20.0,0.0,0.0))

	def set_viewpoint_side(self):
		self.set_view(Vec3(0.0,20.0,0.0))

	def set_viewpoint_top(self):
		self.set_view(Vec3(0.0,0.0,20.0))

	def switch_perspective(self):
		lens = (self.active_lens + 1) % 2
		self.set_lens(lens)

