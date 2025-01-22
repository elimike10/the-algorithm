
import time
from collections import deque
from threading import Lock

class AudioSpaceTable:
    AUDIO_EVENT_EXPIRATION_DURATION = 12 * 60 * 60  # 12 hours in seconds

    def __init__(self):
        self.started_spaces = set()
        self.finished_spaces = set()
        self.timestamped_space_events = deque()
        self.lock = Lock()

    def audio_space_starts(self, space_id):
        with self.lock:
            space_seen_before = space_id in self.started_spaces
            self.started_spaces.add(space_id)
            self.timestamped_space_events.append((time.time(), space_id))
            self._purge_old_spaces()
            return space_seen_before

    def audio_space_finishes(self, space_id):
        with self.lock:
            space_seen_before = space_id in self.finished_spaces
            self.finished_spaces.add(space_id)
            self.timestamped_space_events.append((time.time(), space_id))
            self._purge_old_spaces()
            return space_seen_before

    def is_space_running(self, space_id):
        with self.lock:
            return space_id in self.started_spaces and space_id not in self.finished_spaces

    def _purge_old_spaces(self):
        now = time.time()
        while self.timestamped_space_events:
            timestamp, space_id = self.timestamped_space_events[0]
            if now - timestamp > self.AUDIO_EVENT_EXPIRATION_DURATION:
                self.timestamped_space_events.popleft()
                self.started_spaces.discard(space_id)
                self.finished_spaces.discard(space_id)
            else:
                break

    def get_number_of_live_audio_spaces(self):
        with self.lock:
            return sum(1 for space in self.started_spaces if space not in self.finished_spaces)

    def reset(self):
        with self.lock:
            self.started_spaces.clear()
            self.finished_spaces.clear()
            self.timestamped_space_events.clear()

audio_space_table = AudioSpaceTable()
