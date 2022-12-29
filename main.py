import led
import webserver

led = led.LED()
led.on()

server = webserver.Webserver(led)
server.connect('RoseWoods-2G','ywcL5337,8')
server.listen()