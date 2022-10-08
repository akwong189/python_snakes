from direction import Direction


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def add(self, a, b):
        return Coordinate(a.x + b.x, a.y + b.y)

    def move_to(self, direction):
        return Coordinate.add(self, direction.v)

    def get_direction(self, other):
        vec = Coordinate(other.x - self.x, other.y - self.y)
        for direction in Direction.values():
            if direction.dx == vec.x and direction.dy == vec.y:
                return direction
        return None 

    def in_bounds(self, map_size):
        return self.x >= 0 and self.y >= 0 and self.x < map_size[0] and self.y < map_size[1]

    def __eq__(self, other):
        if self == other: return True
        if other is None or self.__class__.__name__ != other.__class__.__name__: return False
        return self.x == other.x and self.y == other.y

    
