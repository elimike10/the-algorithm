
import sys
import os
import random
import uuid

# Add the directory containing the audio_space_table.py to the Python path
sys.path.append('/home/user/the-algorithm')

from spaces_config import SpacesConfig
from audio_space_table import audio_space_table

class SpaceCallHandler:
    def __init__(self):
        self.config = SpacesConfig()
        self.audio_stream = None
        self.video_stream = None
        self.space_id = None
        self.network_stable = True

    def start_call(self):
        if self.space_id:
            print("Call is already active.")
            return

        try:
            self.space_id = str(uuid.uuid4())
            self.audio_stream = self._start_audio_stream()
            audio_space_table.audio_space_starts(self.space_id)
            if self.config.get_mode() == "video_enabled":
                self.video_stream = self._start_video_stream()
            print(f"Call started successfully. Space ID: {self.space_id}")
        except Exception as e:
            print(f"Failed to start call: {str(e)}")
            self.audio_stream = None
            self.video_stream = None
            self.space_id = None

    def end_call(self):
        if not self.space_id:
            print("No active call to end.")
            return

        audio_space_table.audio_space_finishes(self.space_id)
        self.audio_stream = None
        self.video_stream = None
        print(f"Call ended. Space ID: {self.space_id}")
        self.space_id = None

    def _start_audio_stream(self):
        return "Audio stream started"

    def _start_video_stream(self):
        return "Video stream started"

    def simulate_network_issue(self):
        self.network_stable = random.choice([True, False])
        if not self.network_stable and self.video_stream:
            self.video_stream = None
            self.config.set_mode("audio_only")
            print("Network issue detected. Switched to audio-only mode.")

    def toggle_video(self):
        if not self.space_id:
            print("Cannot toggle video: No active call.")
            return

        try:
            if self.config.get_mode() == "audio_only":
                if self.network_stable:
                    self.config.set_mode("video_enabled")
                    self.video_stream = self._start_video_stream()
                    print("Video enabled")
                else:
                    print("Cannot enable video due to network issues.")
            else:
                self.config.set_mode("audio_only")
                self.video_stream = None
                print("Video disabled")
        except Exception as e:
            print(f"Failed to toggle video: {str(e)}")
            self.config.set_mode("audio_only")
            self.video_stream = None

    def get_status(self):
        if not self.space_id:
            return "No active call"
        return f"Space ID: {self.space_id}, Mode: {self.config.get_mode()}, Audio: {'Active' if self.audio_stream else 'Inactive'}, Video: {'Active' if self.video_stream else 'Inactive'}"

def run_tests():
    print("Test 1: Basic functionality")
    handler = SpaceCallHandler()
    print("Initial state:", handler.get_status())
    handler.start_call()
    print("After start:", handler.get_status())
    handler.toggle_video()
    print("After video toggle:", handler.get_status())
    handler.end_call()
    print("After end:", handler.get_status())

    print("\nTest 2: Network issues")
    handler = SpaceCallHandler()
    handler.start_call()
    for i in range(5):
        handler.simulate_network_issue()
        handler.toggle_video()
        print(f"After toggle {i+1}:", handler.get_status())

    print("\nTest 3: Multiple active spaces")
    handlers = [SpaceCallHandler() for _ in range(3)]
    for i, h in enumerate(handlers):
        h.start_call()
        print(f"Handler {i+1}:", h.get_status())
    print(f"Live audio spaces: {audio_space_table.get_number_of_live_audio_spaces()}")
    for h in handlers:
        h.end_call()
    print(f"Live audio spaces after ending all calls: {audio_space_table.get_number_of_live_audio_spaces()}")

if __name__ == "__main__":
    run_tests()
