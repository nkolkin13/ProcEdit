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
		e1 = v2.pos - v1.pos
		e2 = v3.pos - v1.pos		
		self.norm = util_PG.norm(e1.cross(e2))
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

	def add_vertex(self,x,y,z):
		v = d_vertex(x,y,z)
		v.ID = self.potential_vert_IDs.pop()
		self.verts[v.ID] = v
		self.n_verts += 1
		if len(self.potential_vert_IDs) < 1 :
			self.potential_vert_IDs.append(self.n_verts)
		return v

	def add_edge(self,v1,v2):
		e = d_edge(v1,v2)
		e.ID = self.potential_edge_IDs.pop()

		for e_o in self.edges.values():
			if (e_o.v1.ID == v2.ID and e_o.v2.ID == v1.ID) or (e_o.v1.ID == v1.ID and e_o.v2.ID == v2.ID):
				e.twin = e_o
				break

		self.edges[e.ID]=e
		self.n_edges += 1
		if len(self.potential_edge_IDs) < 1 :
			self.potential_edge_IDs.append(self.n_edges)
		return e

	def add_face(self, v1, v2, v3):
		f = d_tri(v1,v2,v3)
		f.ID = self.potential_face_IDs.pop()
		self.faces[f.ID] = f
		self.n_faces += 1
		e1 = self.add_edge(v1,v2)
		e2 = self.add_edge(v2,v3)
		e3 = self.add_edge(v3,v1)
		e1.next = e2
		e2.next = e3
		e3.next = e1
		e1.face = f
		e2.face = f
		e3.face = f
		if len(self.potential_face_IDs) < 1 :
			self.potential_face_IDs.append(self.n_faces)
		return f


	def draw(self):
		format=GeomVertexFormat.getV3n3cp()
		vdata=GeomVertexData('tri', format, Geom.UHDynamic)

		vertex=GeomVertexWriter(vdata, 'vertex')
		normal=GeomVertexWriter(vdata, 'normal')
		color=GeomVertexWriter(vdata, 'color')

		for v in self.verts.values():
			vertex.addData3f(v.pos.x,v.pos.y,v.pos.z)
			normal.addData3f(v.norm.x, v.norm.y, v.norm.z)
			color.addData4f(v.color[0],v.color[1],v.color[2],v.color[3])

		mesh = Geom(vdata)

		for f in self.faces.values():
			tri = GeomTriangles(Geom.UHDynamic)
			tri.addVertex(f.v1.ID)
			tri.addVertex(f.v2.ID)
			tri.addVertex(f.v3.ID)
			tri.closePrimitive()
			mesh.addPrimitive(tri)

		snode = GeomNode(self.name)
		snode.addGeom(mesh)
		rendered_mesh = render.attachNewNode(snode)
		rendered_mesh.setTwoSided(True)



