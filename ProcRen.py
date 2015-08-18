from direct.showbase.ShowBase import ShowBase

from editor_enviroment import Edit_Env
import primitive_creation as pc
from camera_controller import Camera_Controller as CC

class ProcRen(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		cam_control = CC(self)
		edit_Env = Edit_Env()
		cube = pc.make_zig()



app = ProcRen()
app.run()