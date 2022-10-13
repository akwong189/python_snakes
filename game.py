from datetime import datetime
import random
import threading
from time import sleep
import numpy as np
from rich.console import Console
from bot.samplebot import RandomBot

from snake import Snake
from runner import SnakeRunner
from direction import Direction

TIMEOUT_THRESHOLD = 1
TILE_VALUES = {
    "apple": 1,
    "snake0": 2,
    "snake1": 3,
    "body": 4
}
EMOJI_TILES = {
    0: "⬛",
    1: "🟥", # 🍎
    2: "0️⃣",
    3: "🔟",
    4: "🟩"
}
EMOJI_NUMBERS = {
    " ": "🟧",
    0: "0️⃣",
    1: "🟧",
    2: "*️⃣",
    3: "🟧",
    4: "🔟",
    5: "🟧",
    6: "*️⃣",
    7: "🟧",
    8: "🔟",
    9: "🟧",
}

class SnakeGame:
    def __init__(self, map_size, head0, tail_dir0, head1, tail_dir1, size, bot0, bot1):
        self.game_result = "0 - 0"
        self.apple_eaten0 = 0
        self.apple_eaten1 = 0
        self.num_it_apple_not_eaten = 0
        self.snake_size = 0
        self.name0 = ""
        self.name1 = ""
        self.start_time = 0

        self.snake_size = size
        self.startTime = datetime.now()
        self.map_size = map_size
        self.snake0 = Snake(head0, tail_dir0, size, map_size)
        self.snake1 = Snake(head1, tail_dir1, size, map_size)
        self.bot0 = bot0
        self.bot1 = bot1
        self.name0 = bot0.__class__.__name__
        self.name1 = bot1.__class__.__name__
        
        self.apple_coord = self.random_nonoccupied_cell()
        self.env = np.zeros(self.map_size)

        self.console = Console()
        self.tiler = lambda i: EMOJI_TILES[i]
        self.vectorize = np.vectorize(self.tiler)


    def to_matrix(self):
        self.env = np.zeros(self.map_size)
        self.env[self.apple_coord] = TILE_VALUES["apple"]

        for index, i in enumerate(self.snake0.body):
            if index == 0:
                self.env[i] = TILE_VALUES["snake0"]
            else:
                self.env[i] = TILE_VALUES["body"]
        for index, i in enumerate(self.snake1.body):
            if index == 0:
                self.env[i] = TILE_VALUES["snake1"]
            else:
                self.env[i] = TILE_VALUES["body"]

    def draw_board(self):
        # self.console.clear()
        self.to_matrix()

        nums = map(lambda x: EMOJI_NUMBERS[x % 10], list(range(self.map_size[1])))
        self.console.print( "⬛" + "".join(nums))
        
        for r in range(self.map_size[0]):
            row = "%2d" % r + "".join(list(self.vectorize(self.env[r, :])))
            self.console.print(row)

    def random_nonoccupied_cell(self):
        while True:
            coord = (random.randint(0, self.map_size[0]-1), random.randint(0, self.map_size[1]-1))
            if coord in self.snake0.elements or coord in self.snake1.elements:
                continue
            return coord
        
    def run_one_step(self):
        self.console.clear()
        bot0_thread = SnakeRunner(self.bot0, self.snake0, self.snake0, map_size, self.apple_coord)
        s0_timeout = False

        try:
            bot0_thread.start()
            bot0_thread.join(TIMEOUT_THRESHOLD)
        except Exception as e:
            s0_timeout = True
            self.console.print(f"Bot 0 threw an exception {e}")

        if bot0_thread.is_alive():
            bot0_thread.stop()
            s0_timeout = True
            self.console.print("Bot 0 timed out")

        d0 = bot0_thread.direction

        bot1_thread = SnakeRunner(self.bot1, self.snake1, self.snake1, map_size, self.apple_coord)
        s1_timeout = False

        try:
            bot1_thread.start()
            bot1_thread.join(TIMEOUT_THRESHOLD)
        except Exception as e:
            s1_timeout = True
            self.console.print(f"Bot 1 threw an exception {e}")

        if bot1_thread.is_alive():
            bot1_thread.stop()
            s1_timeout = True
            self.console.print("Bot 1 timed out")

        d1 = bot1_thread.direction
        # self.console.print(bot0_thread.is_alive(), bot1_thread.is_alive())

        timeout = s0_timeout or s1_timeout
        if timeout:
            self.game_result = f"{0 if s0_timeout else 1} - {0 if s1_timeout else 1}"
            return False
        
        self.console.print(f"snake 0 -> {d0}, snake 1 -> {d1}")
        self.console.print(f"Apples eaten: {self.apple_eaten0} - {self.apple_eaten1}")

        grow0 = Snake.move_to(self.snake0.get_head(), d0) == self.apple_coord
        grow1 = Snake.move_to(self.snake1.get_head(), d1) == self.apple_coord
        # self.console.print(grow0, grow1)
        
        was_grow = grow0 or grow1

        s0head, s0dead, s0r = self.snake0.move(d0, grow0, self.console)
        s1head, s1dead, s1r = self.snake1.move(d1, grow1, self.console)

        s0dead = not s0dead
        s1dead = not s1dead
        # self.console.print(s0r, s0head, self.snake0.elements, s1r, s1head)

        if was_grow or self.apple_coord == None:
            self.apple_eaten0 = len(self.snake0.body) - self.snake_size
            self.apple_eaten1 = len(self.snake1.body) - self.snake_size
            self.apple_coord = self.random_nonoccupied_cell()
            self.num_it_apple_not_eaten = 0
        else:
            if self.num_it_apple_not_eaten == 10:
               self.apple_coord = self.random_nonoccupied_cell()
               self.num_it_apple_not_eaten = 0
            else:
               self.num_it_apple_not_eaten += 1
        
        s0dead |= self.snake0.head_collides_with(self.snake1)
        s1dead |= self.snake1.head_collides_with(self.snake0)

        cont = not (s0dead or s1dead)
        # self.console.print(s0dead, s1dead)

        if not cont:
            result = "0 - 0"
            if s0dead ^ s1dead:
                result = f"{0 if s0dead else 1} - {0 if s1dead else 1}"
            elif s0dead and s1dead:
                result = f"{1 if self.apple_eaten0 > self.apple_eaten1 else 0} - {1 if self.apple_eaten1 > self.apple_eaten0 else 0}"
            self.game_result = result
        self.draw_board()
        return cont

    def run(self, delay=1.0):
        while self.run_one_step():
            try:
                sleep(delay)
            except:
                return
        self.console.print(self.game_result)

if __name__ == "__main__":
    map_size = (10, 20)
    head0 = (1, 1)
    head1 = (4, 4)
    tail_dir0 = Direction.RIGHT
    tail_dir1 = Direction.DOWN
    size = 4
    bot0 = RandomBot()
    bot1 = RandomBot()
    game = SnakeGame(map_size=map_size, head0=head0, head1=head1, tail_dir0=tail_dir0, tail_dir1=tail_dir1, size=size, bot0=bot0, bot1=bot1)
    # game.draw_board()
    game.run(delay=0.25)