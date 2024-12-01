import numpy as np
from collections import deque

class NonogramHistory:
    def __init__(self, initial_state):
        self.undo_stack = deque([initial_state.copy()])  # Estado inicial
        self.redo_stack = deque()
        self.max_history = 50  # Límite de estados

    def push_state(self, state):
        # Guarda el nuevo estado
        self.undo_stack.append(state.copy())
        # Limpia el stack cuando se hace una nueva acción
        self.redo_stack.clear()
        # Mantiene el tamaño dentro del límite
        if len(self.undo_stack) > self.max_history:
            self.undo_stack.popleft()

    def undo(self):
        if len(self.undo_stack) > 1:  # Mantiene al menos un estado en el stack
            current_state = self.undo_stack.pop()
            self.redo_stack.append(current_state)
            return self.undo_stack[-1].copy()
        return self.undo_stack[0].copy()

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            return state.copy()
        return self.undo_stack[-1].copy()