from input_listener import *
from panda3d.core import Vec3, Vec4, Point3, Point2
import math
import cmath
import util_PG

class edit_tool:
	def __init__(self, selection):
		self.name = 'generic'
		self.mesh = selection.mesh
		self.base = selection.base
		self.selection = selection
		self.tool_registered = False
		self.axis_lock = None

	def register_tool(self, keys, key_map, activation_type, button):

		self.keys = keys
		self.key_map = key_map

		if self.tool_registered == False:
			
			if activation_type == "hold":
				self.base.taskMgr.add(hold_caller(trigger=keys, index=key_map[button], value = 1, init_handle=self.init_action, loop_handle=self.loop_action, cleanup_handle = self.cleanup_action), self.name+"_tool_task")
				self.tool_registered = True

			elif activation_type == "toggle":
				self.base.taskMgr.add(toggle_caller(trigger=keys, index=key_map[button], value = 1, init_handle=self.init_action, loop_handle=self.loop_action, cleanup_handle = self.cleanup_action), self.name+"_tool_task")
				self.tool_registered = True

			elif activation_type == "delta":
				self.base.taskMgr.add(delta_caller(handle = self.init_action ,trigger=keys, index=key_map[button], value=1, cleanup_handle = self.cleanup_action, cleanup_value = 0), self.name+"_tool_task")
				self.tool_registered = True

			else:
				print "UNKNOWN ACTIVATION TYPE FOR TOOL "+self.name+": NOT REGISTERED"



	def toggle_lock_axis(self,axis):
		if self.axis_lock == axis:
			self.axis_lock = None
		else:
			self.axis_lock = axis

	def toggle_lock_axis_x(self):
		self.toggle_lock_axis('x')

	def toggle_lock_axis_y(self):
		self.toggle_lock_axis('y')

	def toggle_lock_axis_z(self):
		self.toggle_lock_axis('z')

	def add_axis_lock_listeners(self):
		self.base.taskMgr.add(delta_caller(handle = self.toggle_lock_axis_x ,trigger=self.keys, index=self.key_map['x'], value=1), self.name+"_x_axis_lock_task")
		self.base.taskMgr.add(delta_caller(handle = self.toggle_lock_axis_y ,trigger=self.keys, index=self.key_map['y'], value=1), self.name+"_y_axis_lock_task")
		self.base.taskMgr.add(delta_caller(handle = self.toggle_lock_axis_z ,trigger=self.keys, index=self.key_map['z'], value=1), self.name+"_z_axis_lock_task")

	def remove_axis_lock_listeners(self):
		self.base.taskMgr.remove(self.name+"_x_axis_lock_task")
		self.base.taskMgr.remove(self.name+"_y_axis_lock_task")
		self.base.taskMgr.remove(self.name+"_z_axis_lock_task")


	def init_action(self):
		return 0

	def loop_action(self):
		return 0

	def cleanup_action(self):
		return 0

	def set_mouse_origin(self):
		if self.base.mouseWatcherNode.hasMouse():
			self.mouse_origin = Point2(self.base.mouseWatcherNode.getMouse())


