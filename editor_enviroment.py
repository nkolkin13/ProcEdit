from panda3d.core import Light, AmbientLight, DirectionalLight, Spotlight
from panda3d.core import Vec3, Vec4, Point3
from panda3d.core import LineSegs, TransparencyAttrib

class Edit_Env:
	def __init__(self):
		self.initialize_lighting()
		self.draw_floor_plane(10,1)

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