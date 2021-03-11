from network import Network
from button import Button
import pygame
import sys

# server socket settings
# 54.241.79.181
HOST = "localhost"
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
game_over_font = pygame.font.Font(None, 170)

# clear and reset
btn_clear = Button(400, 10, 80, 40, (180, 180, 180), "clear")
btn_reset = Button(400, 60, 80, 40, (180, 180, 180), "reset")

# render your turn text
turn_surface = turn_font.render("Your Turn", True, (255, 255, 255))

# render game over text
x_won = game_over_font.render("X Won!", True, (150, 20, 180))
o_won = game_over_font.render("O Won!", True, (150, 20, 180))
tie_game = game_over_font.render("Tie!", True, (150, 20, 180))


def blur_surface(surface, amt=1):
    """
    Blur the given surface by the given "amount"
    :param surface: surface to blur
    :param amt: amount to blur
    :return: return blurred surface
    """
    scale = 1.0 / float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


def draw_and_update(g, player_number):
    # basic background drawing
    screen.fill((50, 100, 50))
    board_surface.fill((255, 255, 255))
    board_surface.blit(grid, (0, 0))

    # draw button
    btn_clear.draw(screen, (255, 255, 255))
    btn_reset.draw(screen, (255, 255, 255))

    # draw your turn text
    if g.round % 2 != player_number % 2:
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
                board_surface.blit(o_img, (j * 166 + 3, i * 166 + 6))
            elif g.board[i][j] == "X":
                board_surface.blit(x_img, (j * 166 + 3, i * 166 + 6))

    # draw board on screen, blur if win_move
    if g.win_move:
        screen.blit(blur_surface(board_surface, 10), (0, 120))
    else:
        screen.blit(board_surface, (0, 120))

    # draw game over text and win move
    if g.win_move:
        if g.win_move == 1:
            screen.fill((255, 0, 0), rect=(5, 120 + 160 * 0 + 83, 455, 8))
        elif g.win_move == 2:
            screen.fill((255, 0, 0), rect=(5, 120 + 160 * 1 + 83, 455, 8))
        elif g.win_move == 3:
            screen.fill((255, 0, 0), rect=(5, 120 + 160 * 2 + 83, 455, 8))
        elif g.win_move == 4:
            screen.fill((255, 0, 0), rect=(160 * 0 + 83, 120 + 5, 8, 455))
        elif g.win_move == 5:
            screen.fill((255, 0, 0), rect=(160 * 1 + 83, 120 + 5, 8, 455))
        elif g.win_move == 6:
            screen.fill((255, 0, 0), rect=(160 * 2 + 83, 120 + 5, 8, 455))
        elif g.win_move == 7:
            pygame.draw.polygon(screen, (255, 0, 0),
                                [(3, 127), (7, 123), (497, 613), (493, 617)])
        elif g.win_move == 8:
            pygame.draw.polygon(screen, (255, 0, 0),
                                [(493, 123), (497, 127), (7, 617), (3, 613)])

    if g.winner == "O":
        screen.blit(o_won, (50, 310))
    elif g.winner == "X":
        screen.blit(x_won, (50, 310))

    # update pygame display
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
