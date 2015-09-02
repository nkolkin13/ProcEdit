from direct.showbase.ShowBase import ShowBase

from editor_enviroment import Edit_Env
import primitive_creation as pc
from camera_controller import Camera_Controller as CC
from keyboard_reader import Keyboard_Reader as KR


class ProcRen(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		self.keyboard_reader = KR(self)
		
		self.cam_control = CC(self)
		self.active_obj = pc.make_zig()


		self.switch_mode('edit_mesh')

	def switch_mode(self,mode):
		self.mode_cleanup()
		
		if mode == "edit_mesh":
			self.edit_env = Edit_Env(self,self.active_obj,'vertex')

		else:
			print "UNRECOGNIZED MODE, NOTHING DONE"

	def mode_cleanup(self):
		return 0

app = ProcRen()
app.run()