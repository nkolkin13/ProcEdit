from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3

#helper function for normalizing vectors
def norm(vec):
	vec.normalize()
	return vec

class WE_Edge:
	def __init__(self):
		self.iD = None
		self.parent = None
		self.origin = None
		self.dest = None
		self.left = None
		self.right = None
		self.origin_next = None
		self.origin_prev = None
		self.dest_next = None
		self.dest_prev = None
		self.sym = None


class WE_Vertex
	def __init__(self,x,y,z):
		self.iD = None
		self.parent = None
		self.edge = None
		self.coord = Vec3(x,y,z)
		self.color = Vec4(0.5,0.5,0.5,1.0)
		self.normal = norm(Vec3(x,y,z))

class WE_Face
	def __init__(self):
		self.iD = iD
		self.parent = parent
		self.edge = None

class WE_Object
	def __init__(self,name):
		self.name = name
		self.verts = []
		self.faces = []
		self.edges = []
		self.n_verts = 0
		self.n_edges = 0
		self.n_faces = 0
		self.smooth = True

	def check_vertex_status(self,v):
		if v.parent == self:
			return 0

		if v1.parent ~= None and v1.parent ~= self:
			print("ERROR: CANNOT CREATE EDGE USING VERTEX FROM ANOTHER OBJECT")
			return -1

		if v1.parent == None:
			self.n_verts += 1
			v1.iD = self.n_verts
			v1.parent = self
			self.verts.append(v1)
			return 1

		return 0


	def create_edge(self, v1, v2):

		#adds vertexes to object if they aren't already
		if self.check_vertex_status(v1) < 0 or self.check_vertex_status(v2) < 0:
			return -1

		self.n_edges += 1

		#create both half edges
		e1 = WE_Edge()
		e2 = WE_Edge()

		e1.parent = self
		e2.parent = self

		e1.iD = float(n_edges)
		e2.iD = float(n_edges) + 0.5

		e1.origin = v1
		e2.origin = v2

		e1.dest = v2
		e2.dest = v1

		e1.sym = e2
		e2.sym = e1