class grab_tool(edit_tool):
	def __init__(self, selection):
		edit_tool.__init__(self, selection)
		self.name = 'grab'

	def init_action(self):
		self.add_axis_lock_listeners()
		self.set_mouse_origin()
		self.vert_IDS = sorted(list(self.selection.selected_vertices))
		self.original_vert_positions = []
		for vID in self.vert_IDS:
			self.original_vert_positions.append(self.mesh.verts[vID].pos)

	def loop_action(self):
		if self.base.mouseWatcherNode.hasMouse():

			mpos = Point2(self.base.mouseWatcherNode.getMouse())
			delta = mpos - self.mouse_origin


			near_dist = self.base.cam.node().getLens().getNear()
			up_vec = self.base.cam.getMat().getRow3(2)
			side_vec = self.base.cam.getMat().getRow3(0)

			i = 0
			for id in self.vert_IDS:
				#TODO: interact with selection struct/class
				selected_obj = self.mesh.verts[id]

				#TODO, do this to average for efficiency
				far_dist = (self.base.cam.getPos()-self.original_vert_positions[i]).length()

				factor = (far_dist-near_dist)/3.0

				if self.axis_lock == None:
					up_delta = up_vec * factor * delta.y
					side_delta = side_vec * factor * delta.x
					selected_obj.pos = (self.original_vert_positions[i]+up_delta+side_delta)

				if self.axis_lock == 'x':
					x_delta = Vec3(1.0, 0.0, 0.0) * factor * delta.x
					selected_obj.pos = (self.original_vert_positions[i]+x_delta)

				if self.axis_lock == 'y':
					y_delta = Vec3(0.0, 1.0, 0.0) * factor * delta.x
					selected_obj.pos = (self.original_vert_positions[i]+y_delta)

				if self.axis_lock == 'z':
					z_delta = Vec3(0.0, 0.0, 1.0) * factor * delta.x
					selected_obj.pos = (self.original_vert_positions[i]+z_delta)

				i+=1

			self.selection.recalculate_average(self.mesh.verts.values())
			self.mesh.draw()
			self.selection.draw()

	def cleanup_action(self):
		self.remove_axis_lock_listeners()
		self.axis_lock = None
		self.mouse_origin = None
		self.vert_IDS = None
		self.original_vert_positions = None


class scale_tool(edit_tool):
	def __init__(self, selection):
		edit_tool.__init__(self, selection)
		self.name = 'scale'

	def calculate_scaling_vectors(self,center_point):
		vecs = []
		for vID in self.vert_IDS:
			vecs.append(self.mesh.verts[vID].pos-center_point)
		
		return vecs

	def init_action(self):
		self.add_axis_lock_listeners()
		self.set_mouse_origin()
		self.vert_IDS = sorted(list(self.selection.selected_vertices))
		self.original_vert_positions = []
		for vID in self.vert_IDS:
			self.original_vert_positions.append(self.mesh.verts[vID].pos)

		self.scaling_vectors = self.calculate_scaling_vectors(self.selection.average_position)

	def loop_action(self):
		if self.base.mouseWatcherNode.hasMouse():

			mpos = Point2(self.base.mouseWatcherNode.getMouse())
			delta = mpos - self.mouse_origin


			near_dist = self.base.cam.node().getLens().getNear()
			up_vec = self.base.cam.getMat().getRow3(2)
			side_vec = self.base.cam.getMat().getRow3(0)

			i = 0
			for id in self.vert_IDS:
				#TODO: interact with selection struct/class
				selected_obj = self.mesh.verts[id]

				#TODO, do this to average for efficiency
				far_dist = (self.base.cam.getPos()-self.original_vert_positions[i]).length()

				factor = (far_dist-near_dist)/3.0

				if self.axis_lock == None:
					selected_obj.pos = self.selection.average_position + (self.scaling_vectors[i] * (delta.x+1))

				if self.axis_lock == 'x':
					selected_obj.pos = self.original_vert_positions[i] + (self.scaling_vectors[i].project(Vec3(1.0,0.0,0.0)) * (delta.x+1))

				if self.axis_lock == 'y':
					selected_obj.pos = self.original_vert_positions[i] + (self.scaling_vectors[i].project(Vec3(0.0,1.0,0.0)) * (delta.x+1))

				if self.axis_lock == 'z':
					selected_obj.pos = self.original_vert_positions[i] + (self.scaling_vectors[i].project(Vec3(0.0,0.0,1.0)) * (delta.x+1))


				i+=1

			self.mesh.draw()
			self.selection.draw()

	def cleanup_action(self):
		self.remove_axis_lock_listeners()
		self.axis_lock = None
		self.mouse_origin = None
		self.vert_IDS = None
		self.original_vert_positions = None
		self.scaling_vectors = None


