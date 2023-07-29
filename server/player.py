class Player:
    def __init__(self, websocket):
        self.websocket = websocket
        self.num = None
        self.field = None
        self.user_id = None
        self.move = False
        self.move_start = None
