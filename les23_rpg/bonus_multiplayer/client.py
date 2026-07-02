"""
Multiplayer Client - Verbindt met de game server
"""

import socket

class GameClient:
    """Client voor multiplayer RPG"""
    
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.name = ""
    
    def connect(self):
        """Verbind met de server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.running = True
            return True
        except Exception as e:
            print(f"❌ Kan niet verbinden: {e}")
            return False
    
    def run(self):
        """Start de client loop"""
        if not self.connect():
            return
        
        # Vraag naam
        name_msg = self.socket.recv(1024).decode()
        print(name_msg, end="")
        self.name = input().strip()
        self.socket.send(self.name.encode())
        
        # Ontvang welkomstbericht
        response = self.socket.recv(1024).decode()
        print(response)
        
        print("\n🎮 Verbonden met RPG Server!")
        print("Typ 'quit' om te stoppen\n")
        
        try:
            while self.running:
                # Luister naar server berichten
                try:
                    self.socket.settimeout(0.1)
                    data = self.socket.recv(4096).decode()
                    if data:
                        print(data)
                except socket.timeout:
                    pass
                
                # Stuur eigen commando's
                if self.socket.fileno() != -1:  # Check if socket is still open
                    cmd = input()
                    if cmd.lower() == 'quit':
                        self.running = False
                        break
                    self.socket.send(cmd.encode())
                    
        except KeyboardInterrupt:
            print("\n👋 Verbinding verbroken")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Opruimen bij stoppen"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("🛑 Client gestopt.")

if __name__ == "__main__":
    client = GameClient()
    client.run()