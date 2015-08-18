#these are meant to be helper functions for creating and editing 3d geometry

from panda3d.core import GeomVertexFormat, GeomVertexData
from panda3d.core import Geom, GeomTriangles, GeomVertexWriter
from panda3d.core import Texture, GeomNode
from panda3d.core import Vec3, Vec4, Point3

#helper function for normalizing vectors
def norm(vec):
	vec.normalize()
	return vec

#helper function for creating a triangle
def createTriangle(v1, v2, v3, is_flat=False):
	x1 = v1.x
	y1 = v1.y
	z1 = v1.z

	x2 = v2.x
	y2 = v2.y
	z2 = v2.z

	x3 = v3.x
	y3 = v3.y
	z3 = v3.z

	format=GeomVertexFormat.getV3n3cp()
	vdata=GeomVertexData('tri', format, Geom.UHDynamic)

	vertex=GeomVertexWriter(vdata, 'vertex')
	normal=GeomVertexWriter(vdata, 'normal')
	color=GeomVertexWriter(vdata, 'color')

	vertex.addData3f(x1, y1, z1)
	vertex.addData3f(x2, y2, z2)
	vertex.addData3f(x3, y3, z3)

	if is_flat:
		normVector = norm(Vec3( (x1 + x2 + x3)/3.0, (y1 + y2 + y3)/3.0, (z1+ z2+ z3)/3.0))

		normal.addData3f(normVector)
		normal.addData3f(normVector)
		normal.addData3f(normVector)

	else:
		normal.addData3f(norm(Vec3(x1,y1,z1)))
		normal.addData3f(norm(Vec3(x2,y2,z2)))
		normal.addData3f(norm(Vec3(x3,y3,z3)))

	#adding different colors to the vertex for visibility
	color.addData4f(0.5,0.5,0.5,1.0)
	color.addData4f(0.5,0.5,0.5,1.0)
	color.addData4f(0.5,0.5,0.5,1.0)

	tri = GeomTriangles(Geom.UHDynamic)

	tri.addVertex(0)
	tri.addVertex(1)
	tri.addVertex(2)

	tri.closePrimitive()

	output_tri = Geom(vdata)
	output_tri.addPrimitive(tri)

	return output_tri

#helper function for making unit cube
def createCube():

	fnw = Vec3(1.0,1.0,-1.0)
	fne = Vec3(1.0,1.0,1.0)
	fsw = Vec3(1.0,-1.0,-1.0)
	fse = Vec3(1.0,-1.0,1.0)
	bnw = Vec3(-1.0,1.0,-1.0)
	bne = Vec3(-1.0,1.0,1.0)
	bsw = Vec3(-1.0,-1.0,-1.0)
	bse = Vec3(-1.0,-1.0,1.0)

	#define north
	tri1 = createTriangle(fnw,fne,bnw)
	tri2 = createTriangle(fne,bnw,bne)

	#define south
	tri3 = createTriangle(fsw,fse,bsw)
	tri4 = createTriangle(fse,bse,bsw)

	#define front face
	tri5 = createTriangle(fnw,fne,fsw)
	tri6 = createTriangle(fne,fsw,fse)

	#define back face
	tri7 = createTriangle(bnw,bne,bsw)
	tri8 = createTriangle(bne,bsw,bse)

	#define east face
	tri9 = createTriangle(bne,bse,fse)
	tri10 = createTriangle(fse,fne,bne)

	#define west face
	tri11 = createTriangle(bnw,bsw,fsw)
	tri12 = createTriangle(fsw,fnw,bnw)

	snode = GeomNode('cube')

	snode.addGeom(tri1)
	snode.addGeom(tri2)
	snode.addGeom(tri3)
	snode.addGeom(tri4)
	snode.addGeom(tri5)
	snode.addGeom(tri6)
	snode.addGeom(tri7)
	snode.addGeom(tri8)
	snode.addGeom(tri9)
	snode.addGeom(tri10)
	snode.addGeom(tri11)
	snode.addGeom(tri12)

	return snode

#helper function that takes in GeomNode and sends it to renderer
def renderObject(obj):
	rendered_obj = render.attachNewNode(obj)
	#rendered_obj.hprInterval(1.5,Point3(360,360,360)).loop()

	#OpenGl by default only draws "front faces" (polygons whose vertices are specified CCW).
	rendered_obj.setTwoSided(True)
