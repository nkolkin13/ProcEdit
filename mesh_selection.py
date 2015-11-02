from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomPoints, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3, Point2
from panda3d.core import LineSegs
from input_listener import *
from direct.task.Task import Task
import util_PG

class Mesh_Selection:
	def __init__(self, base, mesh, selection_mode):

		self.base = base
		self.selection_mode = selection_mode
		self.mesh = mesh
		self.selected_vertices = set()
		self.selected_edges = set()
		self.selected_faces = set()

		self.render_root = 	render.attachNewNode("selection_root")
		self.render_nodes = {}

		self.average_position = Vec3( 0.0, 0.0, 0.0)

		#these are pointers
		self.keys = self.base.keyboard_reader.keys
		self.key_map = self.base.keyboard_reader.key_map
		
		self.base.taskMgr.add(delta_caller(self.select, self.keys, self.key_map['space'], 1), 'selection_task')

		self.draw()

	#switch upon which buttons are pressed with if statements 
	def setKeys(self, btn, value):
 		self.keys[btn] = value



	def reset_draw(self):
		for r in self.render_nodes.values():
			r.removeNode()

		self.render_nodes = {}

	def draw_face(self,f,f_color):
		#add normal
		format = GeomVertexFormat.getV3n3cp()
		vdata=GeomVertexData('vert', format, Geom.UHDynamic)
		vertex=GeomVertexWriter(vdata, 'vertex')
		color=GeomVertexWriter(vdata, 'color')
		normal=GeomVertexWriter(vdata, 'normal')

		vertex.addData3f(f.v1.pos)
		normal.addData3f(f.v1.norm.x, f.v1.norm.y, f.v1.norm.z)
		color.addData4f(f_color)

		vertex.addData3f(f.v2.pos)
		normal.addData3f(f.v2.norm.x, f.v2.norm.y, f.v2.norm.z)
		color.addData4f(f_color)	

		vertex.addData3f(f.v3.pos)
		normal.addData3f(f.v3.norm.x, f.v3.norm.y, f.v3.norm.z)		
		color.addData4f(f_color)		

		mesh = Geom(vdata)
		tri = GeomTriangles(Geom.UHDynamic)
		tri.addVertex(0)
		tri.addVertex(1)
		tri.addVertex(2)
		tri.closePrimitive()
		mesh.addPrimitive(tri)
		face_node = GeomNode(self.mesh.name+'_face_'+str(f.ID))
		face_node.addGeom(mesh)
		face_node.setTag('ID',str(f.ID))
		rendered_face = self.render_root.attachNewNode(face_node)
		rendered_face.setTwoSided(True)
		self.render_nodes['face_'+str(f.ID)] = rendered_face

	def draw_edge(self,e,e_color):
		line_drawer = LineSegs('line_drawer')
		line_drawer.setColor(e_color)
		line_drawer.setThickness(1.5)
		line_drawer.moveTo(e.v1.pos)
		line_drawer.drawTo(e.v2.pos)
		edge_node = line_drawer.create()
		rendered_edge = self.render_root.attachNewNode(edge_node)
		self.render_nodes['edge_'+str(e.ID)] = rendered_edge


	def draw_vert(self,v, v_color):
		format = GeomVertexFormat.getV3cp()
		vdata=GeomVertexData('vert', format, Geom.UHDynamic)
		vertex=GeomVertexWriter(vdata, 'vertex')
		color=GeomVertexWriter(vdata, 'color')
		vertex.addData3f(0.0,0.0,0.0)
		color.addData4f(v_color)		
		mesh = Geom(vdata)
		point = GeomPoints(Geom.UHDynamic)
		point.addVertex(0)
		point.closePrimitive()
		mesh.addPrimitive(point)
		vert_node = GeomNode(self.mesh.name+'_vert_'+str(v.ID))
		vert_node.addGeom(mesh)
		vert_node.setTag('ID',str(v.ID))
		rendered_vert = self.render_root.attachNewNode(vert_node)
		rendered_vert.setPos(v.pos.x,v.pos.y,v.pos.z)
		rendered_vert.setRenderModeThickness(5.0)
		self.render_nodes['vert_'+str(v.ID)] = rendered_vert

	def draw(self):

		self.reset_draw()

		base_color = Vec4(0.0,0.0,0.0,1.0)
		active_selected_color = Vec4(1.0,0.36,0.0,1.0)
		inactive_selected_color = Vec4(0.5,0.18,0.0,1.0)

		if self.selection_mode == 'vertex':
			for v in self.mesh.verts.values():
				if v.ID in self.selected_vertices:
					self.draw_vert( v, active_selected_color)
				else:
					self.draw_vert( v, base_color)

			drawn_edges = set()
			for e in self.mesh.edges.values():
				if (e.twin == None) or (e.twin.ID not in drawn_edges):
					if e.ID in self.selected_edges:
						self.draw_edge( e, inactive_selected_color)
					else:
						self.draw_edge( e, base_color)
				drawn_edges.add(e.ID)

			#for f in self.mesh.faces.values():
			#	if f.ID in self.selected_faces:
			#		self.draw_face(f, inactive_selected_color)


		elif self.selection_mode == 'edge':
			return 0

		elif self.selection_mode == 'face':
			return 0

		else:
			print "TRIED TO DRAW UNKNOWN SELECTION MODE, DID NOTHING"
			return -1

	#slow af, could be sped up to o(1) with some precomputation (dict of edges keyed by origin, and dict of (face,edge) tuples indexed by origin of edge)
	def check_faces_to_add(self):
		for f in self.mesh.faces.values():
			if (f.v1.ID in self.selected_vertices) and (f.v2.ID in self.selected_vertices) and (f.v3.ID in self.selected_vertices):
				self.selected_faces.add(f.ID)

	def check_edges_to_add(self):
		for e in self.mesh.edges.values():
			if (e.v1.ID in self.selected_vertices) and (e.v2.ID in self.selected_vertices):
				self.selected_edges.add(e.ID)

	def recalculate_average(self, verts):
		self.average_position = Vec3(0.0,0.0,0.0)
		for v in verts:
			if v.ID in self.selected_vertices:
				self.average_position = self.average_position + v.pos

		self.average_position = self.average_position / len(self.selected_vertices)

	def add_vertex(self, v):

		#initialize to avoid divide by 0 error
		if len(self.selected_vertices) == 0:
			self.average_position = v.pos

		else:
			#weight to give to old average
			w1 = float(len(self.selected_vertices))/float(len(self.selected_vertices)+1.0)

			#weight to give to new vertex
			w2 = 1.0/float(len(self.selected_vertices)+1.0)

			self.average_position = self.average_position*w1 + v.pos*w2

		self.selected_vertices.add(v.ID)
		self.check_faces_to_add()
		self.check_edges_to_add()

	def add_face(self, f):
		self.add_vertex(f.v1)
		self.add_vertex(f.v2)
		self.add_vertex(f.v3)

	def add_edge(self, e):
		self.add_vertex(e.v1)
		self.add_vertex(e.v2)

	#these checks could probably be much faster
	def check_faces_to_remove(self,v):

		temp_set = set(self.selected_faces)

		for i in temp_set:
			f = self.mesh.faces[i]
			if (v.ID == f.v1.ID) or (v.ID == f.v2.ID) or (v.ID == f.v3.ID):
				self.selected_faces.remove(f.ID)

	def check_edges_to_remove(self,v):

		temp_set = set(self.selected_edges)

		for i in temp_set:
			e = self.mesh.edges[i]
			if (v.ID == e.v1.ID) or (v.ID == e.v2.ID):
				self.selected_edges.remove(e.ID)

	def remove_vertex(self, v):
		#update average position of selection
		self.average_position = self.average_position -  (v.pos *(1.0/len(self.selected_vertices)))
		self.selected_vertices.remove(v.ID)
		self.check_edges_to_remove(v)
		self.check_faces_to_remove(v)

	def remove_face(self, f):
		self.remove_vertex(f.v1)
		self.remove_vertex(f.v2)
		self.remove_vertex(f.v3)

	def remove_edge(self, e):
		self.remove_vertex(e.v1)
		self.remove_vertex(e.v2)


	def select_vertex(self):
		mpos = Point2(self.base.mouseWatcherNode.getMouse())

		#only consider the points close to the click
		epsilon = 0.03
		Vs = []
		for v in self.mesh.verts.values():
			p3 = self.base.cam.getRelativePoint(render, v.pos)
			p2 = Point2()
			self.base.cam.node().getLens().project(p3,p2)
			if ((mpos-p2).length()) < epsilon:
				Vs.append(v)

		selected_vert = None


		if len(Vs) == 0:
			return 0
		if len(Vs) == 1:
			selected_vert = Vs[0]

		selected_dist = None
		if len(Vs) > 1:
			for v in Vs:
				temp_dist = (self.base.cam.getPos()-v.pos).length()
				if selected_dist == None:
					selected_dist = temp_dist
					selected_vert = v
				else:
					if temp_dist < selected_dist:
						selected_dist = temp_dist
						selected_vert = v

		if selected_vert.ID in self.selected_vertices:
			self.remove_vertex(selected_vert)
		else:
			self.add_vertex(selected_vert)


	def select(self):
		if self.selection_mode == 'vertex':
			self.select_vertex()		

		self.draw()