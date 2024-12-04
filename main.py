from Gráfica.Create_Nonograma import createNonogram
from Gráfica.Ventana_Nonograma import nonogramWindow
from Gráfica.Menu_and_scaling_exp_standalone import menuWindow, options_Menu, video_Options, level_type_Screen, \
    difficulty_Screen, level_selection_Screen, controls_Options, audio_Options, create_Screen, achievements_Screen
from Lógica.Logros import NonogramAchievementTracker
import pygame
import sys
import random

FPS = 60


class MusicManager:
    def __init__(self):
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Define music track groups
        self.track_groups = {
            'menu_tracks': [
                'menuWindow',
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
                'achievementsScreen'
            ],
            'level_tracks': [
                'nonogramWindow'
            ]
        }

        # Define music tracks for different screens
        self.tracks = {
            'start': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',
            'menuWindow': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',  # Changed from musica_menus.wav
            'optionsMenu': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'videoOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'audioOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'controlsOptions': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'levelTypeScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'difficultyScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'levelSelectionScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'createScreen': 'Gráfica/Recursos/Audio/MUSICA/musica_menus.wav',
            'createNonogram': 'Gráfica/Recursos/Audio/MUSICA/Pantalla_dibujo.wav',
            'achievementsScreen': 'Gráfica/Recursos/Audio/MUSICA/Menu_de_titulo.wav',  # Kept as Menu_de_titulo.wav
            'nonogramWindow': [
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_a.wav',
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_b.wav',
                'Gráfica/Recursos/Audio/MUSICA/Musica_nivel_c.wav'
            ]
        }

        # You might also want to update the track groups
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

        # Currently playing track
        self.current_track = None
        self.current_group = None
        self.current_state = None

    def update_music(self, current_state):
        """
        Automatically update music based on the current game state.
        :param current_state: Current state from GameStateManager
        """
        # Determine which group the current state belongs to
        current_group = self._get_track_group(current_state)

        # Check if we're in the same group and track
        if current_group == self.current_group:
            return

        # Handle different state music
        if current_state in self.tracks:
            # Check if the track is a list (for random selection)
            if isinstance(self.tracks[current_state], list):
                track = random.choice(self.tracks[current_state])
            else:
                track = self.tracks[current_state]

            # Play the track
            self._play_track(track)

            # Update current state and group
            self.current_state = current_state
            self.current_group = current_group

    def _get_track_group(self, state):
        """
        Find the group a state belongs to.
        :param state: Current game state
        :return: Group name or None
        """
        for group, states in self.track_groups.items():
            if state in states:
                return group
        return None

    def _play_track(self, track, loops=-1):
        """
        Internal method to play a specific track.
        :param track: Path to the music file
        :param loops: Number of times to loop (-1 for infinite)
        """
        # Stop current track if playing in a different group
        if self.current_track and track != self.current_track:
            pygame.mixer.music.stop()

        try:
            # Load and play the new track
            pygame.mixer.music.load(track)
            pygame.mixer.music.play(loops)
            self.current_track = track
        except pygame.error as e:
            print(f"Error playing music track {track}: {e}")

    def stop_music(self):
        """
        Stop the currently playing music.
        """
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_state = None
        self.current_group = None

    def set_volume(self, volume):
        """
        Set the volume of the music.
        :param volume: Float between 0.0 and 1.0
        """
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

class Game:
    WINDOW_SCALE = 3
    SCREEN_SIZE = (256 * WINDOW_SCALE, 240 * WINDOW_SCALE)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        # Music Manager
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

        self.achievement_tracker = NonogramAchievementTracker()

    def run(self):
        while True:
            # Update music based on current state
            self.music_manager.update_music(self.gameStateManager.get_state())

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

    def run(self, events):
        self.display.fill('red')
        # Implement any start screen logic here


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