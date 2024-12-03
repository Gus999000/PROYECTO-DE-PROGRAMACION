from Gráfica.Create_Nonograma import createNonogram
from Gráfica.Ventana_Nonograma import nonogramWindow
from Gráfica.Menu_and_scaling_exp_standalone import menuWindow, options_Menu, video_Options, level_type_Screen, difficulty_Screen, level_selection_Screen, controls_Options, audio_Options, create_Screen, achievements_Screen
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
        self.gameStateManager = GameStateManager("menuWindow")
        ########### Ventanas ###########
        # Menu
        self.start = Start(self.screen, self.gameStateManager)
        self.menuWindow = menuWindow(self.screen, self.gameStateManager)

        # Opciones
        self.optionsMenu = options_Menu(self.screen, self.gameStateManager)
        self.videoOptions = video_Options(self.screen, self.gameStateManager)
        self.audioOptions = audio_Options(self.screen, self.gameStateManager)
        self.controlsOptions = controls_Options(self.screen, self.gameStateManager)


        #Jugar
        self.levelTypeScreen = level_type_Screen(self.screen, self.gameStateManager)
        self.difficultyScreen = difficulty_Screen(self.screen, self.gameStateManager)
        self.levelSelectionScreen = level_selection_Screen(self.screen, self.gameStateManager)

        # Crear
        self.createScreen = create_Screen(self.screen, self.gameStateManager)
        self.createNonogram = createNonogram(self.screen, self.gameStateManager)

        # Logros
        self.achievementsScreen = achievements_Screen(self.screen, self.gameStateManager)

        # Nonograma
        self.nonogramWindow = nonogramWindow(self.screen, self.gameStateManager)

        ########### Ventanas ###########

        # Palabras clave para el cambio de estados
        self.states = {
            'start': self.start,
            'nonogramWindow': self.nonogramWindow,
            'menuWindow': self.menuWindow,
            'optionsMenu': self.optionsMenu,
            'videoOptions': self.videoOptions,
            'audioOptions': self.audioOptions,
            'controlsOptions': self.controlsOptions,
            'levelTypeScreen': self.levelTypeScreen,
            'difficultyScreen': self.difficultyScreen,
            'levelSelectionScreen': self.levelSelectionScreen,
            'createScreen': self.createScreen,
            'createNonogram': self.createNonogram,
            "achievementsScreen": self.achievementsScreen
        }

    def run(self):
        while True:
            # Cambiar ID de ventanas
            self.levelSelectionScreen.set_id(self.gameStateManager.id)
            # Eventos
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
    id = 0
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state
    def set_state_id(self, state, id):
        self.id = id
        self.currentState = state

if __name__ == "__main__":
    game = Game()

    game.run()
