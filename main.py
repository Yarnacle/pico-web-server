import led
import webserver

led.on()

server = webserver.Webserver()
server.connect('RoseWoods-2G','ywcL5337,8')

server.listen()