class rotate_tool(edit_tool):
	def __init__(self, selection):
		edit_tool.__init__(self, selection)
		self.name = 'rotate'


	def calculate_scaling_vectors(self,center_point):
		vecs = []
		for vID in self.vert_IDS:
			vecs.append(self.mesh.verts[vID].pos-center_point)
		
		return vecs

	def init_action(self):
		self.add_axis_lock_listeners()
		self.set_mouse_origin()
		self.vert_IDS = sorted(list(self.selection.selected_vertices))
		self.original_vert_positions = []
		for vID in self.vert_IDS:
			self.original_vert_positions.append(self.mesh.verts[vID].pos)

		self.scaling_vectors = self.calculate_scaling_vectors(self.selection.average_position)


	def loop_action(self):
		if self.base.mouseWatcherNode.hasMouse():

			mpos = Point2(self.base.mouseWatcherNode.getMouse())
			delta = mpos - self.mouse_origin


			near_dist = self.base.cam.node().getLens().getNear()

			if self.axis_lock == None:
				up_vec = self.base.cam.getMat().getRow3(2)
				side_vec = self.base.cam.getMat().getRow3(0)

			if self.axis_lock == 'x':
				up_vec = Vec3(0.0,0.0,1.0)
				side_vec = Vec3(0.0,1.0,0.0)

			if self.axis_lock == 'y':
				up_vec = Vec3(0.0,0.0,1.0)
				side_vec = Vec3(1.0,0.0,0.0)

			if self.axis_lock == 'z':
				up_vec = Vec3(1.0,0.0,0.0)
				side_vec = Vec3(0.0,1.0,0.0)


			t = delta.x * 4

			i = 0

			for id in self.vert_IDS:
				#TODO: interact with selection struct/class
				selected_obj = self.mesh.verts[id]

				#TODO, do this to average for efficiency
				far_dist = (self.base.cam.getPos()-self.original_vert_positions[i]).length()

				factor = (far_dist-near_dist)/3.0

				vec = self.scaling_vectors[i]


				vec_rotate = vec.project(up_vec) + vec.project(side_vec)
				#L = vec.length()

				
				L = vec_rotate.length()

				o_t = math.atan2(vec_rotate.dot(up_vec),vec_rotate.dot(side_vec))

				param_1 = L * math.cos( o_t + t)
				param_2 = L * math.sin( o_t + t)

				orthagonal_component = self.selection.average_position.project(up_vec.cross(side_vec)) + vec.project(up_vec.cross(side_vec))
				rotational_component = (self.selection.average_position.project(up_vec)+ self.selection.average_position.project(side_vec) + (up_vec * param_2) + (side_vec * param_1))

				selected_obj.pos = orthagonal_component + rotational_component

				i+=1

			self.mesh.draw()
			self.selection.draw()

	def cleanup_action(self):
		self.remove_axis_lock_listeners()
		self.axis_lock = None
		self.mouse_origin = None
		self.vert_IDS = None
		self.original_vert_positions = None
		self.scaling_vectors = None

