from panda3d.core import ModifierButtons

class Keyboard_Reader:

	def __init__(self, base):

		self.base = base
		self.key_map = {} 
		self.keys = []

		accepted_keys = ['shift', 'control', 'mouse1', 'mouse2', 'mouse3','space','wheel_up','wheel_down', 'g','s','r','e','/', 'x', 'y', 'z', '1', '2', '3', '5']
		base.mouseWatcherNode.set_modifier_buttons(ModifierButtons())
		base.buttonThrowers[0].node().set_modifier_buttons(ModifierButtons())


		index = 0
		for k in accepted_keys:
			self.key_map[k] = index
			self.keys.append(0)
			self.base.accept(k, self.setKeys, [index, 1])
			self.base.accept(k+'-up', self.setKeys, [index, 0])

			index += 1
	'''
		for k in shift_combo_keys:
			true_k = 'shift-'+k
			self.key_map[true_k] = index
			self.keys.append(0)
			self.base.accept(true_k, self.setKeys, [index, 1])
			self.base.accept(k+'-up', self.setKeys, [index, 0])
			self.base.accept('shift-up', self.setKeys, [index, 0])

			index += 1
	'''

	def setKeys(self,index,val):
		self.keys[index] = val


