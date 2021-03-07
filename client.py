from network import Network
from button import Button
import pygame
import sys

# server socket settings
HOST = "54.241.79.181"
PORT = 5555

# network, connection with server
network = Network(HOST, PORT)
print(network.id)

# pygame settings
WIDTH = 500
HEIGHT = 620

# pygame initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
board_surface = pygame.Surface((500, 500))

# asset load
o_img = pygame.transform.scale(pygame.image.load("asset\\o.png"), (155, 155))
x_img = pygame.transform.scale(pygame.image.load("asset\\x.png"), (155, 155))
grid = pygame.image.load("asset\\grid.png")

# font
base_font = pygame.font.Font(None, 45)
turn_font = pygame.font.Font(None, 35)

# clear and reset
btn_clear = Button(400, 10, 80, 40, (180, 180, 180), "clear")
btn_reset = Button(400, 60, 80, 40, (180, 180, 180), "reset")

# render your turn text
turn_surface = turn_font.render("Your Turn", True, (255, 255, 255))


def draw_and_update(g, player_number):
    # basic background drawing
    screen.fill((50, 100, 50))
    board_surface.fill((255, 255, 255))
    board_surface.blit(grid, (0, 0))

    # draw button
    btn_clear.draw(screen, (255, 255, 255))
    btn_reset.draw(screen, (255, 255, 255))

    # draw your turn text
    if g.round % 2 + 1 == player_number:
        screen.blit(turn_surface, (180, 90))

    # draw score
    player1_score, player2_score = g.score
    score = f"player 1: {player1_score} vs {player2_score} :player 2"
    score_surface = base_font.render(score, True, (255, 255, 255))
    screen.blit(score_surface, (10, 30))

    # draw O or X
    for i in range(3):
        for j in range(3):
            if g.board[i][j] == "O":
                board_surface.blit(o_img, (j * 166, i * 166))
            elif g.board[i][j] == "X":
                board_surface.blit(x_img, (j * 166, i * 166))

    screen.blit(board_surface, (0, 120))
    pygame.display.flip()


def main():
    run = True
    game_input = (-1, -1)
    player_number = None

    while run:
        clock.tick(30)

        # receive  data
        game = network.send(game_input)
        game_input = (-1, -1)  # default input
        player_number = game.current_player \
            if player_number is None else player_number

        # events
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                network.client.close()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = (my - 120) // 166
                    y = mx // 166
                    if btn_clear.is_over((mx, my)):
                        game_input = (-2, -2)
                    elif btn_reset.is_over((mx, my)):
                        game_input = (-3, -3)
                    else:
                        game_input = (x, y)
            if event.type == pygame.MOUSEMOTION:
                if btn_clear.is_over((mx, my)):
                    btn_clear.color = (180, 180, 180)
                else:
                    btn_clear.color = (220, 220, 220)
                if btn_reset.is_over((mx, my)):
                    btn_reset.color = (180, 180, 180)
                else:
                    btn_reset.color = (220, 220, 220)

        # draw display and surface
        draw_and_update(game, player_number)


if __name__ == "__main__":
    main()
