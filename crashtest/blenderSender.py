import socket
import json
import rich

from rich.console import Console

class BlenderSender:
	def __init__(self):
		self.HOST = "127.0.0.1"
		self.PORT = 9010

		#define rich colors and create console
		self.console = Console()
		self.COLORS = {
			"success":"#C5F527",
			"warning":"#F5AD27",
			"error":"#F52738",
			"notification": "#DE3ABB",
		}

	def send(self, cmd, data=None):
		self.console.print(f'\n[{self.COLORS["notification"]}]Sending Command → [/]{cmd}')
		
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((self.HOST,self.PORT))
			s.sendall(json.dumps(
				{
					"cmd":cmd,
					"data":{}
				}
			).encode())
			response = s.recv(8192)
			self.console.print(f'[{self.COLORS["notification"]}]Answer → [/]{response}')
		
