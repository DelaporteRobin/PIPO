import os
import sys
import site

#check that the site user package is installed in path
site_package = site.getusersitepackages()
if site_package not in sys.path:
	sys.path.append(site_package)

#import other libraries
import socket
import rich
import threading
import json
import traceback

from rich.console import Console
from rich.text import Text
from functools import partial


class BlenderListener:
	def __init__(self):
		self.HOST = "127.0.0.1"
		self.PORT = 9010
		self.BUFFER = 8192

		#create the rich console and defined the colors
		self.console = Console()
		#create rich colors
		self.COLORS = {
			"success":"#C5F527",
			"warning":"#F5AD27",
			"error":"#F52738",
			"notification": "#DE3ABB",
		}



	def create_socket(self):
		self.console.print("Socket creation started...", style=self.COLORS["notification"])

		try:
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				#force stop of the socket if already used
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
				s.bind((self.HOST, self.PORT))
				s.listen()

				while True:
					connection, data = s.accept()
					self.handle_client(connection, data)
		except:
			self.console.print(f"Impossible to open socket\n{traceback.format_exc()}", style=self.COLORS["error"])
			return



			
	def handle_client(self, connection=None, data=None):
		#portal to send the command received to blender main thread
		def blender_task():
			print(f"trying to execute the command: {command}")
			#reponse_container["data"] = send_command_to_blender(command, command_data)
			return None

		self.console.print(f'[{self.COLORS["notification"]}] New client connected →[/] {connection}')
		#self.console.print(f'[{self.COLORS["notification"]} bold] New client conected [/]')

		with connection:
			raw = connection.recv(self.BUFFER)
			if not raw:
				return

			#capture the command and parse content
			request = json.loads(raw.decode())
			command = request.get("cmd")
			command_data = request.get("data", {})

			#try to execute the command in blender
			bpy.app.timers.register(self.blender_task)

			connection.sendall("Command received".encode())


	def create_main_thread(self):
		self.listener_thread = threading.Thread(target=self.create_socket, daemon=True)
		self.listener_thread.start()

listener_called = BlenderListener()
listener_called.create_main_thread()