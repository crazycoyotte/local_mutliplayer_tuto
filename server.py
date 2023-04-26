import socket
from _thread import *
import sys

# Configuration du serveur
server = "192.168.1.64"  # Adresse IP du serveur
port = 5555  # Port d'écoute du serveur

# Création d'un objet socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tentative de connexion du socket à l'adresse et au port spécifiés
try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

# Mise en écoute de nouvelles connexions
s.listen(2)  # Le serveur peut accepter jusqu'à 2 connexions simultanées
print("Waiting for a connection, Server Started")


# Fonction pour convertir une chaîne de caractères en position
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


# Fonction pour convertir une position en chaîne de caractères
def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# Positions initiales des joueurs
pos = [(0, 0), (100, 100)]


# Fonction pour traiter les connexions des clients
def threaded_client(conn, player):
    # Envoi de la position initiale du joueur
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            # Réception des données du client
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            # Si les données ne sont pas valides, on arrête la connexion
            if not data:
                print("Disconnected")
                break
            else:
                # Si le joueur est le joueur 1, on renvoie la position du joueur 2
                # Sinon, on renvoie la position du joueur 1
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("received : ", data)
                print("sending : ", reply)

            # Envoi de la réponse à tous les clients connectés
            conn.sendall(str.encode(make_pos(reply)))
        except error as e:
            print("Server thread error : ", e)
            break

    # Fermeture de la connexion
    print("Lost connection")
    conn.close()


# Numéro du joueur courant
currentPlayer = 0

# Boucle principale pour accepter de nouvelles connexions
while True:
    # Attente d'une nouvelle connexion
    conn, addr = s.accept()
    print("Connected to:", addr)

    # Démarrage d'un nouveau thread pour gérer la connexion
    start_new_thread(threaded_client, (conn, currentPlayer))

    # Changement du joueur courant
    currentPlayer += 1
