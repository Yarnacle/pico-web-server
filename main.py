import led
import webserver
from led_control.led_control import led_control

led.on()

server = webserver.Webserver()
server.connect('RoseWoods-2G','ywcL5337,8')
server.path('/led',handler = led_control)

server.listen()