import pygame
from network import Network

pygame.init()

# Constantes
BLACK = 0, 0, 0
GREEN = 0, 255, 0

# création de la fenetre
width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# numero de client
clientNumber = 0


class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

def read_pos(str):
    # conversion d'une chaîne de caractères en un tuple d'entiers
    if str:
        str = str.split(",")
        return int(str[0]), int(str[1])
    else:
        return 0, 0

def make_pos(tup):
    # conversion d'un tuple d'entiers en une chaîne de caractères
    return str(tup[0]) + "," + str(tup[1])

def redrawWindow(win, player, player2):
    # effacer l'écran et redessiner les joueurs
    win.fill((BLACK))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    n = Network()
    # position de départ du joueur
    startpos = read_pos(n.get_pos())
    p = Player(startpos[0], startpos[1], 100, 100, GREEN)
    p2 = Player(0, 0, 100, 100, GREEN)
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # envoyer la position du joueur à l'autre client et recevoir la position de l'autre client
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        # déplacer le joueur local en fonction des touches du clavier
        p.move()
        # redessiner la fenêtre
        redrawWindow(win, p, p2)


main()
