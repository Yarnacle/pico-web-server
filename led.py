import machine

class LED:
	__led_pin = machine.Pin('LED',machine.Pin.OUT)
	state = False

	def __init__(self):
		pass

	def on(self):
		self.__led_pin.on()
		self.state = True

	def off(self):
		self.__led_pin.off()
		self.state = False
	
	def toggle(self):
		if self.state:
			self.off()
			return
		self.on()