import pygame

from core.game import Game


def main():
    game = Game()
    game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
