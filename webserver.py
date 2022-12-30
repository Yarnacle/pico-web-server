import network
import socket
import time
import led
from collections import namedtuple
import re

def get_html(path):
	with open(path) as html:
		return html.read()

def pass_context(html,context):
	for key in context:
		html = re.sub(r'{{\s*' + key + r'\s*}}',context[key],html)
	return html

class Webserver:
	def __init__(self):
		self.pages = {
			'/': lambda *args: get_html('index.html')
		}


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

	def path(self,url_path,**kwargs):
		if not 'handler' in kwargs:
			handler = lambda: get_html(f'{url_path}.html')
		else:
			handler = kwargs['handler']
		self.pages[url_path] = handler

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
				request = Request(client.recv(1024))
				print(f'{request.rawtext.split("\r\n")[0]} from {ip[0]}:{ip[1]}')

				try:
					handler = self.pages[request.target]
					try:
						response = handler(request)
					except:
						response = '<h1>An unexpected error occured</h1>'

				except KeyError:
					response = '<h1>Error 404: not found</h1>'
				except:
					response = '<h1>An unexpected error occured</h1>'

				client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
				client.send(response)
				client.close()

			except OSError:
				client.close()
				print('Connection closed')

class Request:
	def __init__(self,raw):
		try:
			self.rawtext = raw.decode('utf-8')
		except:
			self.rawtext = raw
		line_list = self.rawtext.split('\r\n')
		line = line_list[0].split(' ')
		self.type,self.target,self.status = line[0],line[1],' '.join(line[2:])

		header_dict = {header.split(': ')[0].replace('-','_'): header.split(': ')[1] for header in line_list[1:line_list.index('')] if header}
		HeaderField = namedtuple('HeaderField',list([header_name.replace('-','_') for header_name in header_dict.keys()]))
		self.headers =  HeaderField(**header_dict)
		self.body = line_list[line_list.index('') + 1]
	
	def parse_form(self):
		field_list = self.body.split('&')
		return {field.split('=')[0]: field.split('=')[1] for field in field_list}
	
	def __str__(self):
		return self.rawtext