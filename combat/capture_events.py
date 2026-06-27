class CaptureBuffer:
    def __init__(self):
        self.captured_player_units = []
        self.captured_ai_units = []
        
    def add_player_capture(self, piece):
        self.captured_player_units.append(piece)
        
    def add_ai_capture(self, piece):
        self.captured_ai_units.append(piece)
        
    def clear(self):
        self.captured_player_units.clear()
        self.captured_ai_units.clear()
