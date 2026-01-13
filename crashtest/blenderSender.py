import socket
import threading
import traceback
from rich.console import Console

class BlenderServer:
	def __init__(self):
		self.HOST = "127.0.0.1"
		self.PORT = 9010
		self.console = Console()
		self.COLORS = {
			"success": "#C5F527",
			"warning": "#F5AD27",
			"error": "#F52738",
			"notification": "#DE3ABB",
		}
		self.CLIENTS = []
		
		threading.Thread(target=self.accept_connections_function, daemon=True).start()
		self.send_loop_function()
		
	def accept_connections_function(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((self.HOST, self.PORT))
		s.listen(5)
		self.console.print(f'[{self.COLORS["notification"]}]Server launched on {self.HOST}:{self.PORT}[/]')
		
		while True:
			connection, address = s.accept()
			threading.Thread(target=self.handle_client_function, args=(connection, address), daemon=True).start()
	
	def handle_client_function(self, connection, address):
		self.console.print(f'[{self.COLORS["warning"]}]New blender client connected: {address}[/]')
		self.CLIENTS.append(connection)
		
		try:
			while True:
				data = connection.recv(1024)
				if not data:
					break
				msg = data.decode()
				self.console.print(f'[{self.COLORS["notification"]}]From {address}: {msg}[/]')
		except Exception as e:
			self.console.print(f'[{self.COLORS["error"]}]Client {address} error:\n{traceback.format_exc()}[/]')
		finally:
			if connection in self.CLIENTS:
				self.CLIENTS.remove(connection)
			connection.close()
			self.console.print(f'[{self.COLORS["warning"]}]Client {address} disconnected[/]')
	
	def send(self, command):
		if not self.CLIENTS:
			self.console.print(f'[{self.COLORS["warning"]}]No clients connected[/]')
			return
		
		self.console.print(f'[{self.COLORS["notification"]}]Sending to {len(self.CLIENTS)} client(s) → [/]{command}')
		
		disconnected = []
		for client in self.CLIENTS:
			try:
				client.send(command.encode())
			except Exception as e:
				self.console.print(f'[{self.COLORS["error"]}]Failed to send:\n{traceback.format_exc()}[/]')
				disconnected.append(client)
		
		# Nettoie les clients déconnectés
		for client in disconnected:
			if client in self.CLIENTS:
				self.CLIENTS.remove(client)
	
	def send_loop_function(self):
		self.console.print(f'\n[{self.COLORS["success"]}]Ready! Type commands (or "quit" to exit)[/]\n')
		while True:
			try:
				command = input("> ")
				if command.lower() in ["quit", "exit"]:
					self.console.print(f'[{self.COLORS["notification"]}]Shutting down...[/]')
					break
				if command.strip():
					self.send(command)
			except KeyboardInterrupt:
				self.console.print(f'\n[{self.COLORS["notification"]}]Interrupted. Shutting down...[/]')
				break

if __name__ == "__main__":
	s = BlenderServer()