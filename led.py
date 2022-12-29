import machine

__led_pin = machine.Pin('LED',machine.Pin.OUT)
state = not not __led_pin.value()

def on():
	global state
	__led_pin.on()
	state = True

def off():
	global state
	__led_pin.off()
	state = False

def toggle():
	if state:
		off()
		return
	on()