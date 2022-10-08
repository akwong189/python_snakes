import threading


class SnakeRunner(threading.Thread):
    def __init__(self, bot, snake, opponent, map_size, apple):
        super(SnakeRunner, self).__init__()
        self._stop_event = threading.Event()

        self.bot = bot
        self.snake = snake
        self.opponent = opponent
        self.map_size = map_size
        self.apple = apple
        self.direction = None

    def run(self):
        self.direction = self.bot.choose_direction(self.snake, self.opponent, self.map_size, self.apple)

    def stop(self):
        self._stop_event.set()