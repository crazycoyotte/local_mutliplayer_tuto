import socket

class Network:
    def __init__(self):
        # Création d'un objet socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Infos du serveur
        self.server = "192.168.1.64"
        self.port = 5555
        self.addr = (self.server, self.port)

        # Connecte le client au serveur
        self.pos = self.connect()

    def get_pos(self):
        # Renvoie la position courante du joueur
        return self.pos

    def connect(self):
        try:
            # Tente de se connecter au serveur
            self.client.connect(self.addr)

            # Renvoie la position initiale du joueur
            return self.client.recv(2048).decode()
        except ConnectionRefusedError as e:
            # En cas d'erreur lors de la connexion, affiche un message d'erreur
            print(f"Network connect error : {e}")

    def send(self, data):
        try:
            # Envoie les données au serveur
            self.client.send(str.encode(data))

            # Récupère la réponse du serveur
            return self.client.recv(2048).decode()
        except socket.error as e:
            # En cas d'erreur lors de l'envoi, affiche un message d'erreur
            print(f"Network send error : {e}")
