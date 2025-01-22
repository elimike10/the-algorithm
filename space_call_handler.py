
import sys
import os
import random
import uuid
import time

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

    def start_call(self, join_space_id=None):
        if self.space_id:
            print("You are already in a call.")
            return

        try:
            if join_space_id:
                if audio_space_table.is_space_running(join_space_id):
                    self.space_id = join_space_id
                    self.audio_stream = self._start_audio_stream()
                    print(f"Joined existing call. Space ID: {self.space_id}")
                else:
                    print("The specified call does not exist or has ended.")
                    return
            else:
                self.space_id = str(uuid.uuid4())
                self.audio_stream = self._start_audio_stream()
                audio_space_table.audio_space_starts(self.space_id)
                print(f"Call started successfully. Space ID: {self.space_id}")

            if self.config.get_mode() == "video_enabled":
                self.video_stream = self._start_video_stream()
        except Exception as e:
            print(f"Failed to start/join call: {str(e)}")
            self.audio_stream = None
            self.video_stream = None
            self.space_id = None

    def end_call(self):
        if not self.space_id:
            print("No active call to end.")
            return

        if audio_space_table.is_space_running(self.space_id):
            audio_space_table.audio_space_finishes(self.space_id)
        self.audio_stream = None
        self.video_stream = None
        print(f"Left the call. Space ID: {self.space_id}")
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

def test_comprehensive():
    print("Comprehensive test of Space Call functionality")
    audio_space_table.reset()
    
    # Start a call
    host = SpaceCallHandler()
    host.start_call()
    print("Host state:", host.get_status())
    
    # Join the active call
    participant = SpaceCallHandler()
    participant.start_call(join_space_id=host.space_id)
    print("Participant state:", participant.get_status())
    
    # Toggle video for both users
    host.toggle_video()
    participant.toggle_video()
    print("Host state after video toggle:", host.get_status())
    print("Participant state after video toggle:", participant.get_status())
    
    # Simulate network issues
    host.simulate_network_issue()
    participant.simulate_network_issue()
    
    # Toggle video again
    host.toggle_video()
    participant.toggle_video()
    print("Host state after network issue and video toggle:", host.get_status())
    print("Participant state after network issue and video toggle:", participant.get_status())
    
    # End calls
    host.end_call()
    participant.end_call()
    
    print(f"Live audio spaces after test: {audio_space_table.get_number_of_live_audio_spaces()}")

if __name__ == "__main__":
    test_comprehensive()
