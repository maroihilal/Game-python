import pygame
import sys
from game import Game

class RunnerGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Infinity Rush")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game(self.screen)
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            self.game.handle_events(events)
            self.game.update()
            self.game.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = RunnerGame()
    game.run()