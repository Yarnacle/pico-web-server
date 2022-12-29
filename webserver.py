import network
import socket
import time
import led

class Webserver:
	def __init__(self):
		pass

	def connect(self,ssid,password):
		wlan = network.WLAN(network.STA_IF)
		wlan.active(True)
		wlan.connect(ssid,password)

		print('Waiting for connection...')

		max_wait = 10
		while max_wait > 0:
			led.toggle()
			if wlan.status() < 0 or wlan.status() >= 3:
				break
			max_wait -= 1
			time.sleep(1)

		led.on()

		if wlan.status() != 3:
			raise RuntimeError('Network connection failed')
		else:
			status = wlan.ifconfig()
			print(f'Connected to {ssid}')
			global network_ip
			network_ip = status[0]

	def listen(self):
		ip = socket.getaddrinfo('0.0.0.0',80)[0][-1]
		connection = socket.socket()
		connection.bind(ip)
		connection.listen(1)
		print()
		print(f'Listening on {network_ip}')

		while True:
			try:
				global client
				client,ip = connection.accept()
				print(f'Client connected from {ip}')

				request = str(client.recv(1024))
				with open('index.html','r') as html:
					response = html.read()

				client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
				client.send(response)
				client.close()

			except OSError:
				client.close()
				print('Connection closed')