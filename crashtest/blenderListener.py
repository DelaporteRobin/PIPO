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
import bpy

BLENDER_DIRECTORY = os.path.dirname(bpy.data.filepath)
BLENDER_FILEPATH = bpy.data.filepath
SCRIPT_PATH = os.path.abspath(os.path.join(BLENDER_DIRECTORY, ".."))

os.system("cls")
print("SCRIPT PATH : %s"%SCRIPT_PATH)
if SCRIPT_PATH not in sys.path:
	sys.path.append(SCRIPT_PATH)

from rich.console import Console
from rich.text import Text
from functools import partial

from src.BlenderOperator import BlenderOperator


class BlenderListener(BlenderOperator):
	def __init__(self):
		
		self.HOST = "127.0.0.1"
		self.PORT = 9010
		self.BUFFER = 8192
		

		#create a kill switch
		self.KILL = False

		#create the rich console and defined the colors
		self.console = Console()
		#create rich colors
		self.COLORS = {
			"success":"#C5F527",
			"warning":"#F5AD27",
			"error":"#F52738",
			"notification": "#DE3ABB",
		}
		self.socket = None



	def create_main_thread(self):
		self.listener_thread = threading.Thread(target=self.create_server, daemon=True)
		self.listener_thread.start()

		#launch the send command portal
		#self.send_command_function()

	def create_server(self):

		#MORE A SERVER CODE
		"""
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			#force stop of the socket if already used
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

			s.bind(("localhost", self.PORT))
			s.listen(1)

			self.console.print("Listening carefully...")

			while self.KILL==False:
				connection,address = s.accept()
				command = connection.recv(1024).decode()
				self.console.print(f'\n[{self.COLORS["warning"]}]Command received[/] : {command}')

				if command == "identify":
					#self.console.print(f'[{self.COLORS["warning"]}]Identification required[/]')
					self.blender_identify()
				elif command == "hello":
					self.blender_hello()
				elif command == "create_cube":
					self.blender_create_cube()
				elif command == "kill":
					self.KILL = True
				else:
					#self.exec_command_function(command)
					self.console.print("i dont want to execute!")
				connection.close()
			self.console.print(f'\n\n[{self.COLORS["notification"]}]Kill switch enabled[/]')
		"""

		#CLIENT CODE
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((self.HOST, self.PORT))
		print("Connected...")
		self.socket.send("Connected".encode())

		while True:
			command = self.socket.recv(1024).decode()
			if command == "kill":
				break
			else:
				print(f'Command received : {command}')
				#launch the execute command function
				self.exec_command_function(command)

	def exec_command_function(self, command):
		def execute_in_main_thread():
			#try to execute the command in blender
			try:
				exec(command)
				self.console.print(f'[{self.COLORS["success"]}]Command executed[/]')
			except Exception as e:
				self.console.print(f'[{self.COLORS["error"]}]Impossible to execute command\n{traceback.format_exc()}[/]')

		try:
			bpy.app.timers.register(execute_in_main_thread, first_interval=0.01)
			self.console.print(f'Sent to main blender thread')
		except Exception as e:
			self.console.print(f'[{self.COLORS["error"]}]Impossible to execute command in thread\n{traceback.format_exc()}[/]')

	#THIS PART OF THE SCRIPT NEEDS TO BE EXECUTED WITHOUT INPUT() FUNCTION THAT FREEZE MAIN BLENDER THREAD
	"""
	def send_command_function(self):
		while self.KILL == False:
			try:
				command = input("Send a command ? ...")
			except KeyboardInterrupt:
				break
			else:
				self.send_command_to_server(command)

	def send_command_to_server(self, command):
		if self.socket != None:
			try:
				self.socket.send(command.encode())
				self.console.print(f'Message sent to Server')
			except Exception as e:
				self.console.print(f'[{self.COLORS["error"]}]Impossible to send message\n{traceback.format_exc()}[/]')
	"""
	



listener_called = BlenderListener()
listener_called.create_main_thread()