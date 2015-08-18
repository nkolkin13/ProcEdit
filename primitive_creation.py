from D_mesh import d_mesh, d_vertex, d_tri

def make_cube():
	cube = d_mesh('cube')
	aaa = cube.add_vertex(1.0,1.0,1.0)
	aab = cube.add_vertex(1.0,1.0,-1.0)
	aba = cube.add_vertex(1.0,-1.0,1.0)
	abb = cube.add_vertex(1.0,-1.0,-1.0)
	baa = cube.add_vertex(-1.0,1.0,1.0)
	bab = cube.add_vertex(-1.0,1.0,-1.0)
	bba = cube.add_vertex(-1.0,-1.0,1.0)
	bbb = cube.add_vertex(-1.0,-1.0,-1.0)

	cube.add_face(aaa,aab,abb)
	cube.add_face(aba,aaa,abb)
	cube.add_face(bba,aaa,aba)
	cube.add_face(baa,aaa,bba)
	cube.add_face(bab,baa,aaa)
	cube.add_face(bab,aaa,aab)
	cube.add_face(bbb,bab,aab)
	cube.add_face(bbb,aab,abb)
	cube.add_face(bbb,aba,abb)
	cube.add_face(bbb,bba,aba)
	cube.add_face(bbb,bba,baa)
	cube.add_face(bbb,baa,bab)

	cube.draw()
	cube.draw_edges()
	cube.draw_verts()

	return cube

def make_zig():
	cube = d_mesh('cube')
	aaa = cube.add_vertex(0.5,0.5,1.0)
	aab = cube.add_vertex(1.0,1.0,-1.0)
	aba = cube.add_vertex(0.5,-0.5,1.0)
	abb = cube.add_vertex(1.0,-1.0,-1.0)
	baa = cube.add_vertex(-0.5,0.5,1.0)
	bab = cube.add_vertex(-1.0,1.0,-1.0)
	bba = cube.add_vertex(-0.5,-0.5,1.0)
	bbb = cube.add_vertex(-1.0,-1.0,-1.0)

	cube.add_face(aaa,aab,abb)
	cube.add_face(aba,aaa,abb)
	cube.add_face(bba,aaa,aba)
	cube.add_face(baa,aaa,bba)
	cube.add_face(bab,baa,aaa)
	cube.add_face(bab,aaa,aab)
	cube.add_face(bbb,bab,aab)
	cube.add_face(bbb,aab,abb)
	cube.add_face(bbb,aba,abb)
	cube.add_face(bbb,bba,aba)
	cube.add_face(bbb,bba,baa)
	cube.add_face(bbb,baa,bab)

	cube.draw()
	cube.draw_edges()
	cube.draw_verts()

	return cube