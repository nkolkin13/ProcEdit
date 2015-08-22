from panda3d.core import Light, AmbientLight, DirectionalLight, Spotlight
from panda3d.core import Vec3, Vec4, Point3, Point2
from panda3d.core import LineSegs, TransparencyAttrib
from direct.task.Task import Task

class Edit_Env:
	def __init__(self,base,selection_mode):
		self.base = base
		self.initialize_lighting()
		self.draw_floor_plane(10,1)
		self.selection_mode = selection_mode
		self.keys = [0]
		self.base.taskMgr.add(self.control_editor, "edit-control-task")

		self.select_locked = False
		self.base.accept("space", self.setKeys, [0, 1])
		self.base.accept("space-up", self.setKeys, [0, 2])


	#switch upon which buttons are pressed with if statements 
	def setKeys(self, btn, value):
 		self.keys[btn] = value

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

	def select_vertex(self):
		mpos = Point2(self.base.mouseWatcherNode.getMouse())

		#only consider the points close to the click
		epsilon = 0.03
		v_IDs = []
		for v in self.base.active_obj.verts.values():
			p3 = self.base.cam.getRelativePoint(self.base.render, v.pos)
			p2 = Point2()
			self.base.camLens.project(p3,p2)
			if ((mpos-p2).length()) < epsilon:
				v_IDs.append(v.ID)



		selection = None

		if len(v_IDs) == 0:
			return 0
		if len(v_IDs) == 1:
			selection = v_IDs[0]

		if len(v_IDs) > 1:
			selected_ID = None 
			selected_dist = None
			for i in v_IDs:
				v = self.base.active_obj.verts[i]
				temp_dist = (self.base.cam.getPos()-v.pos).length()
				if selected_dist == None:
					selected_dist = temp_dist
					selected_ID = v.ID
				else:
					if temp_dist < selected_dist:
						selected_dist = temp_dist
						selected_ID = v.ID
			selection = selected_ID

		if selection in self.edit_obj.selected_IDs:
			self.edit_obj.selected_IDs.remove(selection)
		else:
			self.edit_obj.selected_IDs.add(selection)
		self.edit_obj.draw()




	def select(self):
		if not self.select_locked:
			if self.selection_mode == 'vertex':
				self.select_vertex()

			self.select_locked = True

	def control_editor(self, task):
		if self.keys[0] == 1:
			self.select()
		if self.keys[0] == 2:
			self.keys[0] = 0
			self.select_locked = False

		return Task.cont
