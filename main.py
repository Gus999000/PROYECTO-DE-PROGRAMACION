from random import random

from Gráfica.Create_Nonograma import createNonogram
from Gráfica.Ventana_Nonograma import nonogramWindow
from Gráfica.Menu_and_scaling_exp_standalone import menuWindow, options_Menu, video_Options, level_type_Screen, \
    difficulty_Screen, level_selection_Screen, controls_Options, audio_Options, create_Screen, achievements_Screen
from Lógica.Logros import NonogramAchievementTracker
import pygame
import sys

FPS = 60


class MusicManager:
    def __init__(self):
        # Inicializar mezclador de Pygame
        pygame.mixer.init()

        # Definir grupos de pistas de música
        self.track_groups = {
            'menu_tracks': [
                'optionsMenu',
                'videoOptions',
                'audioOptions',
                'controlsOptions',
                'levelTypeScreen',
                'difficultyScreen',
                'levelSelectionScreen',
                'createScreen'
            ],
            'title_tracks': [
                'start',
                'menuWindow',
                'achievementsScreen'
            ],
            'level_tracks': [
                'nonogramWindow'
            ]
        }

        # Definir pistas de música para diferentes pantallas
        self.tracks = {
            'start': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',
            'menuWindow': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',
            'optionsMenu': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'videoOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'audioOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'controlsOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'levelTypeScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'difficultyScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'levelSelectionScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'createScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'createNonogram': 'Gráfica/Recursos/Audio/MUSICA/Pantalla_dibujo.wav',
            'achievementsScreen': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',
            'nonogramWindow': [
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_a.wav',
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_b.wav',
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_c.wav'
            ]
        }

        # Pista actualmente en reproducción
        self.current_track = None
        self.current_group = None
        self.current_state = None

    def update_music(self, current_state):
        """
        Actualizar música automáticamente según el estado actual del juego.
        :param current_state: Estado actual del GameStateManager
        """
        # Determinar a qué grupo pertenece el estado actual
        current_group = self._get_track_group(current_state)

        # Verificar si estamos en el mismo grupo y pista
        if current_group == self.current_group:
            return

        # Manejar música de diferentes estados
        if current_state in self.tracks:
            # Verificar si la pista es una lista (para selección aleatoria)
            if isinstance(self.tracks[current_state], list):
                track = random.choice(self.tracks[current_state])
            else:
                track = self.tracks[current_state]

            # Reproducir la pista
            self._play_track(track)

            # Actualizar estado y grupo actual
            self.current_state = current_state
            self.current_group = current_group

    def _get_track_group(self, state):
        """
        Encontrar el grupo al que pertenece un estado.
        :param state: Estado actual del juego
        :return: Nombre del grupo o None
        """
        for group, states in self.track_groups.items():
            if state in states:
                return group
        return None

    def _play_track(self, track, loops=-1):
        """
        Método interno para reproducir una pista específica.
        :param track: Ruta del archivo de música
        :param loops: Número de veces para repetir (-1 para infinito)
        """
        # Detener pista actual si se está reproduciendo en un grupo diferente
        if self.current_track and track != self.current_track:
            pygame.mixer.music.stop()

        try:
            # Cargar y reproducir la nueva pista
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(loops)
            self.current_track = track
        except pygame.error as e:
            print(f"Error al reproducir la pista de música {track}: {e}")

    def stop_music(self):
        """
        Detener la música actualmente en reproducción.
        """
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_state = None
        self.current_group = None

    def set_volume(self, volume):
        """
        Establecer el volumen de la música.
        :param volume: Float entre 0.0 y 1.0
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))


class Game:
    WINDOW_SCALE = 3
    SCREEN_SIZE = (256 * WINDOW_SCALE, 240 * WINDOW_SCALE)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        # Inicializar el administrador de música
        self.music_manager = MusicManager()

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

        # Jugar
        self.levelTypeScreen = level_type_Screen(self.screen, self.gameStateManager)
        self.difficultyScreen = difficulty_Screen(self.screen, self.gameStateManager)
        self.levelSelectionScreen = level_selection_Screen(self.screen, self.gameStateManager)

        # Crear
        self.createScreen = create_Screen(self.screen, self.gameStateManager)
        self.createNonogram = createNonogram(self.screen, self.gameStateManager)

        # Logros
        self.achievementsScreen = achievements_Screen(self.screen, self.gameStateManager)
        self.achievement_tracker = NonogramAchievementTracker()

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

            # Actualizar música según el estado actual
            self.music_manager.update_music(self.gameStateManager.get_state())

            # Ejecutar el estado actual
            self.states[self.gameStateManager.get_state()].run(events)

            pygame.display.update()
            self.clock.tick(FPS)


# Clase de la ventana de inicio, reemplazar luego
class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self, events):
        self.display.fill('red')


# Clase que cambiará los estados entre las ventanas
class GameStateManager:
    id = 0
    id_nonograma = ""
    create_nonogram_puzzle_size = 20
    cargar_matriz = ""

    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

    def set_state_id(self, state, id):
        self.id = id
        self.currentState = state

    def set_id_nonograma(self, id):
        self.id_nonograma = id

    def get_id_nonograma(self):
        return self.id_nonograma

    def set_create_nonogram_puzzle_size(self, size):
        self.create_nonogram_puzzle_size = size

    def get_create_nonogram_puzzle_size(self):
        return self.create_nonogram_puzzle_size

    def set_cargar_matriz(self, id):
        self.cargar_matriz = id

    def get_cargar_matriz(self):
        return self.cargar_matriz


if __name__ == "__main__":
    game = Game()
    game.run()