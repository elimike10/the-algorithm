
class SpacesConfig:
    def __init__(self):
        self.audio_video_mode = "audio_only"  # Default mode

    def set_mode(self, mode):
        if mode in ["audio_only", "video_enabled"]:
            self.audio_video_mode = mode
        else:
            raise ValueError("Invalid mode. Use 'audio_only' or 'video_enabled'.")

    def get_mode(self):
        return self.audio_video_mode
