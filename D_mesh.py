from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomPoints, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3
from panda3d.core import LineSegs
import util_PG

class d_vertex:
	def __init__(self,x,y,z):
		self.ID = None
		self.parent = None
		self.pos = Vec3(x,y,z)
		self.color = Vec4(0.5,0.5,0.5,1.0)
		self.norm = util_PG.norm(Vec3(x,y,z))

class d_edge:
	def __init__(self,v1,v2):
		self.ID = None	
		self.parent = None
		self.v1 = v1
		self.v2 = v2
		self.face = None
		self.twin = None
		self.next = None


class d_tri:
	def __init__(self,v1,v2,v3):
		self.ID = None
		self.parent = None
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

		self.verts = []
		self.n_verts = 0

		self.faces = []
		self.n_faces = 0

		self.edges = []
		self.n_edges = 0

	def add_vertex(self,x,y,z):
		v = d_vertex(x,y,z)
		v.parent = self
		v.ID = self.n_verts
		self.verts.append(v)
		self.n_verts += 1
		return v

	def add_edge(self,v1,v2):
		e = d_edge(v1,v2)
		e.ID = self.n_edges
		e.parent = self

		for e_o in self.edges:
			if (e_o.v1.ID == v2.ID and e_o.v2.ID == v1.ID) or (e_o.v1.ID == v1.ID and e_o.v2.ID == v2.ID):
				e.twin = e_o
				break

		self.edges.append(e)
		self.n_edges += 1
		return e

	def add_face(self, v1, v2, v3):
		f = d_tri(v1,v2,v3)
		f.ID = self.n_faces
		f.parent = self
		self.faces.append(f)
		self.n_edges += 1
		e1 = self.add_edge(v1,v2)
		e2 = self.add_edge(v2,v3)
		e3 = self.add_edge(v3,v1)
		e1.next = e2
		e2.next = e3
		e3.next = e1
		e1.face = f
		e2.face = f
		e3.face = f
		return f


	def draw(self):
		format=GeomVertexFormat.getV3n3cp()
		vdata=GeomVertexData('tri', format, Geom.UHDynamic)

		vertex=GeomVertexWriter(vdata, 'vertex')
		normal=GeomVertexWriter(vdata, 'normal')
		color=GeomVertexWriter(vdata, 'color')

		for v in self.verts:
			vertex.addData3f(v.pos.x,v.pos.y,v.pos.z)
			normal.addData3f(v.norm.x, v.norm.y, v.norm.z)
			color.addData4f(v.color[0],v.color[1],v.color[2],v.color[3])

		mesh = Geom(vdata)

		for f in self.faces:
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

	def draw_edges(self):
		line_drawer = LineSegs('line_drawer')
		line_drawer.setColor(0.0,0.0,0.0,1.0)
		line_drawer.setThickness(1.5)
		drawn_edges = set()
		for e in self.edges:
			if (not e.twin == None) and (e.twin.ID not in drawn_edges):
				line_drawer.moveTo(e.v1.pos)
				line_drawer.drawTo(e.v2.pos)
				drawn_edges.add(e.ID)

		edge_node = line_drawer.create()
		rendered_edges = render.attachNewNode(edge_node)

	def draw_verts(self):
		format=GeomVertexFormat.getV3cp()
		vdata=GeomVertexData('verts', format, Geom.UHDynamic)
		vertex=GeomVertexWriter(vdata, 'vertex')
		color=GeomVertexWriter(vdata, 'color')
		for v in self.verts:
			vertex.addData3f(v.pos.x,v.pos.y,v.pos.z)
			color.addData4f(0.0,0.0,0.0,1.0)
		
		mesh = Geom(vdata)
		points = GeomPoints(Geom.UHDynamic)
		for i in range(self.n_verts):
			points.addVertex(i)
		points.closePrimitive()
		mesh.addPrimitive(points)
		verts_node = GeomNode(self.name+'_verts')
		verts_node.addGeom(mesh)
		rendered_verts = render.attachNewNode(verts_node)
		rendered_verts.setRenderModeThickness(5.0)