class extrude_tool(edit_tool):

	def __init__(self, selection):
		edit_tool.__init__(self, selection)
		self.name = 'extrude'

	def init_action(self):

		if len(self.selection.selected_faces) < 1:
			return 0

		self.set_mouse_origin()

		self.average_normal = None
		for f in [self.mesh.faces[ID] for ID in self.selection.selected_faces]:
			if self.average_normal == None:
				self.average_normal = f.norm
			else:
				self.average_normal = self.average_normal + f.norm

		self.average_normal = self.average_normal / len(self.selection.selected_faces)


		v_mapping = {}

		old_loop = []

		for v in [self.mesh.verts[ID] for ID in list(self.selection.selected_vertices)]:
			new_v = self.mesh.add_vertex(v.pos.x,v.pos.y,v.pos.z)
			v_mapping[v.ID] = new_v.ID

		f_list = list([self.mesh.faces[ID] for ID in list(self.selection.selected_faces)])
		
		e_list = list([self.mesh.edges[ID] for ID in list(self.selection.selected_edges)])

		for e in e_list:
			if (e.v1.ID in self.selection.selected_vertices) and (e.v2.ID in self.selection.selected_vertices) and ((e.face == None) or (e.face.ID not in self.selection.selected_faces)):
				old_loop.append(e.ID)

		for f in f_list:
			v1_ID = v_mapping[f.v1.ID]
			v2_ID = v_mapping[f.v2.ID]
			v3_ID = v_mapping[f.v3.ID]

			v1 = self.mesh.verts[v1_ID]
			v2 = self.mesh.verts[v2_ID]
			v3 = self.mesh.verts[v3_ID]
			self.mesh.add_face(v1,v2,v3)

		for f in f_list:
			self.mesh.remove_component("face", f.ID)

		for e_ID in old_loop:
			old_e = self.mesh.edges[e_ID]
			v1_new = self.mesh.verts[v_mapping[old_e.v1.ID]]
			v2_new = self.mesh.verts[v_mapping[old_e.v2.ID]]
			self.mesh.add_face(old_e.v1,old_e.v2,v2_new)
			self.mesh.add_face(old_e.v1,v2_new,v1_new)


		self.selection.selected_vertices = set()
		self.selection.selected_edges = set()
		self.selection.selected_faces = set()

		for v_ID in v_mapping.values():
			self.selection.add_vertex(self.mesh.verts[v_ID])

		self.vert_IDS = sorted(list(self.selection.selected_vertices))
		self.original_vert_positions = []
		for vID in self.vert_IDS:
			self.original_vert_positions.append(self.mesh.verts[vID].pos)

		self.mesh.draw()
		self.selection.draw()

	def loop_action(self):
		if self.base.mouseWatcherNode.hasMouse():

			mpos = Point2(self.base.mouseWatcherNode.getMouse())
			delta = mpos - self.mouse_origin

			i = 0
			for id in self.vert_IDS:
				#TODO: interact with selection struct/class
				selected_obj = self.mesh.verts[id]
				
				selected_obj.pos = self.original_vert_positions[i] + (self.average_normal * (delta.x))

				i+=1

			self.selection.recalculate_average(self.mesh.verts.values())
			self.mesh.draw()
			self.selection.draw()

	def cleanup_action(self):
		self.mouse_origin = None
		self.vert_IDS = None
		self.original_vert_positions = None
		self.average_normal = None

class subdivide_tool(edit_tool):

	def __init__(self, selection):
		edit_tool.__init__(self, selection)
		self.name = 'subdivide_tool'

	def init_action(self):

		if len(self.selection.selected_edges) < 1:
			return 0

		completed_edges = []

		for f_ID in list(self.selection.selected_faces):

			f = self.mesh.faces[f_ID]
			e1 = f.edge
			e2 = f.edge.next
			e3 = f.edge.next.next
			v1 = e1.v1
			v2 = e2.v1
			v3 = e3.v1

			new_v_pos = (v1.pos + v2.pos + v3.pos)/3
			new_v = self.mesh.add_vertex( new_v_pos.x, new_v_pos.y, new_v_pos.z)

			self.mesh.add_face(v1, v2, new_v)
			self.mesh.add_face(v2, v3, new_v)
			self.mesh.add_face(v3, v1, new_v)

			self.mesh.remove_component("face", f.ID)

		self.mesh.find_edge_twins()

		for e_ID in list(self.selection.selected_edges):

			if e_ID not in completed_edges:
				pass
			else:
				continue

			print "ID:",e_ID
			e_old = self.mesh.edges[e_ID]
			print "TWIN ID:",e_old.twin.ID

			completed_edges.append(e_old.ID)
			completed_edges.append(e_old.twin.ID)

			new_v_pos = (e_old.v1.pos + e_old.v2.pos) / 2
			new_v = self.mesh.add_vertex( new_v_pos.x, new_v_pos.y, new_v_pos.z)

			#perform subdivision on this edge
			v_opposite = e_old.next.v2
			f_old = e_old.face

			self.mesh.add_face(new_v,v_opposite,e_old.v1)
			self.mesh.add_face(new_v,v_opposite,e_old.v2)

			
			#perform subdivision on twin edge
			e_old_twin = self.mesh.edges[e_ID].twin
			v_opposite_twin = e_old_twin.next.v2
			f_old_twin = e_old_twin.face

			self.mesh.add_face(new_v,v_opposite_twin,e_old_twin.v1)
			self.mesh.add_face(new_v,v_opposite_twin,e_old_twin.v2)
			

			self.mesh.remove_component("face", f_old.ID)
			self.mesh.remove_component("face", f_old_twin.ID)

		self.mesh.find_edge_twins()

		self.selection.selected_vertices = set()
		self.selection.selected_edges = set()
		self.selection.selected_faces = set()

		self.mesh.draw()
		self.selection.draw()
