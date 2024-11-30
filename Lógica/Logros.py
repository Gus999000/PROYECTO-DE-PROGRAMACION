from pychievements import Achievement, tracker, icons
from pychievements.signals import receiver, goal_achieved


# Logro por número de puzzles completados
class PuzzleMaster(Achievement):
    name = 'Puzzle Master'
    category = 'nonogram'
    keywords = ('puzzle', 'completion')
    goals = (
        {'level': 1, 'name': 'Puzzle Beginner',
         'icon': icons.star, 'description': 'Completed 1 nonogram puzzles'},
        {'level': 15, 'name': 'Puzzle Explorer',
         'icon': icons.star, 'description': 'Completed 15 nonogram puzzles'},
        {'level': 30, 'name': 'Puzzle Expert',
         'icon': icons.star, 'description': 'Completed 30 nonogram puzzles'},
        {'level': 50, 'name': 'Puzzle Master',
         'icon': icons.star, 'description': 'Completed 50 nonogram puzzles'},
    )


# Logro por velocidad
class SpeedMaster(Achievement):
    name = 'Speed Master'
    category = 'nonogram'
    keywords = ('puzzle', 'speed')
    goals = (
        {'level': 1, 'name': 'Quick Solver',
         'icon': icons.unicodeCheck, 'description': 'Solved a puzzle in under 5 minutes'},
        {'level': 2, 'name': 'Speed Runner',
         'icon': icons.unicodeCheckBox, 'description': 'Solved a puzzle in under 3 minutes'},
        {'level': 3, 'name': 'Lightning Fast',
         'icon': icons.star, 'description': 'Solved a puzzle in under 1 minute'},
    )

    def evaluate(self, time_taken, *args, **kwargs):
        """Evalúa el tiempo tomado y determina el nivel alcanzado"""
        if (int(time_taken) < 60):  # Menos de 1 minuto
            self._current = 3
        elif (int(time_taken) < 180):  # Menos de 3 minutos
            self._current = 2
        elif (int(time_taken) < 300):  # Menos de 5 minutos
            self._current = 1
        return self.achieved


# Registrar los logros con el tracker
tracker.register(PuzzleMaster)
tracker.register(SpeedMaster)


# Receptor de señales para mostrar mensajes cuando se alcanza un logro
@receiver(goal_achieved)
def new_goal(tracked_id, achievement, goals, **kwargs):
    """Muestra un mensaje cuando se alcanza un nuevo logro"""
    for goal in goals:
        print(f"\n🏆 ¡Logro desbloqueado! {goal['name']}")
        print(f"   {goal['description']}")





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

        # Registrar los logros solo la primera vez
        if not tracker.achievements():
            tracker.register(PuzzleMaster)
            tracker.register(SpeedMaster)

    def puzzle_completed(self, time_taken):
        tracker.increment(self.player_id, PuzzleMaster)
        tracker.evaluate(self.player_id, SpeedMaster, time_taken)

    def show_achievements(self, show_all=False):
        print("\n=== Logros Conseguidos ===")
        for achievement in [PuzzleMaster, SpeedMaster]:
            achieved = tracker.achieved(self.player_id, achievement)
            for goal in achieved:
                print(f"{goal['icon']} {goal['name']}: {goal['description']}")

        if show_all:
            print("\n=== Logros Pendientes ===")
            for achievement in [PuzzleMaster, SpeedMaster]:
                unachieved = tracker.unachieved(self.player_id, achievement)
                for goal in unachieved:
                    print(f"{goal['icon']} {goal['name']}: {goal['description']}")


# Ejemplo de uso
def main():
    # Crear el tracker de logros
    achievement_tracker = NonogramAchievementTracker()

    # Simular completar algunos puzzles
    achievement_tracker.puzzle_completed(400)  # 6:40 minutos
    achievement_tracker.puzzle_completed(240)  # 4 minutos
    achievement_tracker.puzzle_completed(45)  # 45 segundos

    # Mostrar todos los logros
    achievement_tracker.show_achievements(show_all=True)


if __name__ == "__main__":
    main()