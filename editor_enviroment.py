from panda3d.core import Light, AmbientLight, DirectionalLight, Spotlight
from panda3d.core import Vec3, Vec4, Point3, Point2
from panda3d.core import LineSegs, TransparencyAttrib
from mesh_selection import Mesh_Selection
from input_listener import delta_caller
from direct.task.Task import Task

class Edit_Env:
	def __init__(self,base, mesh, selection_mode):

		#TODO remove circular reference to base
		self.base = base

		self.initialize_lighting()
		self.draw_floor_plane(10,1)
		self.selection_mode = selection_mode

		self.mesh_selection = Mesh_Selection(self.base,mesh,self.selection_mode)



	def initialize_lighting(self):
		# Create Ambient Light 
		ambientLight = AmbientLight('ambientLight')
		ambientLight.setColor(Vec4(0.8,0.8,0.8,1))
		ambientLightNP = render.attachNewNode(ambientLight)
		render.setLight(ambientLightNP)

		#Create Directional Light
		sunLight = DirectionalLight('sunLight')
		sunLight.setColor(Vec4(0.9,0.9,0.9,1))
		sunLightNP = render.attachNewNode(sunLight)
		sunLightNP.setHpr(180,-20,0)
		render.setLight(sunLightNP)

		#Create Directional Light
		backLight = DirectionalLight('backLight')
		backLight.setColor(Vec4(0.2,0.2,0.2,1))
		backLightNP = render.attachNewNode(backLight)
		backLightNP.setHpr(-180,160,0)
		render.setLight(backLightNP)

		return 0

	def draw_floor_plane(self,size,granularity):
		line_drawer = LineSegs('grid_line_drawer')
		line_drawer.setColor(0.0,0.0,0.0,1.0)
		line_drawer.setThickness(1.0)
		for i in range(-size,size+1,granularity):
			line_drawer.moveTo(Vec3(float(i),float(-size),0.0))
			line_drawer.drawTo(Vec3(float(i),float(size),0.0))

		for i in range(-size,size+1,granularity):
			line_drawer.moveTo(Vec3(float(-size),float(i),0.0))
			line_drawer.drawTo(Vec3(float(size),float(i),0.0))

		edge_node = line_drawer.create()
		rendered_edges = render.attachNewNode(edge_node)
		rendered_edges.setTransparency(TransparencyAttrib.MAlpha)
		rendered_edges.setAlphaScale(0.5)

		return 0


'''
	def set_mouse_origin(self):
			if self.base.mouseWatcherNode.hasMouse():
				self.selected_tool = 'grab'
				self.mouse_origin = Point2(self.base.mouseWatcherNode.getMouse())
				self.selected_locations = {}
				for id in self.edit_obj.selected_IDs:
					self.selected_locations[id] = self.edit_obj.e_objects[id].getPos()

	def grab(self):	
		if self.base.mouseWatcherNode.hasMouse():

			mpos = Point2(self.base.mouseWatcherNode.getMouse())
			delta = mpos - self.mouse_origin


			near_dist = self.base.cam.node().getLens().getNear()
			up_vec = self.base.cam.getMat().getRow3(2)
			side_vec = self.base.cam.getMat().getRow3(0)

			for id in self.edit_obj.selected_IDs:
				#TODO: interact with selection struct/class
				selected_obj = self.base.active_obj.verts[id]

				#TODO, do this to average for efficiency
				far_dist = (self.base.cam.getPos()-self.selected_locations[id]).length()

				factor = (far_dist-near_dist)/3.0

				up_delta = up_vec * factor * delta.y
				side_delta = side_vec * factor * delta.x

				selected_obj.pos = (self.selected_locations[id]+up_delta+side_delta)
			self.base.active_obj.reset_draw()
			self.base.active_obj.draw()
			self.edit_obj.draw()

'''