from pychievements import Achievement, tracker, icons
from pychievements.signals import receiver, goal_achieved

# Fácil n00X
# Medio n10X
# Difícil n20X
# Logros de Velocidad


class SpeedsterI(Achievement):
    name = 'Speedster I'
    category = 'speed'
    keywords = ('speed', 'time')
    goals = (
        {'level': 1, 'name': 'Speedster I',
         'icon': icons.star, 'description': 'Termina un nivel fácil en menos de 10 segundos'},
    )

    def evaluate(self, difficulty, time_taken, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 0 <= difficulty < 100 and time_taken < 10:
            self._current = 1
        return self.achieved

class SpeedsterII(Achievement):
    name = 'Speedster II'
    category = 'speed'
    keywords = ('speed', 'time')
    goals = (
        {'level': 1, 'name': 'Speedster II',
         'icon': icons.star, 'description': 'Termina un nivel medio en menos de 30 segundos'},
    )

    def evaluate(self, difficulty, time_taken, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 100 <= difficulty < 200 and time_taken < 30:
            self._current = 1
        return self.achieved

class SpeedsterIII(Achievement):
    name = 'Speedster III'
    category = 'speed'
    keywords = ('speed', 'time')
    goals = (
        {'level': 1, 'name': 'Speedster III',
         'icon': icons.star, 'description': 'Termina un nivel difícil en menos de 1 minuto'},
    )

    def evaluate(self, difficulty, time_taken, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 200 <= difficulty < 600 and time_taken < 60:
            self._current = 1
        return self.achieved


# Logros de Clicks
class MinimalistI(Achievement):
    name = 'Minimalist I'
    category = 'efficiency'
    keywords = ('puzzle', 'clicks')
    goals = (
        {'level': 1, 'name': 'Minimalist I',
         'icon': icons.unicodeCheck, 'description': 'Termina un nivel fácil en menos de 10 clicks'},
    )

    def evaluate(self, difficulty, clicks, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 0 <= difficulty < 100 and clicks < 10:
            self._current = 1
        return self.achieved

class MinimalistII(Achievement):
    name = 'Minimalist II'
    category = 'efficiency'
    keywords = ('puzzle', 'clicks')
    goals = (
        {'level': 1, 'name': 'Minimalist II',
         'icon': icons.unicodeCheck, 'description': 'Termina un nivel medio en menos de 30 clicks'},
    )

    def evaluate(self, difficulty, clicks, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 100 <= difficulty < 200 and clicks < 30:
            self._current = 1
        return self.achieved

class MinimalistIII(Achievement):
    name = 'Minimalist III'
    category = 'efficiency'
    keywords = ('puzzle', 'clicks')
    goals = (
        {'level': 1, 'name': 'Minimalist III',
         'icon': icons.unicodeCheck, 'description': 'Termina un nivel difícil en menos de 50 clicks'},
    )

    def evaluate(self, difficulty, clicks, *args, **kwargs):
        difficulty = int(difficulty.lstrip('n'))
        if 200 <= difficulty < 600 and clicks < 50:
            self._current = 1
        return self.achieved


# Logros de Progresión (sets completados) PENDIENTE
class AccessGranted(Achievement):
    name = 'Access Granted'
    category = 'progression'
    keywords = ('puzzle', 'completion')
    goals = (
        {'level': 1, 'name': 'Access Granted',
         'icon': icons.star, 'description': 'Completa el set de niveles fáciles'},
    )

    def evaluate(self, difficulty, *args, **kwargs):
        if difficulty == 'easy':
            self._current = 1
        return self.achieved

class Breacher(Achievement):
    name = 'Breacher'
    category = 'progression'
    keywords = ('puzzle', 'completion')
    goals = (
        {'level': 1, 'name': 'Breacher',
         'icon': icons.star, 'description': 'Completa el set de niveles medios'},
    )

    def evaluate(self, difficulty, *args, **kwargs):
        if difficulty == 'medium':
            self._current = 1
        return self.achieved

class Netrunner(Achievement):
    name = 'Netrunner'
    category = 'progression'
    keywords = ('puzzle', 'completion')
    goals = (
        {'level': 1, 'name': 'Netrunner',
         'icon': icons.star, 'description': 'Completa el set de niveles difíciles'},
    )

    def evaluate(self, difficulty, *args, **kwargs):
        if difficulty == 'hard':
            self._current = 1
        return self.achieved


# Logros Especiales     PENDIENTE
class HueShift(Achievement):
    name = 'HUE Shift'
    category = 'special'
    keywords = ('puzzle', 'special')
    goals = (
        {'level': 1, 'name': 'HUE Shift',
         'icon': icons.unicodeCheckBox, 'description': 'Cambia el color de tu UI y juega un nivel'},
    )

    def evaluate(self, *args, **kwargs):
        self._current = 1
        return self.achieved

class Picasso(Achievement):
    name = 'Picasso'
    category = 'special'
    keywords = ('puzzle', 'special')
    goals = (
        {'level': 1, 'name': 'Picasso',
         'icon': icons.unicodeCheckBox, 'description': 'Dibuja 3 puzzles de distintos tamaños'},
    )

    def evaluate(self, *args, **kwargs):
        self._current = 1
        return self.achieved

class Completionist(Achievement):
    name = 'Completionist'
    category = 'special'
    keywords = ('puzzle', 'special')
    goals = (
        {'level': 1, 'name': 'Completionist',
         'icon': icons.star, 'description': 'Completa todos los logros'},
    )

    def evaluate(self, *args, **kwargs):
        self._current = 1
        return self.achieved


class NonogramAchievementTracker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NonogramAchievementTracker, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.player_id = "player1"
        self._initialized = True
        self.completed_sizes = set()

        # Registrar todos los logros
        if not tracker.achievements():
            # Logros de velocidad
            tracker.register(SpeedsterI)
            tracker.register(SpeedsterII)
            tracker.register(SpeedsterIII)

            # Logros de Clicks
            tracker.register(MinimalistI)
            tracker.register(MinimalistII)
            tracker.register(MinimalistIII)

            # Logros de progresión (sets completados)
            tracker.register(AccessGranted)
            tracker.register(Breacher)
            tracker.register(Netrunner)

            # Logros especiales
            tracker.register(HueShift)
            tracker.register(Picasso)
            tracker.register(Completionist)

    def puzzle_completed(self, difficulty, time_taken, clicks, size):
        # Evaluar logros de velocidad
        tracker.evaluate(self.player_id, SpeedsterI, difficulty, time_taken)
        tracker.evaluate(self.player_id, SpeedsterII, difficulty, time_taken)
        tracker.evaluate(self.player_id, SpeedsterIII, difficulty, time_taken)

        # Evaluar logros de clicks mínimos
        tracker.evaluate(self.player_id, MinimalistI, difficulty, clicks)
        tracker.evaluate(self.player_id, MinimalistII, difficulty, clicks)
        tracker.evaluate(self.player_id, MinimalistIII, difficulty, clicks)

        # Tracking para Picasso
        self.completed_sizes.add(size)
        if len(self.completed_sizes) >= 3:
            tracker.evaluate(self.player_id, Picasso)

    ####################PENDIENTE##############################################
    def complete_difficulty_set(self, difficulty):
        difficulty = int(difficulty.lstrip('n'))
        if difficulty < 200:
            tracker.evaluate(self.player_id, AccessGranted, difficulty)
        elif difficulty < 400:
            tracker.evaluate(self.player_id, Breacher, difficulty)
        elif difficulty < 600:
            tracker.evaluate(self.player_id, Netrunner, difficulty)


    def ui_color_changed(self):
        tracker.evaluate(self.player_id, HueShift)

    ###########################################################################


    def check_completionist(self):
        """Verifica si se han completado todos los otros logros"""
        all_achievements = [SpeedsterI, SpeedsterII, SpeedsterIII, MinimalistI, MinimalistII, MinimalistIII,
            AccessGranted, Breacher, Netrunner, HueShift, Picasso]

        all_complete = True
        for achievement in all_achievements:
            if tracker.unachieved(self.player_id, achievement):
                all_complete = False
                break

        if all_complete:
            tracker.evaluate(self.player_id, Completionist)

    # Print en consola los logros (para testear)
    def show_achievements(self, show_all=False):
        Achievements = []
        all_achievements = [
            SpeedsterI, SpeedsterII, SpeedsterIII,
            MinimalistI, MinimalistII, MinimalistIII,
            AccessGranted, Breacher, Netrunner,
            HueShift, Picasso, Completionist
        ]

        for achievement in all_achievements:
            achieved = tracker.achieved(self.player_id, achievement)
            for goal in achieved:
                Achievements.append(goal['name'])
        return Achievements

# Muestra mensaje en la consola cuando se alcanza un nuevo logro
@receiver(goal_achieved)
def new_goal(tracked_id, achievement, goals, **kwargs):
    for goal in goals:
        print(f"\n🏆 ¡Logro desbloqueado! {goal['name']}")
        print(f"   {goal['description']}")