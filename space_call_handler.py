
from spaces_config import SpacesConfig

class SpaceCallHandler:
    def __init__(self):
        self.config = SpacesConfig()
        self.audio_stream = None
        self.video_stream = None
        self.call_active = False

    def start_call(self):
        if self.call_active:
            print("Call is already active.")
            return

        try:
            self.audio_stream = self._start_audio_stream()
            self.call_active = True
            if self.config.get_mode() == "video_enabled":
                self.video_stream = self._start_video_stream()
            print("Call started successfully.")
        except Exception as e:
            print(f"Failed to start call: {str(e)}")
            self.audio_stream = None
            self.video_stream = None
            self.call_active = False

    def end_call(self):
        if not self.call_active:
            print("No active call to end.")
            return

        self.audio_stream = None
        self.video_stream = None
        self.call_active = False
        print("Call ended.")

    def _start_audio_stream(self):
        # Simulating potential network issues
        import random
        if random.random() < 0.1:  # 10% chance of failure
            raise Exception("Network error: Could not start audio stream")
        return "Audio stream started"

    def _start_video_stream(self):
        # Simulating potential device issues
        import random
        if random.random() < 0.2:  # 20% chance of failure
            raise Exception("Device error: Could not start video stream")
        return "Video stream started"

    def toggle_video(self):
        if not self.call_active:
            print("Cannot toggle video: No active call.")
            return

        try:
            if self.config.get_mode() == "audio_only":
                self.config.set_mode("video_enabled")
                self.video_stream = self._start_video_stream()
                print("Video enabled")
            else:
                self.config.set_mode("audio_only")
                self.video_stream = None
                print("Video disabled")
        except Exception as e:
            print(f"Failed to toggle video: {str(e)}")
            self.config.set_mode("audio_only")
            self.video_stream = None

    def get_status(self):
        if not self.call_active:
            return "No active call"
        return f"Mode: {self.config.get_mode()}, Audio: {'Active' if self.audio_stream else 'Inactive'}, Video: {'Active' if self.video_stream else 'Inactive'}"

# Test the implementation
def run_tests():
    handler = SpaceCallHandler()
    
    print("Test 1: Initial state")
    print(handler.get_status())

    print("\nTest 2: Starting call")
    handler.start_call()
    print(handler.get_status())

    print("\nTest 3: Toggling video")
    handler.toggle_video()
    print(handler.get_status())

    print("\nTest 4: Toggling video again")
    handler.toggle_video()
    print(handler.get_status())

    print("\nTest 5: Ending call")
    handler.end_call()
    print(handler.get_status())

    print("\nTest 6: Toggling video on ended call")
    handler.toggle_video()

    print("\nTest 7: Starting call with video enabled")
    handler.config.set_mode("video_enabled")
    handler.start_call()
    print(handler.get_status())

    print("\nTest 8: Multiple call starts")
    handler.start_call()

    print("\nTest 9: Ending call multiple times")
    handler.end_call()
    handler.end_call()

run_tests()
