import random
from bot.bot import Bot
from direction import Direction
from snake import Snake

class RandomBot(Bot):

    def collides_body(self, snake, valid_dirs):
        head = snake.get_head()
        r = []

        for d in valid_dirs:
            h = Snake.move_to(head, d)
            valid = h not in snake.elements
            if valid: r.append(d)
        return r

    def collides_walls(self, snake, map_size, valid_dirs):
        head = snake.get_head()
        r = []

        for d in valid_dirs:
            h = Snake.move_to(head, d)
            valid = Snake.in_bounds(map_size, h)
            if valid: r.append(d)
        return r

    def choose_direction(self, snake, opponent, map_size, apple):
        valid_directions = [Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT]
        valid_directions = self.collides_body(snake, valid_directions)
        valid_directions = self.collides_walls(snake, map_size, valid_directions)

        if len(valid_directions) == 0:
            return random.choice([Direction.DOWN, Direction.UP, Direction.LEFT, Direction.RIGHT])
        return random.choice(valid_directions)