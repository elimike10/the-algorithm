
import time
from collections import deque
from threading import Lock

class EnhancedAudioSpaceTable:
    def __init__(self):
        self.active_spaces = {}
        self.finished_spaces = set()
        self.timestamped_space_events = []
        self.lock = Lock()

    def audio_space_starts(self, space_id):
        with self.lock:
            self.active_spaces[space_id] = time.time()
            self.timestamped_space_events.append((time.time(), space_id))

    def audio_space_finishes(self, space_id):
        with self.lock:
            if space_id in self.active_spaces:
                del self.active_spaces[space_id]
                self.finished_spaces.add(space_id)
            else:
                print(f"Warning: Attempting to finish a call that was not started: {space_id}")

    def is_space_running(self, space_id):
        with self.lock:
            return space_id in self.active_spaces

    def get_number_of_live_audio_spaces(self):
        with self.lock:
            return len(self.active_spaces)

    def reset(self):
        with self.lock:
            self.active_spaces.clear()
            self.finished_spaces.clear()
            self.timestamped_space_events.clear()

audio_space_table = EnhancedAudioSpaceTable()
