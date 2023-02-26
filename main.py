import led
import webserver
from led_control.led_control import led_control

led.on()

server = webserver.Webserver()
server.connect('WIFI','PASSWORD')
server.path('/led',handler = led_control)

server.listen()
