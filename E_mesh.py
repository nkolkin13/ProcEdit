from D_mesh import *

class e_mesh:
	def __init__(self,parent_mesh,initial_mode):
		self.parent = parent_mesh
		self.mode = initial_mode
		self.base_color = Vec4(0.0,0.0,0.0,1.0)
		self.selected_color = Vec4(1.0,0.36,0.0,1.0)
		self.render_root = render.attachNewNode("e_root")
		self.e_objects = []
		self.selected_IDs = set()
		self.draw()


	def draw(self):
		if len(self.e_objects) > 0:
			self.draw_reset()
		if self.mode == 'vertex':
			self.draw_verts()
		if self.mode == 'edge':
			self.draw_edges()


	'''
	def draw_edges(self):
		line_drawer = LineSegs('line_drawer')
		line_drawer.setColor(0.0,0.0,0.0,1.0)
		line_drawer.setThickness(1.5)
		drawn_edges = set()
		for e in self.parent.edges:
			if (not e.twin == None) and (e.twin.ID not in drawn_edges):
				line_drawer.moveTo(e.v1.pos)
				line_drawer.drawTo(e.v2.pos)
				drawn_edges.add(e.ID)

		edge_node = line_drawer.create()
		rendered_edges = render.attachNewNode(edge_node)
	'''

	def draw_reset(self):
		for o in self.e_objects:
			o.removeNode()
		self.e_objects = []

	def draw_vert(self,v, v_color):
		format = GeomVertexFormat.getV3cp()
		vdata=GeomVertexData('vert', format, Geom.UHDynamic)
		vertex=GeomVertexWriter(vdata, 'vertex')
		color=GeomVertexWriter(vdata, 'color')
		vertex.addData3f(v.pos.x,v.pos.y,v.pos.z)
		color.addData4f(v_color)		
		mesh = Geom(vdata)
		point = GeomPoints(Geom.UHDynamic)
		point.addVertex(0)
		point.closePrimitive()
		mesh.addPrimitive(point)
		vert_node = GeomNode(self.parent.name+'_vert_'+str(v.ID))
		vert_node.addGeom(mesh)
		vert_node.setTag('ID',str(v.ID))
		rendered_vert = self.render_root.attachNewNode(vert_node)
		rendered_vert.setRenderModeThickness(5.0)
		self.e_objects.append(rendered_vert)



	def draw_verts(self):
		for v in self.parent.verts.values():
			if v.ID in self.selected_IDs:
				self.draw_vert(v,self.selected_color)
			else:
				self.draw_vert(v,self.base_color)
