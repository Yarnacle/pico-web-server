import webserver
import led

def led_control(request):
	if request.type == 'GET':
		pass

	elif request.type == 'POST':
		form_data = request.parse_form()
		if form_data['led-field'] == 'On':
			led.on()
		elif form_data['led-field'] == 'Off':
			led.off()

	context = {
		'led_state': 'ON' if led.state else 'OFF'
	}
	return webserver.pass_context(webserver.get_html('led_control/led_control.html'),context)