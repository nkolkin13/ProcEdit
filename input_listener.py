from direct.task.Task import Task

class delta_caller:

	def __init__(self,handle,trigger, index, value, cleanup_handle = None, cleanup_value = None):
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
		
		self.trigger = trigger
		self.old_trigger = list(trigger)
		self.index = index
		self.trigger_activation = value

		self.init_handle = init_handle
		self.loop_handle = loop_handle
		self.cleanup_handle = cleanup_handle

	def __call__(self,task):

		if self.activated == True and self.trigger[self.index] == self.old_trigger[self.index]:
			if self.loop_handle != None:
				self.loop_handle()

		if self.trigger[self.index] != self.old_trigger[self.index]:
			self.old_trigger = list(self.trigger)

			if self.activated == False and self.trigger[self.index] == self.trigger_activation:
				if self.init_handle != None:
					self.init_handle()
				self.activated = True

			if self.activated == True and self.trigger[self.index] == self.trigger_activation:
				if self.cleanup_handle != None:
					self.cleanup_handle()
				self.activated = False

		return Task.cont
