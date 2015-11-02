from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomPoints, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3
from panda3d.core import LineSegs
import util_PG

class d_vertex:
	def __init__(self,x,y,z):
		self.ID = None
		self.pos = Vec3(x,y,z)
		self.color = Vec4(0.5,0.5,0.5,1.0)
		self.norm = util_PG.norm(Vec3(x,y,z))
		self.n_refs = 0

class d_edge:
	def __init__(self,v1,v2):
		self.ID = None	
		self.v1 = v1
		self.v2 = v2
		self.face = None
		self.twin = None
		self.next = None


class d_tri:
	def __init__(self,v1,v2,v3):
		self.ID = None
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.edge = None	
		self.flat = False


#This is the base class for a drawable 3d mesh
class d_mesh:
	def __init__(self,name):
		self.name = name

		self.verts = {}
		self.n_verts = 0
		self.potential_vert_IDs = [0]  

		self.faces = {}
		self.n_faces = 0
		self.potential_face_IDs = [0]  


		self.edges = {}
		self.n_edges = 0
		self.potential_edge_IDs = [0]

		self.rendered_mesh = None

	def remove_vertex_core(self,ID):
		if ID in self.verts.keys():
			del self.verts[ID]
			self.potential_vert_IDs.append(ID)
			self.n_verts -= 1
		else: 
			print "NO VERTEX WITH ID '"+str(ID)+"' EXISTS, NOTHING DONE"

	def remove_edge_core(self,ID):
		if ID in self.edges.keys():
			self.edges[ID].v1.n_refs -= 1
			self.edges[ID].v2.n_refs -= 1			
			del self.edges[ID]
			self.potential_edge_IDs.append(ID)
			self.n_edges -= 1
		else: 
			print "NO EDGE WITH ID '"+str(ID)+"' EXISTS, NOTHING DONE"

	def remove_face_core(self,ID):
		if ID in self.faces.keys():
			del self.faces[ID]
			self.potential_face_IDs.append(ID)
			self.n_faces -= 1
		else: 
			print "NO FACE WITH ID '"+str(ID)+"' EXISTS, NOTHING DONE"


	def remove_zref_verts(self):
		for v in list(self.verts.values()):
			if v.n_refs == 0:
				self.remove_vertex_core(v.ID)


	def remove_vertex(self,ID):
		for e_ID in list(self.edges.keys()):
			e_temp = self.edges[e_ID]
			if e_temp.v1.ID == ID or e_temp.v2.ID == ID:
				remove_edge(ID)

	def remove_edge(self, ID):
		e_temp = self.edges[ID]
		self.remove_face_core(e_temp.face.ID)
		self.remove_edge_core(ID)

	#ONLY WORKS FOR TRIANGLES
	def remove_face(self, ID):
		f_temp = self.faces[ID]
		e1_ID = f_temp.edge.ID
		e2_ID = f_temp.edge.next.ID
		e3_ID = f_temp.edge.next.next.ID
		self.remove_edge_core(e1_ID)
		self.remove_edge_core(e2_ID)
		self.remove_edge_core(e3_ID)
		self.remove_face_core(ID)

	# Only call this function to remove stuff
	def remove_component(self,type,ID):
		if type == "vertex":
			self.remove_vertex(ID)

		elif type == "edge":
			self.remove_edge(ID)

		elif type == "face":
			self.remove_face(ID)

		else:
			print "TYPE NOT RECOGNIZED, NO COMPONENT REMOVED"
			return 0

		self.remove_zref_verts()

	def find_edge_twins(self):
		for e in self.edges.values():
			for e_o in self.edges.values():
				if (e.ID != e_o.ID) and (e_o.v1.ID == e.v2.ID and e_o.v2.ID == e.v1.ID) or (e_o.v1.ID == e.v1.ID and e_o.v2.ID == e.v2.ID):
					e.twin = e_o
					e_o.twin = e
					break	

	def add_vertex(self,x,y,z):
		v = d_vertex(x,y,z)
		v.ID = self.potential_vert_IDs.pop()
		self.verts[v.ID] = v
		self.n_verts += 1
		if len(self.potential_vert_IDs) < 1 :
			self.potential_vert_IDs.append(self.n_verts)
		return v

	def add_half_edge(self,v1,v2):

		e = d_edge(v1,v2)

		self.verts[v1.ID].n_refs += 1
		self.verts[v2.ID].n_refs += 1

		e.ID = self.potential_edge_IDs.pop()

		for e_o in self.edges.values():
			if (e_o.ID  != e.ID) and (e_o.v1.ID == v2.ID and e_o.v2.ID == v1.ID) or (e_o.v1.ID == v1.ID and e_o.v2.ID == v2.ID):
				e.twin = e_o
				e_o.twin = e
				break

		self.edges[e.ID]=e
		self.n_edges += 1
		if len(self.potential_edge_IDs) < 1 :
			self.potential_edge_IDs.append(self.n_edges)

		self.find_edge_twins()

		return e


	def add_face(self, v1, v2, v3):

		f = d_tri(v1,v2,v3)
		f.ID = self.potential_face_IDs.pop()
		self.faces[f.ID] = f
		self.n_faces += 1
		e1 = self.add_half_edge(v1,v2)
		e2 = self.add_half_edge(v2,v3)
		e3 = self.add_half_edge(v3,v1)
		e1.next = e2
		e2.next = e3
		e3.next = e1
		e1.face = f
		e2.face = f
		e3.face = f
		f.edge = e1

		vec_e1 = v2.pos-v1.pos
		vec_e3 = v3.pos-v1.pos
		f.norm = util_PG.norm(vec_e1.cross(vec_e3))
		if len(self.potential_face_IDs) < 1 :
			self.potential_face_IDs.append(self.n_faces)

		self.find_edge_twins()

		return f

	def reset_draw(self):
		self.rendered_mesh.removeNode()
		self.rendered_mesh = None

	def draw(self):
		if self.rendered_mesh != None:
			self.reset_draw()

		format=GeomVertexFormat.getV3n3cp()
		vdata=GeomVertexData('tri', format, Geom.UHDynamic)

		vertex=GeomVertexWriter(vdata, 'vertex')
		normal=GeomVertexWriter(vdata, 'normal')
		color=GeomVertexWriter(vdata, 'color')
		v_mapping = {}

		i=0
		for v in self.verts.values():
			vertex.addData3f(v.pos.x,v.pos.y,v.pos.z)
			normal.addData3f(v.norm.x, v.norm.y, v.norm.z)
			color.addData4f(v.color[0],v.color[1],v.color[2],v.color[3])
			v_mapping[v.ID] = i
			i += 1

		mesh = Geom(vdata)

		for f in self.faces.values():
			tri = GeomTriangles(Geom.UHDynamic)
			tri.addVertex(v_mapping[f.v1.ID])
			tri.addVertex(v_mapping[f.v2.ID])
			tri.addVertex(v_mapping[f.v3.ID])
			tri.closePrimitive()
			mesh.addPrimitive(tri)

		snode = GeomNode(self.name)
		snode.addGeom(mesh)
		self.rendered_mesh = render.attachNewNode(snode)
		self.rendered_mesh.setTwoSided(True)



