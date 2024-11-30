from Gráfica.Ventana_Nonograma import nonogramWindow
from Lógica.Logros import NonogramAchievementTracker
import pygame
import sys

WINDOW_SCALE = 3
SCREEN_SIZE = (256 * WINDOW_SCALE, 240 * WINDOW_SCALE)

FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        # Aquí es donde se cambia el estado del juego, probar cambiar con "nonogramWindow" y "start"
        self.gameStateManager = GameStateManager("nonogramWindow")
        # Ventanas
        self.start = Start(self.screen, self.gameStateManager)
        self.nonogramWindow = nonogramWindow(self.screen, self.gameStateManager)

        self.states = {'start': self.start, 'nonogramWindow': self.nonogramWindow}

        self.achievement_tracker = NonogramAchievementTracker()

    def run(self):
        while True:

            events = pygame.event.get()

            for event in events:
                # SALIR
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.states[self.gameStateManager.get_state()].run(events)

            pygame.display.update()
            self.clock.tick(FPS)

# CLase de la ventana de inicio, reemplazar luego
class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('red')

# Clase que cambiará los estados entre las ventanas
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

if __name__ == "__main__":
    game = Game()

    game.run()
