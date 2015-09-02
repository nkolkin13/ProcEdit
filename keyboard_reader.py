

class Keyboard_Reader:

	def __init__(self, base):

		self.base = base
		self.key_map = {} 
		self.keys = []

		accepted_keys = ['shift', 'mouse1', 'mouse2', 'mouse3','space', '1', '2', '3', '5']
		shift_combo_keys = ['mouse1', 'mouse2', 'mouse3']



		index = 0
		for k in accepted_keys:
			self.key_map[k] = index
			self.keys.append(0)
			self.base.accept(k, self.setKeys, [index, 1])
			self.base.accept(k+'-up', self.setKeys, [index, 0])

			index += 1

		for k in shift_combo_keys:
			true_k = 'shift-'+k
			self.key_map[true_k] = index
			self.keys.append(0)
			self.base.accept(true_k, self.setKeys, [index, 1])
			self.base.accept(k+'-up', self.setKeys, [index, 0])
			self.base.accept('shift-up', self.setKeys, [index, 0])

			index += 1


	def setKeys(self,index,val):
		self.keys[index] = val


