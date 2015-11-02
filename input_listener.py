from direct.task.Task import Task

class delta_caller:

	def __init__(self,handle,trigger, index, value, cleanup_handle = None, cleanup_value = 0):
		self.handle = handle
		self.cleanup_handle = cleanup_handle
		self.trigger = trigger
		self.old_trigger = list(trigger)
		self.index = index
		self.trigger_activation = value
		self.cleanup_activation = cleanup_value

	def __call__(self,task):
		if self.trigger[self.index] != self.old_trigger[self.index]:
			self.old_trigger = list(self.trigger)

			if self.trigger[self.index] == self.trigger_activation:
				self.handle()

			if self.cleanup_handle != None:
				if self.trigger[self.index] == self.cleanup_activation:
					self.cleanup_handle()

		return Task.cont


class delta_caller_multikey:

	def __init__(self,handle,trigger, indices, values, cleanup_handle = None, cleanup_values = 0):
		self.handle = handle
		self.cleanup_handle = cleanup_handle
		self.trigger = trigger
		self.old_trigger = list(trigger)
		self.indices = indices
		self.trigger_activations = values
		self.cleanup_activations = cleanup_values
		self.active = False

	def __call__(self,task):
		if self.trigger[self.indices[0]] != self.old_trigger[self.indices[0]]:
			self.old_trigger = list(self.trigger)

			should_call_handle = True
			for i in range(len(self.indices)):
				ind = self.indices[i]
				if self.trigger[ind] != self.trigger_activations[i]:
					should_call_handle = False

			if should_call_handle:
				self.handle()
				self.active = True

			if self.cleanup_handle != None and self.active:
				should_call_cleanup = True
				for i in range(len(self.indices)):
					ind = self.indices[i]
					if self.trigger[ind] != self.cleanup_activations[i]:
						should_call_cleanup = False

				if should_call_cleanup:
					self.cleanup_handle()

		return Task.cont

class hold_caller_multikey:

	def __init__(self, trigger, indices, values, init_handle, loop_handle, cleanup_handle):
		self.activated = False
		
		self.trigger = trigger
		self.indices = indices
		self.trigger_activations = values

		self.init_handle = init_handle
		self.loop_handle = loop_handle
		self.cleanup_handle = cleanup_handle


	def __call__(self,task):
		
		if self.activated == False and self.trigger[self.indices[0]] == self.trigger_activations[0]:
		
			should_init = True
			for i in range(len(self.indices)):
				ind = self.indices[i]
				if self.trigger[ind] != self.trigger_activations[i]:
					should_init = False

			if should_init:	
				if self.init_handle != None:
					self.init_handle()
				self.activated = True
				return Task.cont


		if self.activated == True and self.trigger[self.indices[0]] == self.trigger_activations[0]:

			should_loop = True
			for i in range(len(self.indices)):
				ind = self.indices[i]
				if self.trigger[ind] != self.trigger_activations[i]:
					should_loop = False

			if should_loop:	
				if self.loop_handle != None:
					self.loop_handle()
				return Task.cont

		should_clean = False

		if self.activated:
			for i in range(len(self.indices)):
					ind = self.indices[i]
					if self.trigger[ind] != self.trigger_activations[i]:
						should_clean = True
						break

		if should_clean:

			if self.cleanup_handle != None:
				self.cleanup_handle()
			self.activated = False
			return Task.cont

		return Task.cont


class hold_caller:

	def __init__(self, trigger, index, value, init_handle, loop_handle, cleanup_handle):

		self.activated = False
		
		self.trigger = trigger
		self.index = index
		self.trigger_activation = value

		self.init_handle = init_handle
		self.loop_handle = loop_handle
		self.cleanup_handle = cleanup_handle

	def __call__(self,task):

		if self.activated == False and self.trigger[self.index] == self.trigger_activation:
			if self.init_handle != None:
				self.init_handle()
			self.activated = True

		if self.activated == True and self.trigger[self.index] == self.trigger_activation:
			if self.loop_handle != None:
				self.loop_handle()

		if self.activated == True and self.trigger[self.index] != self.trigger_activation:
			if self.cleanup_handle != None:
				self.cleanup_handle()
			self.activated = False

		return Task.cont

class toggle_caller:
	def __init__(self, trigger, index, value, init_handle, loop_handle, cleanup_handle):

		self.activated = False
		self.initialized = False
		
		self.trigger = trigger
		self.old_trigger = list(trigger)
		self.index = index
		self.trigger_activation = value

		self.init_handle = init_handle
		self.loop_handle = loop_handle
		self.cleanup_handle = cleanup_handle

	def __call__(self,task):

		if self.activated == True and self.trigger[self.index] == 0:
			if self.loop_handle != None:
				self.loop_handle()

		if self.trigger[self.index] != self.old_trigger[self.index]:
			self.old_trigger = list(self.trigger)

			if self.initialized == False and self.trigger[self.index] == self.trigger_activation:
				if self.init_handle != None:
					self.init_handle()
				self.initialized = True

			elif self.activated == False and self.initialized == True and self.trigger[self.index] != self.trigger_activation:
				self.activated = True;

			elif self.activated == True and self.trigger[self.index] != self.trigger_activation:
				if self.cleanup_handle != None:
					self.cleanup_handle()
				self.activated = False
				self.initialized = False

			else:
				pass

		return Task.cont
